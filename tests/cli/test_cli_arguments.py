#!/usr/bin/env python

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.

from __future__ import absolute_import, print_function, unicode_literals

import subprocess
import unittest


class TestCLIArguments(unittest.TestCase):
    """Test CLI entry script for arguments."""

    def test_unrecognized_argument(self):
        try:
            output = subprocess.check_output(['mozdownload', '--abc'],
                                             stderr=subprocess.STDOUT)
        except subprocess.CalledProcessError as e:
            output = e.output

        self.assertRegexpMatches(output, r'mozdownload: error: unrecognized arguments: --abc')
