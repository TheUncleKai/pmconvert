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
from typing import Union, List

import pmlib

from pmlib.hierachy.entry import Entry

__all__ = [
    "entry",
    "types",

    "Hierarchy"
]


class Hierarchy(object):

    def __init__(self):

        self.count: int = 0
        self.entries: List[Entry] = []
        self.root: Union[Entry, None] = None
        return

    def parse(self, folder: str) -> bool:
        filename = os.path.abspath(os.path.normpath("{0:s}/HIERARCH.PM".format(folder)))
        if os.path.exists(filename) is False:
            pmlib.log.error("Unable to find HIERARCH.PM")
            return False

        pmlib.log.inform("Hierarchy", "Open {0:s}".format(filename))

        f = open(filename, mode='r')
        for line in f:
            data = Entry()
            check = data.parse(line)
            if check is False:
                continue
            self.entries.append(data)
            data.show()
            self.count += 1
        f.close()

        if self.count == 0:
            pmlib.log.warn("Hierarchy", "No entries found!")
            return False

        pmlib.log.inform("Hierarchy", "{0:d} entries found!".format(self.count))
        return True
