#!/usr/bin/env python

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.

import os
import unittest
import urllib

from mozdownload import TinderboxScraper
from mozdownload.utils import urljoin

import mozhttpd_base_test as mhttpd


firefox_tests = [
    # -p win32
    {'args': {'platform': 'win32'},
     'filename': '1374583608-mozilla-central-firefox-25.0a1.en-US.win32.installer.exe',
     'url': 'firefox/tinderbox-builds/mozilla-central-win32/'
            '1374583608/firefox-25.0a1.en-US.win32.installer.exe'},
    # -p win32 --branch=mozilla-central
    {'args': {'branch': 'mozilla-central',
              'platform': 'win32'},
     'filename': '1374583608-mozilla-central-firefox-25.0a1.en-US.win32.installer.exe',
     'url': 'firefox/tinderbox-builds/mozilla-central-win32/'
            '1374583608/firefox-25.0a1.en-US.win32.installer.exe'},
    # -a firefox -p win32
    {'args': {'application': 'firefox',
              'platform': 'win32'},
     'filename': '1374583608-mozilla-central-firefox-25.0a1.en-US.win32.installer.exe',
     'url': 'firefox/tinderbox-builds/mozilla-central-win32/'
            '1374583608/firefox-25.0a1.en-US.win32.installer.exe'},
    # -a firefox -p win32 --date 1374573725 --stub (old format)
    {'args': {'application': 'firefox',
              'platform': 'win32',
              'date': '1374573725',
              'is_stub_installer': True},
     'filename': '1374573725-mozilla-central-firefox-25.0a1.en-US.win32.installer-stub.exe',
     'url': 'firefox/tinderbox-builds/mozilla-central-win32/'
            '1374573725/firefox-25.0a1.en-US.win32.installer-stub.exe'},
    # -a firefox -p win32 --stub (new format)
    {'args': {'application': 'firefox',
              'platform': 'win32',
              'date': '1374583608',
              'is_stub_installer': True},
     'filename': '1374583608-mozilla-central-setup.exe',
     'url': 'firefox/tinderbox-builds/mozilla-central-win32/'
            '1374583608/setup.exe'},
    # -a firefox -p linux --branch=mozilla-central
    {'args': {'branch': 'mozilla-central',
              'platform': 'linux'},
     'filename': '1374583608-mozilla-central-firefox-25.0a1.en-US.linux-i686.tar.bz2',
     'url': 'firefox/tinderbox-builds/mozilla-central-linux/'
            '1374583608/firefox-25.0a1.en-US.linux-i686.tar.bz2'},
    # -a firefox -p linux64 --branch=mozilla-central
    {'args': {'branch': 'mozilla-central',
              'platform': 'linux64'},
     'filename': '1374583608-mozilla-central-firefox-25.0a1.en-US.linux-x86_64.tar.bz2',
     'url': 'firefox/tinderbox-builds/mozilla-central-linux64/'
            '1374583608/firefox-25.0a1.en-US.linux-x86_64.tar.bz2'},
    # -a firefox -p win32 --branch=mozilla-central
    {'args': {'application': 'firefox',
              'branch': 'mozilla-central',
              'platform': 'win32'},
     'filename': '1374583608-mozilla-central-firefox-25.0a1.en-US.win32.installer.exe',
     'url': 'firefox/tinderbox-builds/mozilla-central-win32/'
            '1374583608/firefox-25.0a1.en-US.win32.installer.exe'},
    # -a firefox -p win64 --branch=mozilla-central
    {'args': {'application': 'firefox',
              'branch': 'mozilla-central',
              'platform': 'win64'},
     'filename': '1423517445-mozilla-central-firefox-38.0a1.en-US.win64.installer.exe',
     'url': 'firefox/tinderbox-builds/mozilla-central-win64/'
            '1423517445/firefox-38.0a1.en-US.win64.installer.exe'},
    # -a firefox -p win64 --branch=mozilla-central --date=2013-07-23 (old filename format)
    {'args': {'application': 'firefox',
              'branch': 'mozilla-central',
              'platform': 'win64',
              'date': '2013-07-23'},
     'filename': '1374583608-mozilla-central-firefox-25.0a1.en-US.win64-x86_64.installer.exe',
     'url': 'firefox/tinderbox-builds/mozilla-central-win64/'
            '1374583608/firefox-25.0a1.en-US.win64-x86_64.installer.exe'},
    # -a firefox -p mac64 --branch=mozilla-central
    {'args': {'application': 'firefox',
              'branch': 'mozilla-central',
              'platform': 'mac64'},
     'filename': '1374583608-mozilla-central-firefox-25.0a1.en-US.mac.dmg',
     'url': 'firefox/tinderbox-builds/mozilla-central-macosx64/'
            '1374583608/firefox-25.0a1.en-US.mac.dmg'},
    # -a firefox -p win32 --branch=mozilla-central --debug-build
    {'args': {'application': 'firefox',
              'branch': 'mozilla-central',
              'debug_build': True,
              'platform': 'win32'},
     'filename': '1374583608-mozilla-central-debug-firefox-25.0a1.en-US.win32.installer.exe',
     'url': 'firefox/tinderbox-builds/mozilla-central-win32-debug/'
            '1374583608/firefox-25.0a1.en-US.win32.installer.exe'},
    # -a firefox -p win32 --branch=mozilla-central -l de
    {'args': {'application': 'firefox',
              'branch': 'mozilla-central',
              'locale': 'de',
              'platform': 'win32'},
     'filename': 'mozilla-central-firefox-25.0a1.de.win32.installer.exe',
     'url': 'firefox/tinderbox-builds/mozilla-central-l10n/'
            'firefox-25.0a1.de.win32.installer.exe'},
    # -a firefox -p win32 --branch=mozilla-central -l pt-PT
    {'args': {'application': 'firefox',
              'branch': 'mozilla-central',
              'locale': 'pt-PT',
              'platform': 'win32'},
     'filename': 'mozilla-central-firefox-25.0a1.pt-PT.win32.installer.exe',
     'url': 'firefox/tinderbox-builds/mozilla-central-l10n/'
            'firefox-25.0a1.pt-PT.win32.installer.exe'},
    # -a firefox -p win32 --branch=mozilla-central --date=2013-07-23
    {'args': {'application': 'firefox',
              'branch': 'mozilla-central',
              'date': '2013-07-23',
              'platform': 'win32'},
     'filename': '1374583608-mozilla-central-firefox-25.0a1.en-US.win32.installer.exe',
     'url': 'firefox/tinderbox-builds/mozilla-central-win32/'
            '1374583608/firefox-25.0a1.en-US.win32.installer.exe'},
    # -a firefox -p win32 --branch=mozilla-central --date=2013-07-23 --build-number=1
    {'args': {'application': 'firefox',
              'branch': 'mozilla-central',
              'build_number': '1',
              'date': '2013-07-23',
              'platform': 'win32'},
     'filename': '1374568307-mozilla-central-firefox-25.0a1.en-US.win32.installer.exe',
     'url': 'firefox/tinderbox-builds/mozilla-central-win32/'
            '1374568307/firefox-25.0a1.en-US.win32.installer.exe'},
    # -a firefox -p win32 --branch=mozilla-central --date=1374573725
    {'args': {'application': 'firefox',
              'branch': 'mozilla-central',
              'date': '1374573725',
              'platform': 'win32'},
     'filename': '1374573725-mozilla-central-firefox-25.0a1.en-US.win32.installer.exe',
     'url': 'firefox/tinderbox-builds/mozilla-central-win32/'
            '1374573725/firefox-25.0a1.en-US.win32.installer.exe'},
    # -a firefox -p win32 --branch=mozilla-inbound
    {'args': {'application': 'firefox',
              'branch': 'mozilla-inbound',
              'platform': 'win32'},
     'filename': '1374583608-mozilla-inbound-firefox-25.0a1.en-US.win32.installer.exe',
     'url': 'firefox/tinderbox-builds/mozilla-inbound-win32/'
            '1374583608/firefox-25.0a1.en-US.win32.installer.exe'},
    # -a firefox -t tinderbox -p linux --branch=mozilla-central --extension=txt
    {'args': {'application': 'firefox',
              'branch': 'mozilla-central',
              'extension': 'txt',
              'platform': 'linux'},
     'filename': '1374583608-mozilla-central-firefox-25.0a1.en-US.linux-i686.txt',
     'url': 'firefox/tinderbox-builds/mozilla-central-linux/'
            '1374583608/firefox-25.0a1.en-US.linux-i686.txt'},
    # -a firefox -t tinderbox -p win32 --extension=txt
    {'args': {'application': 'firefox',
              'extension': 'txt',
              'platform': 'win32'},
     'filename': '1374568307-mozilla-central-firefox-25.0a1.en-US.win32.txt',
     'url': 'firefox/tinderbox-builds/mozilla-central-win32/'
            '1374568307/firefox-25.0a1.en-US.win32.txt'},
    # -a firefox -t tinderbox -p mac --extension=txt
    {'args': {'application': 'firefox',
              'extension': 'txt',
              'platform': 'mac'},
     'filename': '1374568307-mozilla-central-firefox-25.0a1.en-US.mac.txt',
     'url': 'firefox/tinderbox-builds/mozilla-central-macosx64/'
            '1374568307/firefox-25.0a1.en-US.mac.txt'},
]

