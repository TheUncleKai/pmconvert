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
from typing import List

import pmlib
import pmlib.log

from pmlib.item import Item, sort_items
from pmlib.types import Entry, Counter

__all__ = [
    "Hierarchy"
]


class Hierarchy(object):

    def __init__(self):
        self.counter = Counter()
        return

    @staticmethod
    def parse() -> bool:
        filename = os.path.abspath(os.path.normpath("{0:s}/HIERARCH.PM".format(pmlib.config.pegasus_path)))
        if os.path.exists(filename) is False:
            pmlib.log.error("Unable to find HIERARCH.PM")
            return False

        pmlib.log.inform("Hierarchy", "Open {0:s}".format(filename))

        f = open(filename, mode='r')
        for line in f:
            data = Item(line)
            if data.valid is False:
                continue
            if data.name == pmlib.config.pegasus_root:
                data.is_root = True
                pmlib.data.root = data
            pmlib.data.entries.append(data)
        f.close()

        count = len(pmlib.data.entries)

        if pmlib.data.root is None:
            pmlib.log.warn("Hierarchy", "No root found!")
            return False

        if count == 0:
            pmlib.log.warn("Hierarchy", "No entries found!")
            return False

        pmlib.log.inform("Hierarchy", "{0:d} entries found!".format(count))
        return True

    def _write_entry(self, root: list, item: Item):

        if item.type is Entry.folder:
            root.append(item.name)
        else:
            content = []
            for _item in sorted(item.children, key=sort_items):
                self._write_entry(content, _item)
            root.append({item.name: content})
        return

    def _add_folder(self, folder: List[Item], item: Item):
        if item.type is Entry.folder:
            folder.append(item)
            return

        if len(item.children) != 0:
            for _item in item.children:
                self._add_folder(folder, _item)
        return

    @staticmethod
    def _count_item(level: int, counter: Counter, item: Item, max_count: int):
        item.navigation.level = level + 1
        item.navigation.count = max_count
        item.navigation.number = counter.item
        if item.navigation.number == (max_count - 1):
            item.navigation.is_last = True
        counter.inc_item()
        return

    def _index(self, item: Item):

        self.counter.inc_index()

        max_count = len(item.children)
        counter = Counter()

        if item.type is not Entry.folder:
            self.counter.inc_tray()

        for _item in sorted(item.children, key=sort_items):
            if _item.type is Entry.folder:
                self._count_item(item.navigation.level, counter, _item, max_count)
                self._index(_item)

        for _item in sorted(item.children, key=sort_items):
            if _item.type is Entry.tray:
                self._count_item(item.navigation.level, counter, _item, max_count)
                self._index(_item)
        return

    def sort(self):
        root: Item = pmlib.data.root

        root.navigation.level = 0
        root.navigation.is_last = True
        root.populate(pmlib.data.entries)

        for _item in pmlib.data.entries:
            _item.populate(pmlib.data.entries)

        self._index(root)

        for _item in pmlib.data.entries:
            if _item.navigation.level > pmlib.data.level:
                pmlib.data.level = _item.navigation.level
        return
