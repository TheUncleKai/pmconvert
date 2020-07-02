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
from typing import List

from pmlib.item import Item
from pmlib.types import Source, ErrorReport


class Reader(metaclass=ABCMeta):

    def __init__(self, root: Item, box: mailbox.Mailbox):
        self.item: Item = root
        self.source: Source = Source.unknown
        self.box: mailbox.Mailbox = box
        self.error: List[ErrorReport] = []
        return

    @abc.abstractmethod
    def read(self) -> int:
        pass
