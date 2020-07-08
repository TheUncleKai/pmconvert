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
    "Expression"
]


class _ExpressionType(Enum):

    headers = "headers"
    body = "body"
    both = "both"

# =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
# Expression...

#  If expression headers matches "From: <tech@kpslashhaven.net>" Move "YZDNYMAS:3D5D:FOL00816"
#  If expression body matches "Return-path: <do-not-reply@archiveofourown.org>" Move "MDJIPSSK:0830:FOL00B44"
#  If expression both matches "Return-path: <do-not-reply@archiveofourown.org>" Move "MDJIPSSK:0830:FOL00B44"


class Expression(Rule):

    def __init__(self):
        Rule.__init__(self, "Expression...")
        return

    def parse(self, data: str) -> bool:
        return False
