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

from typing import Union

import pmlib

from pmlib.filter.types import Action
from pmlib.types import Folder

__all__ = [
    "Copy",
    "Move"
]


_folder = re.compile("(?P<ID>.+):(?P<Folder>.+):(?P<Name>.+)")


class Copy(Action):

    def __init__(self):
        Action.__init__(self)
        self.name = "Copy"
        self.filter = "Copy"
        self.folder: Union[Folder, None] = None

        self._pattern = re.compile("Copy \"(?P<Folder>.+)\"")
        return

    def parse(self, data: str) -> bool:
        m = self._pattern.search(data)
        if m is None:
            return False

        folder = m.group('Folder')

        m = _folder.search(folder)
        if m is None:
            return False

        _id = m.group('ID')

        self.folder = pmlib.data.root.search(_id)

        if self.folder is None:
            return False

        self.folder.rules.append(self.rule)
        return True

    def result(self) -> str:
        text = "Copy to {0:s}".format(self.folder.name)
        return text


class Move(Action):

    def __init__(self):
        Action.__init__(self)
        self.name = "Move"
        self.filter = "Move"
        self.folder: Union[Folder, None] = None

        self._pattern = re.compile("Move \"(?P<Folder>.+)\"")
        return

    def parse(self, data: str) -> bool:
        m = self._pattern.search(data)
        if m is None:
            return False

        folder = m.group('Folder')

        m = _folder.search(folder)
        if m is None:
            return False

        _id = m.group('ID')

        self.folder = pmlib.data.root.search(_id)

        if self.folder is None:
            return False

        self.folder.rules.append(self.rule)
        return True

    def result(self) -> str:
        text = "Move to {0:s}".format(self.folder.name)
        return text
