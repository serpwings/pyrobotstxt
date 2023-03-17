#!/usr/bin/env python
# -*- coding: utf-8 -*- #

"""
pyrobotstxt: A Python Package for robots.txt Files.

MIT License
Copyright (c) 2022 SERP Wings www.serpwings.com
Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:
The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.
THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

# +++++++++++++++++++++++++++++++++++++++++++++++++++++
# IMPORTS Standard Library
# +++++++++++++++++++++++++++++++++++++++++++++++++++++

import re
from unittest.mock import Mock
import os
import json
from math import ceil
from datetime import datetime

# +++++++++++++++++++++++++++++++++++++++++++++++++++++
# IMPORTS 3rd Party Libraries
# +++++++++++++++++++++++++++++++++++++++++++++++++++++

import requests
from requests.adapters import HTTPAdapter
from requests.models import Response
from bs4 import BeautifulSoup
from PIL import Image

# +++++++++++++++++++++++++++++++++++++++++++++++++++++
# CONSTANTS / ROBOTS DataBase
# +++++++++++++++++++++++++++++++++++++++++++++++++++++

ROBOTS = {
    "Applebot": "Apple",
    "AhrefsBot": "Ahrefs",
    "Baiduspider": "Baidu",
    "Bingbot": "Microsoft Bing",
    "Discordbot": "Discord",
    "DuckDuckBot": "DuckDuckGo",
    "Googlebot": "Google Search Bot",
    "Googlebot-Image": "Google Image Bot",
    "LinkedInBot": "LinkedIn Bot",
    "MJ12bot": "MJ12bot",
    "Pinterestbot": "Pinterest",
    "SemrushBot": "Semrsh",
    "Slurp": "Slurp",
    "TelegramBot": "Telegram",
    "Twitterbot": "Twitter Bot",
    "Yandex": "Yandex",
    "YandexBot": "YandexBot",
    "facebot": "Facebook",
    "msnbot": "MSN Bot",
    "rogerbot": "MOZ Bot",
    "xenu": "xenu",
}

HEADER = {
    "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0",
}

# +++++++++++++++++++++++++++++++++++++++++++++++++++++
# UTIL FUNCTIONS
# +++++++++++++++++++++++++++++++++++++++++++++++++++++


def mock_requests_object(url):
    """ """
    response = Mock(spec=Response)
    response.text = ""
    response.status_code = 9999
    response.url = url
    return response


def get_remote_content(url, max_retires=5):
    """ """
    try:
        s = requests.Session()
        s.mount(url, HTTPAdapter(max_retries=max_retires))
        return s.get(url, headers=HEADER)
    except:
        return mock_requests_object(url)


def get_corrected_url(url, fix_slash="sitemap.xml"):
    """ """
    if not url.startswith("http://") and not url.startswith("https://"):
        url = f"http://{url}"

    if not url.endswith(fix_slash):
        url = f"{url}/{fix_slash}"

    return url


# +++++++++++++++++++++++++++++++++++++++++++++++++++++
# CLASSES
# +++++++++++++++++++++++++++++++++++++++++++++++++++++


class ImageAsASCII:
    """Class to Convert RGB/GRAYSCALE Images to ASCII (Text) format."""

    def __init__(self, image_path=None, desired_width=90):
        """intializes an object of ImageAsASCII class. A user need to
        specify desired (ascii) image width and the path of RGB/Gray Image.

        Args:
            desired_width (int, optional): width of the desired output ASCII Image.
            image_path (str, optional):path of the input image. If None then conversion will not work.
        """

        if not image_path:
            raise ValueError

        self.ascii_str_map = [" ", *("*$+?.%;:,@")]
        self.ascii_image = ""
        self.image = Image.open(image_path).convert("L")

        desired_height = desired_width * self.image.height / self.image.width
        self.image = self.image.resize((ceil(desired_width), ceil(desired_height)))

    def map_to_ascii(self):
        """map each pixel of indvidual image to a respective ascii value from ascii_str_map.
        This is achieved by deviding each pixel to ca. 10 equal parts (//25) and then maped to respecive value.
        """

        str_container = ""  # a container to hold ascii charcters
        for pixel in self.image.getdata():
            str_container += self.ascii_str_map[pixel // 25]

        self.ascii_image = "#\t"  # Now transform the string container to column format.
        for i in range(0, len(str_container), self.image.width):
            self.ascii_image += (
                " ".join(str_container[i : i + self.image.width]) + "\n#\t"
            )


class UserAgent:
    def __init__(self, ua_name="*", crawl_delay=0):
        """Initialize UserAgent objet with a user-agent name and crawl delay varible.

        Args:
            ua_name (str, optional): name of the user-agent. Defaults to "*".
            crawl_delay (int, optional): crawl delay value for user agent/bots. Defaults to 0.
        """
        self.user_agent_name = ua_name
        self.crawl_delay = crawl_delay
        self.sitemaps = []  # lists of sitemap for current UserAgent
        self.allowed = []  # lists of Allowed Items for current UserAgent
        self.disallowed = []  # lists of Disallowed Items for current UserAgent
        self.content = ""  # consolidate content for robots.txt file

    def add_allow(self, allow_items, unique=True, comments=""):
        """Add allowed items/pages/slugs to current User Agent.

        Args:
            allow_items (str, list): single item or list of items allowed for current user agnet.
            unique (bool, optional): If True duplicate item stripped to single value. Defaults to True.
            comments (str, optional): Any comments for added value for human readability. Defaults to "".
        """

        if isinstance(allow_items, str):
            allow_items = [allow_items]

        if not isinstance(allow_items, list):
            print("not supported", type(allow_items))  # raise exception
            raise TypeError
        else:
            self.allowed += allow_items
            if unique:
                self.allowed = list(set(self.allowed))

    def remove_allow(self, allow_item):
        """Remove any previously added allowed item from allowed list.

        Args:
            allow_item (str, list): item(s) to be removed.
        """

        if allow_item in self.allowed:
            self.allowed -= [allow_item]

    def add_disallow(self, disallow_items, unique=True, comments=""):
        """Add disallowed items/pages/slugs to current User Agent.

        Args:
            disallow_items (str, list): single item or list of items disallowed for current user agnet.
            unique (bool, optional): If True duplicate item stripped to single value. Defaults to True.
            comments (str, optional): Any comments for added value for human readability. Defaults to "".
        """
        if isinstance(disallow_items, str):
            disallow_items = [disallow_items]

        if not isinstance(disallow_items, list):
            print("not supported", type(disallow_items))  # raise exception
            raise TypeError
        else:
            self.disallowed += disallow_items
            if unique:
                self.disallowed = list(set(self.disallowed))

    def remove_disallow(self, disallow_item):
        """Remove any previously added disallowed item from allowed list.

        Args:
            disallow_item (str, list): item(s) to be removed.
        """

        if disallow_item in self.disallowed:
            self.disallowed -= [disallow_item]

    def add_sitemap(self, site_map_path=None, comments=""):
        """add file path of sitemap to current user agent.

        Args:
            site_map_path (str): location of sitemap. Defaults to None.
            comments (str): any comments to include with sitemap path. Defaults to "".
        """
        if not site_map_path:
            raise ValueError

        self.sitemaps.append(site_map_path)

    def remove_sitemap(self, site_map_path=None):
        """remove a sitemap from current user agent.

        Args:
            site_map_path (str): sitemap file path to be removed. Defaults to None.
        """

        if site_map_path in self.sitemaps:
            self.sitemaps -= [site_map_path]

    def disallow_pagination(self, prefix="/page/*", comments=""):
        """Single function to disable pagination on a website using robots.txt file.

        Args:
            prefix (str, optional): prefix for pages (default - /page/). Defaults to "/page/*".
            comments (str, optional): human readable comments for inclusion. Defaults to "".
        """
        self.add_disallow(disallow_item=prefix, comments=comments)

    def consolidate(self):
        """consolidate all the information (allowed, disallowed, sitemaps) in single text string."""

        self.content = f"User-agent: {self.user_agent_name}"

        # Support for including Crawl_delay. see feature request #1
        if self.crawl_delay > 0:
            self.content += f"\nCrawl-delay: {self.crawl_delay}\n"

        if self.allowed:
            self.content += "\n# Allowed Patterns\n"
            self.content += "\n".join([f"Allow: {item}" for item in self.allowed])

        if self.disallowed:
            self.content += "\n\n# Disallowed Patterns\n"
            self.content += "\n".join([f"Disallow: {item}" for item in self.disallowed])

        if self.sitemaps:
            self.content += "\n\n# Site Maps\n"
            self.content += "\n".join([f"Sitemap: {item}" for item in self.sitemaps])

        self.content += "\n\n"


class RobotsTxt:
    def __init__(self, version=""):
        """Intializes Robots.txt operations

        Args:
            version (str, optional): Version number (optional) for robots.txt. Defaults to "".
        """
        self.user_agents = []
        self.create_time = datetime.now()
        self.version = version
        self.image_branding = None
        self.header = ""  # message added to the start of the output file.
        self.footer = ""  # message added to the end of the output file.

    def read(self, robots_url):
        """read a robots.txt File"""

        self.create_time = datetime.now()
        robots_url = get_corrected_url(robots_url, "")
        response = get_remote_content(robots_url)

        if response.status_code < 400:
            for ua_item in response.text.split("User-agent:"):
                if ua_item:
                    ua_content_items = [
                        ua_split_item.strip() for ua_split_item in ua_item.split("\n") if ua_split_item
                    ]
                    if not ua_content_items[0].startswith("#"):
                        ua = UserAgent(ua_name=ua_content_items[0])
                        ua.add_allow(
                            [
                                it.split("Allow:")[-1]
                                for it in ua_content_items[1:]
                                if it.startswith("Allow:")
                            ]
                        )
                        ua.add_disallow(
                            [
                                it.split("Disallow:")[-1]
                                for it in ua_content_items[1:]
                                if it.startswith("Disallow:")
                            ]
                        )
                        # TODO: Comments are not included Yet
                        comment = [
                            it.split("# ")[-1]
                            for it in ua_content_items[1:]
                            if it.startswith("#")
                        ]

                        self.add_user_agent(ua=ua)

    def write(self, file_path="robots.txt"):
        """write robots.txt file at a given file_path location.

        Args:
            file_path (str, optional): location of robots.txt file. Defaults to "robots.txt".
        """

        with open(file_path, "w") as f:
            # include header
            if self.header:
                f.write(f"# {self.header}")

            # include user agents with consolidate text
            for ua in self.user_agents:
                ua.consolidate()
                f.write(ua.content)

            f.write("\n")

            # append ascii image, if available
            if self.image_branding:
                f.write(self.image_branding)

            # append footer message
            if self.footer:
                f.write(f"\n# {self.footer}")

    def include_header(self, message="", append_date=True):
        """include header message with/without creation date.

        Args:
            message (str, optional): header or header message. Defaults to "".
            append_date (bool, optional): Append date/time to the header. Defaults to True.
        """

        self.header = message

        if append_date:
            self.header += f"\n# Created on {self.create_time} using pyrobotstxt"

    def include_footer(self, message=""):
        """include footer message

        Args:
            message (str, optional): footer message. Defaults to "".
        """
        self.footer = message

    def include_image(self, image_path=None, desired_width=90):
        """includes ascii image provided at image_file

        Args:
            image_path (str): location of image file. Defaults to None.
            desired_width (int, optional): desired width of ASCII image. Defaults to 90(chars).
        """
        img = ImageAsASCII(image_path=image_path, desired_width=desired_width)
        img.map_to_ascii()
        self.image_branding = img.ascii_image

    def add_user_agent(self, ua):
        """Add/Append user agent to RobotsTxt

        Args:
            ua (UserAgent): user agent to be included in final robots.txt file.
        """
        self.user_agents.append(ua)

    def remove_user_agent(self, ua_name=""):
        """Remove user agent from RobotsTxt

        Args:
            ua_name (UserAgent): user agent to be removed from already included in robots.txt file.
        """
        self.user_agents -= [ua for ua in self.user_agents if ua.name == ua_name]

    @staticmethod
    def robots_name(crawl_bot):
        """Find robot name, if you know any keywrod about that crawl bot.

        Args:
            crawl_bot (str): description about the crawl bot. e.g. facebook

        Returns:
            (dict): all matching crawl bots with relevent information
        """
        return {
            robot: ROBOTS[robot]
            for robot in ROBOTS
            if crawl_bot.capitalize() in ROBOTS[robot]
        }

    @staticmethod
    def robots_details(crawl_bot):
        """Static Method to return details about any crawl bot.

        Args:
            crawl_bot (str): name of crawl bot

        Returns:
            (dict): information about all crawl bots matching to input string.
        """
        return {
            robot: ROBOTS[robot]
            for robot in ROBOTS
            if crawl_bot.lower() == robot.lower()
        }
