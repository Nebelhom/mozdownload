#!/usr/bin/env python

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.

import os
import re

from setuptools import setup

THIS_DIR = os.path.dirname(os.path.realpath(__name__))


def read(*parts):
    with open(os.path.join(THIS_DIR, *parts)) as f:
        return f.read()


def get_version():
    return re.findall("__version__ = '([\d\.]+)'",
                      read('mozdownload', 'cli.py'), re.M)[0]

setup(name='mozdownload',
      version=get_version(),
      description='Script to download builds for Firefox and Thunderbird '
                  'from the Mozilla server.',
      long_description=read('README.md'),
      # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
      classifiers=[],
      keywords='mozilla',
      author='Mozilla Automation and Testing Team',
      author_email='tools@lists.mozilla.com',
      url='https://github.com/mozilla/mozdownload',
      license='Mozilla Public License 2.0 (MPL 2.0)',
      packages=['mozdownload'],
      zip_safe=False,
      install_requires=read('requirements.txt').splitlines(),
      entry_points="""
      # -*- Entry points: -*-
      [console_scripts]
      mozdownload = mozdownload.cli:cli
      """,
      )