thunderbird_tests = [
    # -a thunderbird -p linux --branch=comm-central
    {'args': {'application': 'thunderbird',
              'branch': 'comm-central',
              'platform': 'linux'},
     'filename': '1380362686-comm-central-thunderbird-27.0a1.en-US.linux-i686.tar.bz2',
     'url': 'thunderbird/tinderbox-builds/comm-central-linux/'
            '1380362686/thunderbird-27.0a1.en-US.linux-i686.tar.bz2'},
    # -a thunderbird -p linux64 --branch=comm-central
    {'args': {'application': 'thunderbird',
              'branch': 'comm-central',
              'platform': 'linux64'},
     'filename': '1380362686-comm-central-thunderbird-27.0a1.en-US.linux-x86_64.tar.bz2',
     'url': 'thunderbird/tinderbox-builds/comm-central-linux64/'
            '1380362686/thunderbird-27.0a1.en-US.linux-x86_64.tar.bz2'},
    # -a thunderbird -p mac64 --branch=comm-central
    {'args': {'application': 'thunderbird',
              'branch': 'comm-central',
              'platform': 'mac64'},
     'filename': '1380362686-comm-central-thunderbird-27.0a1.en-US.mac.dmg',
     'url': 'thunderbird/tinderbox-builds/comm-central-macosx64/'
            '1380362686/thunderbird-27.0a1.en-US.mac.dmg'},
    # -a thunderbird -p win32 --branch=comm-central
    {'args': {'application': 'thunderbird',
              'branch': 'comm-central',
              'platform': 'win32'},
     'filename': '1380362686-comm-central-thunderbird-27.0a1.en-US.win32.installer.exe',
     'url': 'thunderbird/tinderbox-builds/comm-central-win32/'
            '1380362686/thunderbird-27.0a1.en-US.win32.installer.exe'},
    # -a thunderbird -p win64 --branch=comm-central
    {'args': {'application': 'thunderbird',
              'branch': 'comm-central',
              'platform': 'win64'},
     'filename': '1380362686-comm-central-thunderbird-27.0a1.en-US.win64-x86_64.installer.exe',
     'url': 'thunderbird/tinderbox-builds/comm-central-win64/'
            '1380362686/thunderbird-27.0a1.en-US.win64-x86_64.installer.exe'},
    # -a thunderbird -p win32 --branch=comm-central --debug-build
    {'args': {'application': 'thunderbird',
              'branch': 'comm-central',
              'debug_build': True,
              'platform': 'win32'},
     'filename': '1380362686-comm-central-debug-thunderbird-27.0a1.en-US.win32.installer.exe',
     'url': 'thunderbird/tinderbox-builds/comm-central-win32-debug/'
            '1380362686/thunderbird-27.0a1.en-US.win32.installer.exe'},
    # -a thunderbird -p win32 --branch=comm-central -l de
    {'args': {'application': 'thunderbird',
              'branch': 'comm-central',
              'locale': 'de',
              'platform': 'win32'},
     'filename': 'comm-central-thunderbird-27.0a1.de.win32.installer.exe',
     'url': 'thunderbird/tinderbox-builds/comm-central-l10n/'
            'thunderbird-27.0a1.de.win32.installer.exe'},
    # -a thunderbird -p win32 --branch=comm-central -l pt-PT
    {'args': {'application': 'thunderbird',
              'branch': 'comm-central',
              'locale': 'pt-PT',
              'platform': 'win32'},
     'filename': 'comm-central-thunderbird-27.0a1.pt-PT.win32.installer.exe',
     'url': 'thunderbird/tinderbox-builds/comm-central-l10n/'
            'thunderbird-27.0a1.pt-PT.win32.installer.exe'},
    # -a thunderbird -p win32 --branch=comm-central --date=2013-09-28
    {'args': {'application': 'thunderbird',
              'branch': 'comm-central',
              'date': '2013-09-28',
              'platform': 'win32'},
     'filename': '1380362686-comm-central-thunderbird-27.0a1.en-US.win32.installer.exe',
     'url': 'thunderbird/tinderbox-builds/comm-central-win32/'
            '1380362686/thunderbird-27.0a1.en-US.win32.installer.exe'},
    # -a thunderbird -p win32 --branch=comm-central --date=2013-07-24 --build-number=1
    {'args': {'application': 'thunderbird',
              'branch': 'comm-central',
              'build_number': '1',
              'date': '2013-09-28',
              'platform': 'win32'},
     'filename': '1380362527-comm-central-thunderbird-27.0a1.en-US.win32.installer.exe',
     'url': 'thunderbird/tinderbox-builds/comm-central-win32/'
            '1380362527/thunderbird-27.0a1.en-US.win32.installer.exe'},
    # -a thunderbird -p win32 --branch=comm-central --date=1380362527
    {'args': {'application': 'thunderbird',
              'branch': 'comm-central',
              'date': '1380362527',
              'platform': 'win32'},
     'filename': '1380362527-comm-central-thunderbird-27.0a1.en-US.win32.installer.exe',
     'url': 'thunderbird/tinderbox-builds/comm-central-win32/'
            '1380362527/thunderbird-27.0a1.en-US.win32.installer.exe'},
    # -a thunderbird -p win32 --branch=comm-aurora
    {'args': {'application': 'thunderbird',
              'branch': 'comm-aurora',
              'platform': 'win32'},
     'filename': '1380362686-comm-aurora-thunderbird-27.0a1.en-US.win32.installer.exe',
     'url': 'thunderbird/tinderbox-builds/comm-aurora-win32/'
            '1380362686/thunderbird-27.0a1.en-US.win32.installer.exe'}
]

tests = firefox_tests + thunderbird_tests


class TinderboxScraperTest(mhttpd.MozHttpdBaseTest):
    """test mozdownload TinderboxScraper class"""

    def test_scraper(self):
        """Testing various download scenarios for TinderboxScraper"""

        for entry in tests:
            scraper = TinderboxScraper(destination=self.temp_dir,
                                       base_url=self.wdir,
                                       logger=self.logger,
                                       **entry['args'])
            expected_filename = os.path.join(self.temp_dir, entry['filename'])
            self.assertEqual(scraper.filename, expected_filename)
            self.assertEqual(urllib.unquote(scraper.url),
                             urljoin(self.wdir, entry['url']))


if __name__ == '__main__':
    unittest.main()
