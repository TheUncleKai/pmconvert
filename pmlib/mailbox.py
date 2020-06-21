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

from pmlib.convert import Convert
from pmlib.hierachy import Hierarchy
from pmlib.types import Entry, Target
from pmlib.item import Item
from pmlib.utils import create_folder


def _sort_name(item: Item):
    return item.name


class Mailbox(object):

    def __init__(self, root: str, target: str):
        self._conv: Convert = Convert()

        self.target: str = target
        self.root: str = root
        self.hierarchy: Hierarchy = Hierarchy()
        self.folder: List[Item] = []
        self.export: Target = Target.unknown
        return

    def init(self, folder: str, filename=None) -> bool:
        self._conv.init()

        count = self.hierarchy.parse(folder, self.root)
        if count == 0:
            return False

        self.hierarchy.sort(self.folder)

        if filename is not None:
            self.hierarchy.export_json(filename)

        return True

    def _create_folder(self, item: Item) -> bool:
        item.set_target(self.target)

        if item.type is Entry.folder:
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

    def _convert(self, item: Item) -> bool:
        converter = self._conv.get_converter(item.data.type, self.export)
        if converter is None:
            pmlib.log.error(
                "Unable to convert folder {0:s} with type {1:s} to {2:s}".format(item.name, item.data.type.name,
                                                                                 self.export.name))
            return False

        check = converter.prepare(item)
        if check is False:
            return False

        check = converter.run()
        if check is False:
            return False

        check = converter.close()
        if check is False:
            return False

        return True

    def _export(self, item: Item) -> bool:

        if item.type is Entry.folder:
            check = self._convert(item)
            if check is False:
                return False
        else:
            pmlib.log.inform("TRAY", item.name)

            for _item in sorted(item.children, key=_sort_name):
                check = self._export(_item)
                if check is False:
                    return False

        return True

    def convert(self, export: Target) -> bool:
        self.export = export
        check = self._create_folder(self.hierarchy.root)
        if check is False:
            return False

        check = self._export(self.hierarchy.root)
        if check is False:
            return False

        return True
