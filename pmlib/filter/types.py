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

from typing import Union
from abc import ABCMeta

from typing import List

from bbutil.utils import get_attribute

__all__ = [
    "Action",
    "Rule"
]


class Action(metaclass=ABCMeta):

    def __repr__(self):
        return self.result()

    def __init__(self):
        self.name: str = ""
        self.filter: str = ""
        return

    @abc.abstractmethod
    def parse(self, data: str) -> bool:
        pass

    @abc.abstractmethod
    def result(self) -> str:
        pass


class _Actions(object):

    def __init__(self):
        self.modules: list = []

        for _item in __all__:
            path = "pmlib.filter.action.{0:s}".format(_item)
            input_list = get_attribute(path, "__all__")
            self._get_list(path, input_list)
        return

    def _get_list(self, path: str, input_list: List[str]):

        for _item in input_list:
            path = "pmlib.filter.action.{0:s}".format(path)
            attr = get_attribute(path, _item)
            self.modules.append(attr)
        return


class Rule(metaclass=ABCMeta):

    def __init__(self, name: str):
        self.name: str = name
        self.action: Union[Action, None] = None
        return

    def set_action(self, data: str) -> Union[Action, None]:
        actions = _Actions()

        for _item in actions.modules:
            check = _item.parse(data)
            if check is True:
                self.action = _item
                return
        return

    @abc.abstractmethod
    def parse(self, data: str) -> bool:
        pass
