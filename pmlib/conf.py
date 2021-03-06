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

import pmlib

from dataclasses import dataclass
from pmlib.types import Target


@dataclass(init=False)
class Config(object):

    verbose: int = 0
    pegasus_path: str = ""
    pegasus_root: str = ""
    target_type: Target = Target.unknown
    target_path: str = ""
    no_convert: bool = False

    def parse(self, options) -> bool:

        if os.path.exists(options.folder) is False:
            pmlib.log.error("Unable to find Pegasus user folder: {0:s}".format(options.folder_list))
            return False

        if options.root == "":
            pmlib.log.error("Need to give a Pegasus Root Mailbox name!")
            return False

        self.pegasus_root = options.root
        self.pegasus_path = options.folder
        self.no_convert = options.noconvert

        if options.target == "":
            pmlib.log.error("Need to give target path!")
            return False

        self.target_path = os.path.abspath(os.path.normpath(options.target))

        if options.export == "mbox":
            self.target_type = Target.mbox

        if options.export == "maildir":
            self.target_type = Target.maildir

        if self.target_type is Target.unknown:
            pmlib.log.error("Invalid export format: {0:s}".format(options.export))
            return False

        self.verbose = int(options.verbose)

        return True
