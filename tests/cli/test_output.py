#!/usr/bin/env python

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.

from __future__ import absolute_import, print_function, unicode_literals

import subprocess
import unittest

from mozdownload import __version__, cli


class TestCLIOutput(unittest.TestCase):
    """Tests for the cli() function in scraper.py"""

    def test_cli_executes(self):
        """Test that cli will start and print usage message"""
        output = subprocess.check_output(['mozdownload', '--help'])
        self.assertTrue(cli.__doc__.format(__version__) in output)
