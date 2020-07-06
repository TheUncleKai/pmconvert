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


class _Compare(Enum):

    Contains = "contains"
    Is = "is"


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
        Rule.__init__(self)
        self.name = "Headers..."
        self.rule = "header"
        return

    def parse(self, data: str) -> bool:
        return True
