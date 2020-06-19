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

import mailbox
import email

import pmlib

from pmlib.hierachy import Hierarchy
from pmlib.types import TypeFolder, TypeEntry, Position, ExportFormat
from pmlib.item import Item
from pmlib.utils import create_folder


class Mailbox(object):

    def __init__(self, root: str, target: str):
        self.target: str = target
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

    @staticmethod
    def _open_pegasus(item: Item) -> bool:
        pmlib.log.inform("Folder", "Open {0:s}".format(item.name))

        positions = []

        f = open(item.data.filename, mode='rb')
        f.seek(128)  # move to first mail

        n = 0
        count = 1

        stream = f.read(-1)
        f.close()

        item.size = len(stream)
        pmlib.log.debug1(item.name, "Size: {0:d}".format(item.size))

        start = 0
        for byte in stream:
            if byte == 0x1a:  # 1A seperates the mails
                pos = Position(start=start, end=n)
                positions.append(pos)
                count += 1
                start = n + 1
            n += 1

        pmlib.log.debug1("EXPORT", "Count {0:s}: {1:d}".format(item.name, len(positions)))

        for _pos in positions:
            value = stream[_pos.start:_pos.end]
            item.mails.append(value)

        item.count = len(item.mails)
        return True

    @staticmethod
    def _export_mbox(item: Item) -> bool:
        path = "{0:s}.mbx".format(item.target)
        mbox = mailbox.mbox(path)
        mbox.lock()

        pmlib.log.inform("EXPORT", "Export {0:s} with {1:d} (2:d)".format(path, item.count, item.size))
        for _data in item.mails:
            msg = email.message_from_bytes(_data)
            mbox.add(msg)
            mbox.flush()

        mbox.unlock()
        return True

    def _export_maildir(self, item: Item) -> bool:
        pass

    def _convert(self, item: Item, export: ExportFormat) -> bool:
        check = self._open_pegasus(item)
        if check is False:
            return False

        if export is ExportFormat.mbox:
            check = self._export_mbox(item)
            if check is False:
                return False

        if export is ExportFormat.maildir:
            check = self._export_maildir(item)
            if check is False:
                return False

        return True

    def _create_folder(self, item: Item) -> bool:
        item.set_target(self.target)

        if item.type is TypeEntry.folder:
            return True

        check = create_folder(item.target)
        if check is False:
            pmlib.log.error("Unable to create target folder: {0:s}".format(item.target))
            return False

        for _item in item.children:
            check = self._create_folder(_item)
            if check is False:
                return False

        return True

    def _export(self, item: Item, export: ExportFormat) -> bool:

        if item.type is TypeEntry.folder:
            check = self._convert(item, export)
            if check is False:
                return False
        else:
            pmlib.log.inform("TRAY", item.name)

            for _item in item.children:
                check = self._export(_item, export)
                if check is False:
                    return False

        return True

    def convert(self, export: ExportFormat) -> bool:
        check = self._create_folder(self.hierarchy.root)
        if check is False:
            return False

        check = self._export(self.hierarchy.root, export)
        if check is False:
            return False

        return True
