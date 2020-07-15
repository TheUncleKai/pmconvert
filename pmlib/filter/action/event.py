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

from pmlib.filter.types import Action

__all__ = [
    "Print",
    "Highlight",
    "MarkRead",
    "PlaySound",
    "Dialog",
    "Select",
    "Run",
    "SendTextFile",
    "AddToList",
    "RemoveFromList",
    "SetIdentity",
    "MarkSignificant"
]


class Print(Action):

    def __init__(self):
        Action.__init__(self)
        self.name = "Print"
        self.filter = "Print"
        return

    def parse(self, data: str) -> bool:
        return False

    def result(self) -> str:
        text = "Print mail"
        return text


class Highlight(Action):

    def __init__(self):
        Action.__init__(self)
        self.name = "Highlight"
        self.filter = "Highlight"
        self.parameter: int = 0
        return

    def parse(self, data: str) -> bool:
        return False

    def result(self) -> str:
        text = "Set message color {0:d}".format(self.parameter)
        return text


class MarkRead(Action):

    def __init__(self):
        Action.__init__(self)
        self.name = "MarkRead"
        self.filter = "MarkRead"

        self._pattern = re.compile("MarkRead \"\"")
        return

    def parse(self, data: str) -> bool:
        m = self._pattern.search(data)
        if m is None:
            return False

        return False

    def result(self) -> str:
        text = "Mark mail read"
        return text


class PlaySound(Action):

    def __init__(self):
        Action.__init__(self)
        self.name = "PlaySound"
        self.filter = "PlaySound"
        self.parameter: str = ""
        return

    def parse(self, data: str) -> bool:
        return False

    def result(self) -> str:
        text = "Play sound {0:s}".format(self.parameter)
        return text


class Dialog(Action):

    def __init__(self):
        Action.__init__(self)
        self.name = "Dialog"
        self.filter = "Dialog"
        self.parameter: str = ""
        return

    def parse(self, data: str) -> bool:
        return False

    def result(self) -> str:
        text = "Show dialog {0:s}".format(self.parameter)
        return text


class Select(Action):

    def __init__(self):
        Action.__init__(self)
        self.name = "Select"
        self.filter = "Select"
        return

    def parse(self, data: str) -> bool:
        return False

    def result(self) -> str:
        text = "Select mail"
        return text


class Run(Action):

    def __init__(self):
        Action.__init__(self)
        self.name = "Run"
        self.filter = "Run"
        self.parameter: str = ""
        return

    def parse(self, data: str) -> bool:
        return False

    def result(self) -> str:
        text = "Run program {0:s}".format(self.parameter)
        return text


class SendTextFile(Action):

    def __init__(self):
        Action.__init__(self)
        self.name = "SendTextFile"
        self.filter = "SendTextFile"
        self.parameter: str = ""
        return

    def parse(self, data: str) -> bool:
        return False

    def result(self) -> str:
        text = "Send text {0:s}".format(self.parameter)
        return text


class SendBinaryFile(Action):

    def __init__(self):
        Action.__init__(self)
        self.name = "SendBinaryFile"
        self.filter = "SendBinaryFile"
        self.parameter: str = ""
        return

    def parse(self, data: str) -> bool:
        return False

    def result(self) -> str:
        text = "Send binary {0:s}".format(self.parameter)
        return text


class AddToList(Action):

    def __init__(self):
        Action.__init__(self)
        self.name = "AddToList"
        self.filter = "AddToList"
        self.parameter: str = ""
        return

    def parse(self, data: str) -> bool:
        return False

    def result(self) -> str:
        text = "Add user to list {0:s}".format(self.parameter)
        return text


class RemoveFromList(Action):

    def __init__(self):
        Action.__init__(self)
        self.name = "RemoveFromList"
        self.filter = "RemoveFromList"
        self.parameter: str = ""
        return

    def parse(self, data: str) -> bool:
        return False

    def result(self) -> str:
        text = "Remove user from list {0:s}".format(self.parameter)
        return text


class SetIdentity(Action):

    def __init__(self):
        Action.__init__(self)
        self.name = "SetIdentity"
        self.filter = "SetIdentity"
        self.parameter: str = ""
        return

    def parse(self, data: str) -> bool:
        return False

    def result(self) -> str:
        text = "Set identity {0:s}".format(self.parameter)
        return text


class Expire(Action):

    def __init__(self):
        Action.__init__(self)
        self.name = "Expire"
        self.filter = "Expire"
        return

    def parse(self, data: str) -> bool:
        return False

    def result(self) -> str:
        text = "Expire"
        return text


class MarkSignificant(Action):

    def __init__(self):
        Action.__init__(self)
        self.name = "MarkSignificant"
        self.filter = "MarkSignificant"
        return

    def parse(self, data: str) -> bool:
        return False

    def result(self) -> str:
        text = "Mark mail as significant"
        return text
