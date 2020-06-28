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

import pmlib

from abc import ABCMeta

from typing import Union, List, Tuple, Any

from pmlib.types import Target
from pmlib.item import Item
from bbutil.utils import get_attribute

__all__ = [
    "mbx",
    "maildir",

    "Converter",
    "Convert"
]

_converter = [
    "mbx",
    "maildir"
]


class Converter(metaclass=ABCMeta):

    def __init__(self, root: Item):
        self.root: Item = root
        self.target: Target = Target.unknown
        return

    @abc.abstractmethod
    def prepare(self) -> bool:
        pass

    @abc.abstractmethod
    def run(self) -> bool:
        pass

    @abc.abstractmethod
    def close(self) -> bool:
        pass


class Convert(object):

    def __init__(self):
        self.modules: List[Tuple] = []
        return

    def init(self):
        for _item in _converter:
            path = "pmlib.convert.{0:s}".format(_item)
            target = get_attribute(path, "target")
            name = get_attribute(path, "converter")
            attr = get_attribute(path, name)
            item = (target, attr)
            self.modules.append(item)
        return

    def get_converter(self) -> Union[None, Any]:
        for _item in self.modules:
            item_target, attr = _item
            if item_target is pmlib.config.target_type:
                return attr
        return None
