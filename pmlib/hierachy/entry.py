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
from pmlib.hierachy.types import Type, State, get_type, get_state


class Entry(object):

    def __init__(self):
        self.parent: Union[Entry, None] = None

        self.unique_id: str = ""
        self.folder_id: str = ""
        self.name: str = ""

        self.type: Type = Type.mailbox
        self.state: State = State.closed

        # 0,0,"GTCNHPSY:0385:UNX0391B","1D553105:Accounts","Chefkoch"

        self._re_entry = re.compile(
            "(?P<Type>[0-9]+),(?P<State>[0-9]+),\"(?P<Folder>.+)\",\"(?P<Parent>.*)\",\"(?P<Name>.*)\"")

        return

    def parse(self, line: str) -> bool:

        m = self._re_entry.search(line)
        if m is None:
            return False

        self.type = get_type(int(m.group("Type")))
        if self.type is None:
            return False

        self.state = get_state(int(m.group("State")))
        if self.state is None:
            return False

        data_folder = m.group("Folder")
        data_parent = m.group("Parent")
        name = m.group("Name")
        if name is None:
            return False

        self.name = name
        return True

    def show(self):
        pmlib.log.inform("Entry", "{0:s},{1:s},{2:s}".format(self.type.name, self.state.name, self.name))
        return
