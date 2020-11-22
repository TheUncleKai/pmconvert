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
    "Exit",
    "Call",
    "Goto",
    "Return",
    "SkipNext",
    "LogicalAnd"
]


class Exit(Action):

    def __init__(self):
        Action.__init__(self)
        self.name = "Exit"
        self.filter = "Exit"
        return

    def parse(self, data: str) -> bool:
        return False

    def result(self) -> str:
        text = "Exit rule set"
        return text


class Call(Action):

    def __init__(self):
        Action.__init__(self)
        self.name = "Call"
        self.filter = "Call"
        self.parameter: str = ""
        return

    def parse(self, data: str) -> bool:
        return False

    def result(self) -> str:
        text = "Call label {0:s}".format(self.parameter)
        return text


class Goto(Action):

    def __init__(self):
        Action.__init__(self)
        self.name = "Goto"
        self.filter = "Goto"
        self.parameter: str = ""
        return

    def parse(self, data: str) -> bool:
        return False

    def result(self) -> str:
        text = "Goto label {0:s}".format(self.parameter)
        return text


class Return(Action):

    def __init__(self):
        Action.__init__(self)
        self.name = "Return"
        self.filter = "Return"
        return

    def parse(self, data: str) -> bool:
        return False

    def result(self) -> str:
        text = "Return from call"
        return text


class SkipNext(Action):

    def __init__(self):
        Action.__init__(self)
        self.name = "SkipNext"
        self.filter = "SkipNext"
        return

    def parse(self, data: str) -> bool:
        return False

    def result(self) -> str:
        text = "Skip next rule"
        return text


class LogicalAnd(Action):

    def __init__(self):
        Action.__init__(self)
        self.name = "LogicalAnd"
        self.filter = "LogicalAnd"
        return

    def parse(self, data: str) -> bool:
        return False

    def result(self) -> str:
        text = "Logical and next rule"
        return text
