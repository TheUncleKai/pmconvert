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

__all__ = [
    "html",

    "Reporter",
    "Report"
]

import abc
from abc import ABCMeta
from typing import List

import pmlib

from pmlib.item import Item
from bbutil.utils import get_attribute


class Reporter(metaclass=ABCMeta):

    def __init__(self):
        self.root: Item = pmlib.data.root
        self.name: str = ""
        self.desc: str = ""
        return

    @abc.abstractmethod
    def create(self) -> bool:
        pass


_reporter = [
    "html"
]


class Report(object):

    def __init__(self):
        self.modules: List[Reporter] = []
        return

    def init(self):
        for _item in _reporter:
            path = "pmlib.report.{0:s}".format(_item)
            name = get_attribute(path, "report")
            attr = get_attribute(path, name)
            c = attr()
            self.modules.append(c)
        return
