# Copyright (c) 2024 Itz-fork
# Project: Unless

import os

from re import findall
from setuptools import setup, find_packages

os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))


# Readme
def get_description():
    if os.path.isfile("README.md"):
        with open(("README.md"), encoding="utf-8") as readmeh:
            return readmeh.read()
    else:
        return "Lightweight python library for error handling"


# Version
def find_version():
    with open("unless/__init__.py", encoding="utf-8") as f:
        return findall(r"__version__ = \"(.+)\"", f.read())[0]


version = find_version()

setup(
    name="unless-handler",
    version=version,
    description="Lightweight python library for error handling",
    url="https://github.com/Itz-fork/Unless",
    author="Itz-fork",
    author_email="git.itzfork@gmail.com",
    license="MIT",
    packages=find_packages(),
    download_url=f"https://github.com/Itz-fork/Unless/archive/refs/tags/v{version}.tar.gz",
    keywords=["unless", "error-handler", "simplified", "error", "python-error-handler"],
    long_description=get_description(),
    long_description_content_type="text/markdown",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    python_requires=">=3.6",
)
