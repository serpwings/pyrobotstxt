#!/usr/bin/env python
# -*- coding: utf-8 -*- #

"""
pyrobotstxt: A Python Package for robots.txt Files.

MIT License
Copyright (c) 2022 SeoWings www.seowings.org
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

from setuptools import setup

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

version = "0.0.1"

setup(
    name="pyrobotstxt",
    version=version,
    author="Faisal Shahzad",
    author_email="seowingsorg@gmail.com",
    description="Python Package to Generate and Analyse Robots.txt files",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/seowings/pyrobotstxt/",
    project_urls={
        "Bug Tracker": "https://github.com/seowings/pyrobotstxt/issues",
        "Documentation": "https://pyrobotstxt.seowings.org/",
    },
    classifiers=[
        "Topic :: Utilities",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    packages=["pyrobotstxt"],
    python_requires=">=3.9",
    install_requires=["pillow==9.3.0"]
)