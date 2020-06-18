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
from typing import List

import pmlib
from pmlib.types import TypeFolder, TypeEntry, Folder, Object, EntryData

from pmlib.utils import get_entry_type, get_entry_state


_entry = re.compile("(?P<Type>[0-9]+),(?P<State>[0-9]+),\"(?P<Data>.+)\",\"(?P<Parent>.*)\",\"(?P<Name>.*)\"")
_object = re.compile("(?P<ID>.+):(?P<Name>.+)")
_folder = re.compile("(?P<ID>.+):(?P<Folder>.+):(?P<Name>.+)")


class Item(EntryData):

    def __repr__(self):
        return self.name

    def _check_folder(self, root: str) -> bool:
        if self.data is None:
            pmlib.log.error("No folder object found!")
            return False

        filename = os.path.normpath("{0:s}/{1:s}.PMM".format(root, self.data.name))
        if os.path.exists(filename):
            self.data.type = TypeFolder.pegasus
            self.data.filename = filename

        filename = os.path.normpath("{0:s}/{1:s}.MBX".format(root, self.data.name))
        if os.path.exists(filename):
            self.data.type = TypeFolder.unix
            self.data.filename = filename

        if self.data.type is TypeFolder.unix:
            filename = os.path.normpath("{0:s}/{1:s}.PMG".format(root, self.data.name))
            if os.path.exists(filename):
                self.data.indexname = filename
            else:
                pmlib.log.warn(self.data.name, "Folder index not found or unknown!")
                return False

        if self.data.type is TypeFolder.pegasus:
            filename = os.path.normpath("{0:s}/{1:s}.PMI".format(root, self.data.name))
            if os.path.exists(filename):
                self.data.indexname = filename
            else:
                pmlib.log.warn(self.data.name, "Folder index not found or unknown!")
                return False

        if self.data.type is TypeFolder.unknown:
            pmlib.log.warn(self.data.name, "Folder not found or unknown!")
            return False

        return True

    def __init__(self, line: str, root: str):
        m = _entry.search(line)
        if m is None:
            return

        m_object = _object.search(m.group("Parent"))

        parent_id = Object(m_object)

        self.children = []
        self.type = get_entry_type(int(m.group("Type")))
        self.state = get_entry_state(int(m.group("State")))
        self.name = str(m.group("Name"))

        if parent_id.valid is True:
            self.parent_id = parent_id.id

        if self.type is TypeEntry.folder:
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

        if self.type is None or self.state is None:
            return

        if self.type is TypeEntry.folder:
            check = self._check_folder(root)
            if check is False:
                return

        self.valid = True
        return

    def populate(self, datalist: List[EntryData]):
        if self.is_sorted is True:
            return

        for _item in datalist:
            if _item.is_sorted is True:
                continue

            if _item.parent_id == self.id:
                self.children.append(_item)
                _item.parent = self

                if _item.type is TypeEntry.folder:
                    _item.is_sorted = True

        self.is_sorted = True
        return
