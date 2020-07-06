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


from pmlib.filter.types import Action

__all__ = [
    "Append",
    "Delete",
    "Extract",
    "Forward",
    "AddHeader"
]


class Delete(Action):

    def __init__(self):
        Action.__init__(self)
        self.name = "Delete"
        self.filter = "Delete"
        return

    def parse(self, data: str) -> bool:
        return True

    def result(self) -> str:
        text = "Delete mail"
        return text


class Forward(Action):

    def __init__(self):
        Action.__init__(self)
        self.name = "Forward"
        self.filter = "Forward"
        self.target: str = ""
        return

    def parse(self, data: str) -> bool:
        return True

    def result(self) -> str:
        text = "Forward mail to {0:s}".format(self.target)
        return text


class Extract(Action):

    def __init__(self):
        Action.__init__(self)
        self.name = "Extract"
        self.filter = "eXtract"
        self.target: str = ""
        return

    def parse(self, data: str) -> bool:
        return True

    def result(self) -> str:
        text = "Extract data to {0:s}".format(self.target)
        return text


class Append(Action):

    def __init__(self):
        Action.__init__(self)
        self.name = "Append"
        self.filter = "Append"
        self.target: str = ""
        return

    def parse(self, data: str) -> bool:
        return True

    def result(self) -> str:
        text = "Append data to {0:s}".format(self.target)
        return text


class AddHeader(Action):

    def __init__(self):
        Action.__init__(self)
        self.name = "AddHeader"
        self.filter = "AddHeader"
        self.target: str = ""
        return

    def parse(self, data: str) -> bool:
        return True

    def result(self) -> str:
        text = "Add header {0:s}".format(self.target)
        return text
