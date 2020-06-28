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
import re
from typing import List, Dict
from dataclasses import dataclass, field

import pmlib
import pmlib.log

from pmlib.types import Source, Entry, Folder, Object, EntryData, ErrorReport, EntryReport, Navigation

from pmlib.utils import get_entry_type


_entry = re.compile("(?P<Type>[0-9]+),(?P<State>[0-9]+),\"(?P<Data>.+)\",\"(?P<Parent>.*)\",\"(?P<Name>.*)\"")
_object = re.compile("(?P<ID>.+):(?P<Name>.+)")
_folder = re.compile("(?P<ID>.+):(?P<Folder>.+):(?P<Name>.+)")

__all__ = [
    "Item",
    "sort_items",
    "Data"
]


class Item(EntryData):

    def __repr__(self):
        return self.name

    def _check_folder(self) -> bool:
        if self.data is None:
            pmlib.log.error("No folder object found!")
            return False

        root = pmlib.config.pegasus_path

        filename = os.path.normpath("{0:s}/{1:s}.PMM".format(root, self.data.name))
        if os.path.exists(filename):
            self.data.type = Source.pegasus
            self.data.filename = filename

        filename = os.path.normpath("{0:s}/{1:s}.MBX".format(root, self.data.name))
        if os.path.exists(filename):
            self.data.type = Source.unix
            self.data.filename = filename

        if self.data.type is Source.unix:
            filename = os.path.normpath("{0:s}/{1:s}.PMG".format(root, self.data.name))
            if os.path.exists(filename):
                self.data.indexname = filename
            else:
                pmlib.log.warn(self.data.name, "Folder index not found or unknown!")
                return False

        if self.data.type is Source.pegasus:
            filename = os.path.normpath("{0:s}/{1:s}.PMI".format(root, self.data.name))
            if os.path.exists(filename):
                self.data.indexname = filename
            else:
                pmlib.log.warn(self.data.name, "Folder index not found or unknown!")
                return False

        if self.data.type is Source.unknown:
            pmlib.log.warn(self.data.name, "Folder not found or unknown!")
            return False

        return True

    def __init__(self, line: str):
        m = _entry.search(line)
        if m is None:
            return

        m_object = _object.search(m.group("Parent"))

        parent_id = Object(m_object)

        self.children = []
        self.mails = []
        self.symbols = []
        self.navigation = Navigation()
        self.type = get_entry_type(int(m.group("Type")))
        self.name = str(m.group("Name"))
        self.report = EntryReport()

        if parent_id.valid is True:
            self.parent_id = parent_id.id

        if self.type is Entry.folder:
            m_folder = _folder.search(m.group("Data"))
            data = Folder(m_folder)
            if data.valid is True:
                self.data = data
        else:
            m_object = _object.search(m.group("Data"))
            data = Object(m_object)
            if data.valid is True:
                self.data = data
        if self.data is None:
            return

        if self.type is None:
            return

        if self.type is Entry.folder:
            check = self._check_folder()
            if check is False:
                return

        self.valid = True
        return

    def populate(self, datalist: List[EntryData]):
        if self.is_sorted is True:
            return

        children = []

        for _item in datalist:
            if _item.parent_id == self.id:
                children.append(_item)
                _item.parent = self

                if _item.type is Entry.folder:
                    _item.is_sorted = True

        for _item in sorted(children, key=sort_items):
            if _item.type is Entry.folder:
                self.children.append(_item)

        for _item in sorted(children, key=sort_items):
            if _item.type is Entry.tray:
                self.children.append(_item)

        self.is_sorted = True
        return

    def _set_target(self, target: str, path: str, item: EntryData) -> str:
        if path == "":
            ret = target
        else:
            ret = path

        if item.parent is None:
            ret = "{0:s}/{1:s}".format(ret, item.name)
        else:
            _data = self._set_target(target, ret, item.parent)
            ret = "{0:s}/{1:s}".format(_data, item.name)

        result = os.path.abspath(os.path.normpath(ret))
        return result

    def _set_full_name(self, path: str, item: EntryData) -> str:
        ret = ""
        if path != "":
            ret = path

        if item.parent is None:
            if ret == "":
                ret = "{0:s}".format(item.name)
            else:
                ret = "{0:s}\\{1:s}".format(ret, item.name)
        else:
            _data = self._set_full_name(ret, item.parent)
            ret = "{0:s}\\{1:s}".format(_data, item.name)

        return ret

    def add_error(self, number: int, text: str, exception: Exception):
        error = ErrorReport()
        error.number = number
        error.exception = exception
        error.text = text
        self.report.error.append(error)
        return

    def set_target(self):
        self.target = self._set_target(pmlib.config.target_path, "", self)
        self.full_name = self._set_full_name("", self)
        return


def sort_items(item: Item):
    return item.name


@dataclass()
class Data(object):

    level: int = 0
    entries: List[Item] = field(default_factory=list)
    root: Item = field(default=None)
