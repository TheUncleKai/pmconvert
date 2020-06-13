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

import os
from optparse import OptionParser

import pmlib
from pmlib.hierachy import Hierarchy


class Console(object):

    def __init__(self):

        self.options = None
        self.folder: str = ""
        self.root: str = ""

        self.hierarchy: Hierarchy = Hierarchy()

        usage = "usage: %prog [options] arg1 arg2"
        self.parser: OptionParser = OptionParser(usage=usage)
        self.parser.add_option("-v", "--verbose", help="run verbose level [0..3]", metavar="1", type="int",
                               default=0)
        self.parser.add_option("-f", "--folder", help="pegasus mail folder", type="string", default="")
        self.parser.add_option("-r", "--root", help="pegasus mail root mailbox", type="string", default="My mailbox")
        return

    def prepare(self) -> bool:
        (options, args) = self.parser.parse_args()
        self.options = options

        if os.path.exists(options.folder) is False:
            pmlib.log.error("Unable to find mail folder: {0:s}".format(options.folder))
            return False

        self.folder = options.folder
        self.root = options.root
        pmlib.log.inform("Mail folder", "{0:s}".format(self.folder))
        return True

    def run(self) -> bool:
        count = self.hierarchy.parse(self.folder, self.root)
        if count == 0:
            return False

        self.hierarchy.sort()

        return True

    def close(self) -> bool:
        return True
