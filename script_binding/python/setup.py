#!/usr/bin/env python
# -*- coding: utf8 -*-

from distutils.core import setup

setup(name="pyftk-ctypes",
      version="0.6",
      author="hotforest",
      author_email="hotforest@gmail.com",
      url="https://github.com/htbegin/pyftk",
      description="python binding for ftk",
      long_description="""The binding is implemented by using python ctypes. \
It provides the c-style interfaces, not the oo-style interfaces.""",
      classifiers = [
          "Development Status :: 4 - Beta",
          "Intended Audience :: Developers",
          "Operating System :: POSIX",
          "Programming Language :: Python",
          "Topic :: Software Development :: User Interfaces",
          "Topic :: Software Development :: Widget Sets",
          ],
      license="LGPL",
      platforms=["linux"],
      packages=["ftk"],
)
