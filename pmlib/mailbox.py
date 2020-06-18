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

from typing import List

import pmlib

from pmlib.hierachy import Hierarchy
from pmlib.types import TypeFolder, Position
from pmlib.item import Item


class Mailbox(object):

    def __init__(self, root: str):
        self.root: str = root
        self.hierarchy: Hierarchy = Hierarchy()
        self.folder: List[Item] = []
        return

    def init(self, folder: str, filename=None) -> bool:
        count = self.hierarchy.parse(folder, self.root)
        if count == 0:
            return False

        self.hierarchy.sort(self.folder)

        if filename is not None:
            self.hierarchy.export_json(filename)

        return True

    def _open_pegasus(self, item: Item) -> bool:
        pmlib.log.inform("Folder", "Open {0:s}".format(item.name))

        positions = []

        f = open(item.data.filename, mode='rb')
        byte = f.seek(128)  # move to first mail

        n = 0
        count = 1

        stream = f.read(-1)
        f.close()

        pmlib.log.inform(item.name, "Size: {0:d}".format(len(stream)))

        start = 0
        for byte in stream:
            if byte == 0x1a:  # 1A seperates the mails
                pos = Position(start=start, end=n)
                positions.append(pos)
                count += 1
                start = n + 1
            n += 1

        pmlib.log.inform(item.name, "Count {0:d}".format(len(positions)))

        for _pos in positions:
            value = stream[_pos.start:_pos.end]
            item.mails.append(value)

        return True

    def open(self) -> bool:

        for item in self.folder:
            if item.data.type is TypeFolder.pegasus:
                check = self._open_pegasus(item)
                if check is False:
                    return False

        return True
