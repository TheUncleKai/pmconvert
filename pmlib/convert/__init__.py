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
from abc import ABCMeta

from typing import Union, List

from pmlib.types import Source, Target
from pmlib.item import Item
from bbutil.utils import get_attribute

__all__ = [
    "pmm2mbx",

    "Converter",
    "Convert"
]

_converter = [
    "pmm2mbx"
]


class Converter(metaclass=ABCMeta):

    def __init__(self):
        self.item: Union[Item, None] = None
        self.source: Source = Source.unknown
        self.target: Target = Target.unknown
        return

    @abc.abstractmethod
    def prepare(self, item: Item) -> bool:
        pass

    @abc.abstractmethod
    def run(self) -> bool:
        pass

    @abc.abstractmethod
    def close(self) -> bool:
        pass


class Convert(object):

    def __init__(self):
        self.modules: List[Converter] = []
        return

    def init(self):
        for _item in _converter:
            path = "pmlib.convert.{0:s}".format(_item)
            name = get_attribute(path, "converter")
            attr = get_attribute(path, name)
            c = attr()
            self.modules.append(c)
        return

    def get_converter(self, source: Source, target: Target) -> Union[None, Converter]:
        for _item in self.modules:
            if (_item.source is source) and (_item.target is target):
                return _item
        return None
