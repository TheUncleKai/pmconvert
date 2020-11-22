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

from enum import Enum

from pmlib.filter.types import Rule

__all__ = [
    "Expression"
]


class _ExpressionType(Enum):

    unknown = "unknown"
    headers = "headers"
    body = "body"
    both = "both"

# =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
# Expression...

#  If expression headers matches "From: <tech@kpslashhaven.net>" Move "YZDNYMAS:3D5D:FOL00816"
#  If expression body matches "Return-path: <do-not-reply@archiveofourown.org>" Move "MDJIPSSK:0830:FOL00B44"
#  If expression both matches "Return-path: <do-not-reply@archiveofourown.org>" Move "MDJIPSSK:0830:FOL00B44"


class Expression(Rule):

    def __repr__(self):
        text = "{0:s}: {1:s} matches {2:s}".format(str(self.action), self.type.value, self.expression)
        return text

    def __init__(self):
        Rule.__init__(self, "Expression...")

        self._pattern = re.compile(
            "If expression (?P<Type>headers|body|both) matches \"(?P<Filter>.+)\" (?P<Action>.+)")

        self.expression: str = ""
        self.type: _ExpressionType = _ExpressionType.unknown
        return

    def parse(self, data: str) -> bool:
        m = self._pattern.search(data)
        if m is None:
            return False

        _type = m.group('Type')
        _filter = m.group('Filter')
        _action = m.group('Action')

        for _expression in _ExpressionType:
            if _expression.value == _type:
                self.type = _expression

        if self.type is _ExpressionType.unknown:
            return False

        self.expression = _filter
        self.set_action(_action)
        return True
