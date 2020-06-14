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

import re
import os
from typing import Union, Any, List
from dataclasses import dataclass, field

import pmlib
from pmlib.hierachy.types import Type, Folder, State, get_type, get_state

__all__ = [
    "Entry"
]


_entry = re.compile("(?P<Type>[0-9]+),(?P<State>[0-9]+),\"(?P<Data>.+)\",\"(?P<Parent>.*)\",\"(?P<Name>.*)\"")
_object = re.compile("(?P<ID>.+):(?P<Name>.+)")
_folder = re.compile("(?P<ID>.+):(?P<Folder>.+):(?P<Name>.+)")


@dataclass(init=False)
class _Object(object):

    id: str
    name: str
    valid: bool = False

    def __repr__(self):
        return self.id

    def __init__(self, data: str):
        m = _object.search(data)
        if m is None:
            return
        self.id = m.group("ID")
        self.name = m.group("Name")
        self.valid = True
        return


@dataclass(init=False)
class _Folder(object):

    id: str = ""
    folder: str = ""
    name: str = ""
    type: Folder = Folder.unknown
    filename: str = ""
    indexname: str = ""
    valid: bool = False

    def __repr__(self):
        return self.id

    def __init__(self, data: str):
        m = _folder.search(data)
        if m is None:
            return
        self.id = m.group("ID")
        self.folder = m.group("Folder")
        self.name = m.group("Name")
        self.valid = True
        return


@dataclass(init=False)
class _Entry(object):

    type: Type = Type.unknown
    state: State = State.unknown

    data: Union[_Object, _Folder] = None
    children: List[Any] = field(default_factory=list)

    parent: Any = None
    parent_id: str = ""
    name: str = ""
    valid: bool = False
    is_root: bool = False
    is_sorted: bool = False

    @property
    def id(self) -> str:
        return self.data.id


class Entry(_Entry):

    def __repr__(self):
        return self.name

    def _check_folder(self, root: str) -> bool:
        if self.data is None:
            pmlib.log.error("No folder object found!")
            return False

        filename = os.path.normpath("{0:s}/{1:s}.PMM".format(root, self.data.name))
        if os.path.exists(filename):
            self.data.type = Folder.pegasus
            self.data.filename = filename

        filename = os.path.normpath("{0:s}/{1:s}.MBX".format(root, self.data.name))
        if os.path.exists(filename):
            self.data.type = Folder.unix
            self.data.filename = filename

        if self.data.type is Folder.unix:
            filename = os.path.normpath("{0:s}/{1:s}.PMG".format(root, self.data.name))
            if os.path.exists(filename):
                self.data.indexname = filename
            else:
                pmlib.log.warn(self.data.name, "Folder index not found or unknown!")
                return False

        if self.data.type is Folder.pegasus:
            filename = os.path.normpath("{0:s}/{1:s}.PMI".format(root, self.data.name))
            if os.path.exists(filename):
                self.data.indexname = filename
            else:
                pmlib.log.warn(self.data.name, "Folder index not found or unknown!")
                return False

        if self.data.type is Folder.unknown:
            pmlib.log.warn(self.data.name, "Folder not found or unknown!")
            return False

        return True

    def __init__(self, line: str, root: str):
        m = _entry.search(line)
        if m is None:
            return

        parent_id = _Object(m.group("Parent"))

        self.children = []
        self.type = get_type(int(m.group("Type")))
        self.state = get_state(int(m.group("State")))
        self.name = str(m.group("Name"))

        if parent_id.valid is True:
            self.parent_id = parent_id.id

        if self.type is Type.folder:
            data = _Folder(m.group("Data"))
            if data.valid is True:
                self.data = data
        else:
            data = _Object(m.group("Data"))
            if data.valid is True:
                self.data = data
        if self.data is None:
            return

        if self.type is None or self.state is None:
            return

        if self.type is Type.folder:
            check = self._check_folder(root)
            if check is False:
                return

        self.valid = True
        return

    def populate(self, datalist: List[_Entry]):
        if self.is_sorted is True:
            return

        for _item in datalist:
            if _item.is_sorted is True:
                continue

            if _item.parent_id == self.id:
                self.children.append(_item)
                _item.parent = self

                if _item.type is Type.folder:
                    _item.is_sorted = True

        self.is_sorted = True
        return

    def show(self):
        pmlib.log.inform("Entry", "{0:s},{1:s},{2:s}".format(self.type.name, self.state.name, self.name))
        return
