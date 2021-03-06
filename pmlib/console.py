#!/usr/bin/python3
# -*- coding: utf-8 -*-
#
#    Licensed under the Apache License, Version 2.0 (the "License");
#    you may not use this file except in compliance with the License.
#    You may obtain a copy of the License at
#
#        http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS,
#    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#    See the License for the specific language governing permissions and
#    limitations under the License.
#
#    Copyright (C) 2017, Kai Raphahn <kai.raphahn@laburec.de>
#

from optparse import OptionParser

import pmlib

from pmlib import config

from pmlib.hierachy import Hierarchy
from pmlib.utils import create_folder
from pmlib.report import Report

_filter = [
    "WINRULEA.PMC",
    "WINRULES.PMC"
]


class Console(object):

    def __init__(self):
        usage = "usage: %prog [options] arg1 arg2"
        self.parser: OptionParser = OptionParser(usage=usage)
        self.parser.add_option("-v", "--verbose", help="run verbose level [0..3]", type="int", metavar="1",
                               default=0)
        self.parser.add_option("-f", "--folder", help="pegasus mail folder", type="string", metavar="<FOLDER>",
                               default="")
        self.parser.add_option("-r", "--root", help="pegasus mail root mailbox", type="string", metavar="<MAILBOX>",
                               default="My mailbox")
        self.parser.add_option("-x", "--export", help="type for data export", type="string", metavar="mbox|maildir",
                               default="mbox")

        self.parser.add_option("-s", "--source", help="target path for export", type="string", metavar="<FOLDER>",
                               default="")

        self.parser.add_option("-t", "--target", help="target path for export", type="string", metavar="<FOLDER>",
                               default="")

        self.parser.add_option("-n", "--noconvert", help="target path for export", action="store_true",
                               default=False)
        return

    def prepare(self) -> bool:
        (options, args) = self.parser.parse_args()

        check = config.parse(options)
        if check is False:
            return False

        pmlib.log.setup(level=config.verbose)

        pmlib.log.inform("Mail folder", "{0:s}".format(config.pegasus_path))
        pmlib.log.inform("Root Mailbox", "{0:s}".format(config.pegasus_root))
        pmlib.log.inform("Target folder", "{0:s}".format(config.target_path))

        check = create_folder(config.target_path)
        if check is False:
            pmlib.log.error("Unable to create target folder!")
            return False

        return True

    @staticmethod
    def run() -> bool:
        hierarchy = Hierarchy()

        count = hierarchy.parse()
        if count == 0:
            return False

        hierarchy.sort()

        for _item in _filter:
            check = pmlib.data.filter.parse(_item)
            if check is False:
                return False

        lfilter = pmlib.data.filter

        item = pmlib.data.root

        target = pmlib.manager.get_target(pmlib.config.target_type)
        if target is None:
            text = "Unable to find converter with type {0:s}".format(pmlib.config.target_type.name)
            pmlib.log.warn("Mailbox", text)
            return False

        if config.no_convert is True:
            return True

        check = target.prepare(item)
        if check is False:
            return False

        check = target.run()
        if check is False:
            return False

        check = target.close()
        if check is False:
            return False

        return True

    @staticmethod
    def close() -> bool:

        report = Report()

        report.init()

        for _report in report.modules:
            pmlib.log.inform(_report.name, _report.desc)
            check = _report.create()
            if check is False:
                return False

        return True
