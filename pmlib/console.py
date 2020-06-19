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
from typing import Union

import pmlib
from pmlib.mailbox import Mailbox
from pmlib.types import ExportFormat
from pmlib.utils import create_folder


class Console(object):

    def __init__(self):

        self.options = None
        self.folder: str = ""
        self.root: str = ""
        self.hierachy_file: str = ""
        self.target: str = ""
        self.export: ExportFormat = ExportFormat.unknown

        self.mailbox: Union[Mailbox, None] = None

        usage = "usage: %prog [options] arg1 arg2"
        self.parser: OptionParser = OptionParser(usage=usage)
        self.parser.add_option("-v", "--verbose", help="run verbose level [0..3]", type="int", metavar="1",
                               default=0)
        self.parser.add_option("-f", "--folder", help="pegasus mail folder", type="string", metavar="<FOLDER>",
                               default="")
        self.parser.add_option("-r", "--root", help="pegasus mail root mailbox", type="string", metavar="<MAILBOX>",
                               default="My mailbox")
        self.parser.add_option("-a", "--hierachy", help="hierachy json file", type="string", metavar="<FILENAME>",
                               default=None)
        self.parser.add_option("-x", "--export", help="hierachy json file", type="string", metavar="mbox|maildir",
                               default="mbox")
        self.parser.add_option("-t", "--target", help="export target path", type="string", metavar="<FOLDER>",
                               default="")
        return

    def prepare(self) -> bool:
        (options, args) = self.parser.parse_args()
        self.options = options

        if os.path.exists(options.folder) is False:
            pmlib.log.error("Unable to find mail folder: {0:s}".format(options.folder))
            return False

        if options.target == "":
            pmlib.log.error("Need to give target path!")
            return False

        if options.export == "mbox":
            self.export = ExportFormat.mbox

        if options.export == "maildir":
            self.export = ExportFormat.maildir

        if self.export is ExportFormat.unknown:
            pmlib.log.error("Invalid export format: {0:s}".format(options.export))
            return False

        pmlib.log.setup(level=options.verbose)

        self.folder = options.folder
        self.root = options.root
        self.hierachy_file = options.hierachy
        self.target = os.path.abspath(os.path.normpath(options.target))

        pmlib.log.inform("Mail folder", "{0:s}".format(self.folder))
        pmlib.log.inform("Root Mailbox", "{0:s}".format(self.root))
        pmlib.log.inform("Target folder", "{0:s}".format(self.target))
        if self.hierachy_file:
            pmlib.log.inform("Hierachy file", "{0:s}".format(self.hierachy_file))

        check = create_folder(self.target)
        if check is False:
            pmlib.log.error("Unable to create target folder!")
            return False

        self.mailbox = Mailbox(self.root, self.target)
        return True

    def run(self) -> bool:
        check = self.mailbox.init(self.folder)
        if check is False:
            return False

        check = self.mailbox.convert(self.export)
        if check is False:
            return False

        return True

    def close(self) -> bool:
        return True
