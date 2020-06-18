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

from pmlib.hierachy import Hierarchy
from pmlib.item import Item


class Mailbox(object):

    def __init__(self, root: str):
        self.root: str = root
        self.hierarchy: Hierarchy = Hierarchy()
        self.folder: List[Item] = []
        return

    def init(self, folder: str, filename=None) -> bool:
        count = self.hierarchy.parse(folder, self.root)
        if count == 0:
            return False

        self.hierarchy.sort(self.folder)

        if filename is not None:
            self.hierarchy.export_json(filename)

        return True
