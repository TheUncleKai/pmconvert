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
from pmlib.types import Entry
from pmlib.item import Item
from pmlib.utils import create_folder


def _sort_name(item: Item):
    return item.name


class Mailbox(object):

    def __init__(self):
        self._conv: Convert = Convert()

        self.hierarchy: Hierarchy = Hierarchy()
        self.folder_list: List[Item] = []
        return

    def init(self) -> bool:
        self._conv.init()

        count = self.hierarchy.parse()
        if count == 0:
            return False

        self.hierarchy.sort(self.folder_list)
        return True

    def _create_folder(self, item: Item) -> bool:
        item.set_target()

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
        attr = self._conv.get_converter(item.data.type)
        if attr is None:
            text = "Unable to convert folder {0:s} with type {1:s} to {2:s}".format(item.name,
                                                                                    item.data.type.name,
                                                                                    pmlib.config.target_type.name)
            pmlib.log.warn("Mailbox", text)
            return True

        converter = attr()
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
            pmlib.log.inform("TRAY", item.full_name)

            # first convert folder
            for _item in sorted(item.children, key=_sort_name):
                if _item.type is Entry.folder:
                    check = self._export(_item)
                    if check is False:
                        return False

            # then trays
            for _item in sorted(item.children, key=_sort_name):
                if _item.type is not Entry.folder:
                    check = self._export(_item)
                    if check is False:
                        return False

        return True

    def convert(self) -> bool:
        check = self._create_folder(self.hierarchy.root)
        if check is False:
            return False

        check = self._export(self.hierarchy.root)
        if check is False:
            return False

        return True

    def report(self) -> bool:
        return True
