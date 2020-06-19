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

from pmlib.item import Item
from pmlib.types import TypeEntry
import json

__all__ = [
    "Hierarchy"
]


def _sort_name(item: Item):
    return item.name


class Hierarchy(object):

    def __init__(self):

        self.root: Union[Item, None] = None
        self.count: int = 0
        self.entries: List[Item] = []
        self.root: Union[Item, None] = None
        return

    def parse(self, folder: str, root: str) -> bool:
        filename = os.path.abspath(os.path.normpath("{0:s}/HIERARCH.PM".format(folder)))
        if os.path.exists(filename) is False:
            pmlib.log.error("Unable to find HIERARCH.PM")
            return False

        pmlib.log.inform("Hierarchy", "Open {0:s}".format(filename))

        f = open(filename, mode='r')
        for line in f:
            data = Item(line, folder)
            if data.valid is False:
                continue
            if data.name == root:
                data.is_root = True
                self.root = data
            self.entries.append(data)
            self.count += 1
        f.close()

        if self.root is None:
            pmlib.log.warn("Hierarchy", "No root found!")
            return False

        if self.count == 0:
            pmlib.log.warn("Hierarchy", "No entries found!")
            return False

        pmlib.log.inform("Hierarchy", "{0:d} entries found!".format(self.count))
        return True

    def _write_entry(self, root: list, item: Item):

        if item.type is TypeEntry.folder:
            root.append(item.name)
        else:
            content = []
            for _item in sorted(item.children, key=_sort_name):
                self._write_entry(content, _item)
            root.append({item.name: content})

        return

    def export_json(self, filename: str):
        root = []

        self._write_entry(root, self.root)

        file = os.path.abspath(os.path.normpath(filename))
        pmlib.log.inform("Hierarchy", "Export hierarchy to {0:s}".format(file))

        f = open(file, mode="w")
        json.dump(root, f, indent=4)
        f.close()
        return

    def _add_folder(self, folder: List[Item], item: Item):
        if item.type is TypeEntry.folder:
            folder.append(item)
            return

        if len(item.children) != 0:
            for _item in item.children:
                self._add_folder(folder, _item)
        return

    def sort(self, folder: List[Item]):
        self.root.populate(self.entries)

        for _item in self.entries:
            _item.populate(self.entries)

        self._add_folder(folder, self.root)
        return
