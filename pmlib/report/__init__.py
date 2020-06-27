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

__all__ = [
    "html",
    "excel",

    "Symbol",
    "Reporter",
    "Report"
]

import abc
from abc import ABCMeta
from enum import Enum
from typing import List

import pmlib

from pmlib.item import Item
from bbutil.utils import get_attribute
from pmlib.types import Entry


class Symbol(Enum):

    root = 0
    tray = 1
    horizontal = 2
    vertical = 3
    last = 4
    child = 5
    mailbox = 6
    envelope = 7
    folder = 8
    space = 9


class Reporter(metaclass=ABCMeta):

    def __init__(self):
        self.root: Item = pmlib.data.root
        self.name: str = ""
        self.desc: str = ""
        return

    @abc.abstractmethod
    def format_symbol(self, symbol: Symbol, item: Item) -> str:
        pass

    def _set_parent_symbols(self, work_item: Item, parent: Item, child: Item):

        if parent is None:
            return

        level = parent.navigation.level

        if work_item.parent is parent:
            if work_item.navigation.is_last is False:
                work_item.symbols[level] = self.get_symbol(Symbol.child)
            else:
                work_item.symbols[level] = self.get_symbol(Symbol.last)

        else:
            if parent.navigation.is_last is True:
                if child.navigation.is_last is False:
                    work_item.symbols[level] = self.get_symbol(Symbol.vertical)
            else:
                if child.navigation.is_last is False:
                    work_item.symbols[level] = self.get_symbol(Symbol.vertical)

        self._set_parent_symbols(work_item, parent.parent, parent)
        return

    def set_symbol(self, item: Item):
        level = item.navigation.level

        if item.is_root is True:
            item.symbols[level + 1] = self.format_symbol(Symbol.mailbox, item)
            item.symbols[0] = self.get_symbol(Symbol.root)
            return

        if item.type is Entry.tray:
            item.symbols[level + 1] = self.format_symbol(Symbol.folder, item)
            item.symbols[level] = self.get_symbol(Symbol.tray)

        if item.type is Entry.folder:
            item.symbols[level + 1] = self.format_symbol(Symbol.envelope, item)
            item.symbols[level] = self.get_symbol(Symbol.horizontal)

        self._set_parent_symbols(item, item.parent, item)
        return

    @abc.abstractmethod
    def get_symbol(self, symbol: Symbol) -> str:
        pass

    @abc.abstractmethod
    def create(self) -> bool:
        pass


_reporter = [
    "html",
    "excel"
]


class Report(object):

    def __init__(self):
        self.modules: List[Reporter] = []
        return

    def init(self):
        for _item in _reporter:
            path = "pmlib.report.{0:s}".format(_item)
            name = get_attribute(path, "report")
            attr = get_attribute(path, name)
            c = attr()
            self.modules.append(c)
        return
