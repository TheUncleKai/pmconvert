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
from typing import Union

import pmlib
import pmlib.log

from pmlib import config
from pmlib.mailbox import Mailbox
from pmlib.utils import create_folder


class Console(object):

    def __init__(self):

        self.mailbox: Union[Mailbox, None] = None

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
        self.parser.add_option("-t", "--target", help="target path for export", type="string", metavar="<FOLDER>",
                               default="")
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

        self.mailbox = Mailbox()
        return True

    def run(self) -> bool:
        check = self.mailbox.init()
        if check is False:
            return False

        check = self.mailbox.convert()
        if check is False:
            return False

        return True

    def close(self) -> bool:

        check = True
        # check = self.mailbox.report()
        return check
