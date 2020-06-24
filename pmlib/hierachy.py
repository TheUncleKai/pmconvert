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
from typing import Union, List, Dict

import pmlib

from pmlib.item import Item
from pmlib.types import Entry, Counter

__all__ = [
    "Hierarchy"
]


def _sort_name(item: Item):
    return item.name


class Hierarchy(object):

    def __init__(self):

        self.root: Union[Item, None] = None
        self.counter = Counter()
        self.entries: List[Item] = []

        self.index: Dict[int, Item] = {}
        self.tray: Dict[int, Item] = {}
        self.root: Union[Item, None] = None
        self.level: int = 0
        return

    def parse(self) -> bool:
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
                self.root = data
            self.entries.append(data)
        f.close()

        count = len(self.entries)

        if self.root is None:
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
            for _item in sorted(item.children, key=_sort_name):
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
    def _count(item: Item) -> Counter:
        counter = Counter()

        if item.type is Entry.folder:
            return counter

        for _item in sorted(item.children, key=_sort_name):
            if _item.type is Entry.folder:
                counter.inc_folder()

        for _item in sorted(item.children, key=_sort_name):
            if _item.type is Entry.tray:
                counter.inc_tray()

        return counter

    def _index(self, item: Item):

        item.navigation.index = self.counter.index
        self.counter.inc_index()

        item.navigation.children = len(item.children)

        max_counter = self._count(item)
        counter = Counter()

        if item.type is not Entry.folder:
            item.navigation.tray = self.counter.tray
            self.counter.inc_tray()
            self.tray[item.navigation.tray] = item

        for _item in sorted(item.children, key=_sort_name):
            if _item.type is Entry.folder:
                counter.inc_folder()
                _item.navigation.level = item.navigation.level
                _item.navigation.count = max_counter.folder
                _item.navigation.number = counter.folder
                self._index(_item)

        for _item in sorted(item.children, key=_sort_name):
            if _item.type is Entry.tray:
                counter.inc_tray()
                _item.navigation.level = item.navigation.level + 1
                _item.navigation.count = max_counter.tray
                _item.navigation.number = counter.tray
                self._index(_item)
        return

    def sort(self, folder_list: List[Item]):
        self.root.navigation.level = 1
        self.root.populate(self.entries)

        for _item in self.entries:
            _item.populate(self.entries)

        self._add_folder(folder_list, self.root)

        self._index(self.root)

        for _item in self.entries:
            self.index[_item.navigation.index] = _item
            if _item.navigation.level > self.level:
                self.level = _item.navigation.level
        return
