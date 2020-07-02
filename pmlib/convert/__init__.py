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

import pmlib

from abc import ABCMeta

from typing import Union, List

from pmlib.types import Target, Source
from pmlib.item import Item
from bbutil.utils import get_attribute

__all__ = [
    "source",
    "target",

    "SourceBase",
    "TargetBase",
    "Manager"
]


class SourceBase(metaclass=ABCMeta):

    def __init__(self):
        self.source: Source = Source.unknown
        return

    @abc.abstractmethod
    def read(self, item: Item, box: mailbox.Mailbox) -> int:
        pass


class TargetBase(metaclass=ABCMeta):

    def __init__(self):
        self.root: Union[Item, None] = None
        self.target: Target = Target.unknown
        return

    @abc.abstractmethod
    def prepare(self, root: Item) -> bool:
        pass

    @abc.abstractmethod
    def run(self) -> bool:
        pass

    @abc.abstractmethod
    def close(self) -> bool:
        pass


class Manager(object):

    def __init__(self):
        self.source: List[SourceBase] = []
        self.target: List[TargetBase] = []

        for _item in pmlib.convert.source.__all__:
            path = "pmlib.convert.source.{0:s}".format(_item)
            target = get_attribute(path, "name")
            attr = get_attribute(path, target)
            self.source.append(attr())

        for _item in pmlib.convert.source.__all__:
            path = "pmlib.convert.target.{0:s}".format(_item)
            target = get_attribute(path, "name")
            attr = get_attribute(path, target)
            self.target.append(attr())
        return

    def get_source(self, source: Source) -> Union[None, SourceBase]:
        for _item in self.source:
            if _item.source is source:
                return _item
        return None

    def get_target(self, target: Target) -> Union[None, TargetBase]:
        for _item in self.target:
            if _item.target is target:
                return _item
        return None
