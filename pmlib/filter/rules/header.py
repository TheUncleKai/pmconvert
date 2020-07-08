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

from typing import List
from enum import Enum

from pmlib.filter.types import Rule

__all__ = [
    "Header"
]


class _Condition(Enum):

    To = "T"
    From = "F"
    Cc = "C"
    Subject = "S"
    ReplyTo = "R"
    Sender = "E"

# =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
# Headers...

#  If header "T" contains "ubuntu-security-announce@lists.ubuntu.com" Move "2Q76BD9H:22D9:FOL034E4"

#  T: To
#  F: From
#  C: Cc
#  S: Subject
#  R: Reply-to
#  E: Sender

#  contains
#  is


class Header(Rule):

    def __init__(self):
        Rule.__init__(self, "Headers...")
        self._pattern = re.compile(
            "If header \"(?P<Header>[TFCSRE]+)\" (?P<Type>contains|is) \"(?P<Filter>.+)\" (?P<Action>.+)")

        self.header: List[_Condition] = []
        self.type: str = ""
        self.filter: str = ""
        return

    def parse(self, data: str) -> bool:
        m = self._pattern.search(data)
        if m is None:
            return False

        _header = m.group('Header')
        _action = m.group('Action')

        self.type = m.group('Type')
        self.filter = m.group('Filter')

        for _char in _header:
            for condition in _Condition:
                if condition.value == _char:
                    self.header.append(condition)

        self.set_action(_action)
        return True
