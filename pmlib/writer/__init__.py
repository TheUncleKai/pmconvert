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


import abc
import mailbox

from abc import ABCMeta
from typing import List, Union

from pmlib.item import Item
from pmlib.types import Source
from bbutil.utils import get_attribute

__all__ = [
    "mbox",

    "ReadBase",
    "Reader"
]

_reader = [
    "mbox"
]


class ReadBase(metaclass=ABCMeta):

    def __init__(self):
        self.source: Source = Source.unknown
        return

    @abc.abstractmethod
    def read(self, item: Item, box: mailbox.Mailbox) -> int:
        pass


class Reader(object):

    def __init__(self):
        self.modules: List[ReadBase] = []

        for _item in _reader:
            path = "pmlib.reader.{0:s}".format(_item)
            name = get_attribute(path, "source")
            attr = get_attribute(path, name)
            c = attr()
            self.modules.append(c)
        return

    def get_reader(self, source: Source) -> Union[None, ReadBase]:
        for _item in self.modules:
            if _item.source is source:
                return _item
        return None
