![pyrobotstx feature image](docs/img/feature-image.png)

# pyrobotstxt: Python Package for **robots.txt** Files

``pyrobotstxt`` package can be used to (systematically) generate **robots.txt** files. Moreover, this package comes in handy for creating and including ``ASCII`` images in **robots.txt** files.

In future releases, it would be possible to parse and analyze **robots.txt** file generated using any software (not limited to ``pyrobotstxt``)

## Whats in PyRobotsTxt?

We believe in monolithic software development and created this tiny package that does its job without any bloat. It is useful for 

- Createing **robots.txt** File
- Parsing a **robots.txt** File [in progress]
- Analyzing **robots.txt** File [in progress]

## Installation

You can install this package using ``pip`` with the following command. It should also work with other methods, e.g. ``pipenv`` or ``poetry``. If you encounter any installation problems, please create an ``issue``.

```bash
pip install pyrobotstxt
```

## Usage

There are several use cases for ``pyrobotstxt``. 

### Basic
You can use it to check the details of a search bot. Just specify a keyword, e.g. ``Google``, and it will provide a list of Google bots in the ``pyrobotstxt`` database.

```python
from pyrobotstxt import RobotsTxt
print(RobotsTxt().robots_name("Google"))
```
You can also do a reverse search by providing a robot name. Again, you will get details about that bot.

```python
from pyrobotstxt import RobotsTxt
print(RobotsTxt().robots_details("Googlebot"))
```

### Advance

You can create a robot file by creating an object of the ``RobotsTxt`` class. 

```python
from pyrobotstxt import RobotsTxt
robots_file = RobotsTxt()
```

You can add a header and footer section. These are comments for humans looking into this **robots.txt** file. In the header section, you can also include file creation ``date``. It is handy for archiving purposes.

```python
robots_file.include_header("Welcome Crawlers", append_date=True)
robots_file.include_footer("Good Bye Crawlers")
```

In **robots.txt** file, rules are specified as per user agent. ``pyrobotstxt`` offer a ``UserAgent`` class. You can use it to create multiple user agent. Default user agent is ``*``. 

```python
ua_general = UserAgent(name="*")
```
After creating a user agent, you can add all those routes/pages/images you want to Allow or Disallow.

```python
ua_general.add_allow(
    allow_items=["/home", "/deep", "/home"],
    unique=True,
    comments="This is a list of allowed items",
)

ua_general.add_disallow(
    disallow_items=["/nopi$", "/topi?a", "/img*.png$"],
    unique=True,
    comments="This is a list of allowed items",
)
```

Here is a complete example of a user agent. You can also include a sitemap of your website.

```python
ua_general_google = UserAgent(name="Google")
ua_general_google.add_allow(
    allow_items=["/home", "/deep", "/home"],
    unique=True,
    comments="This is a list of allowed items",
)
ua_general_google.add_disallow(
    disallow_items=["/nopi$", "/topi?a", "/img*.png$"],
    unique=True,
    comments="This is a list of allowed items",
)
ua_general_google.add_sitemap("https://seowings.org/sitemap.xml")
```

After you have prepared user agents, you can add them to the ``RobotsTxt`` object. This object keeps a list of all the user agents.

```python
robots_file.add_user_agent(ua_general)
robots_file.add_user_agent(ua_general_google)
```

You can also include any image (``ASCII`` format) in your **robots.txt** file. For example, add the following command in your script/program to include an ``ASCII`` image in your **robots.txt** file.

```python
robots_file.include_image("logo_dark.png", 90)
```

In the end, you can save this file to the desired location. The default name of the file is **robots.txt**.

```python
robots_file.write("robots.txt")
```

## Contribute

Pull Requests, Feature Suggestions, and collaborations are welcome.