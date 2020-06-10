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
from typing import Union

__all__ = [
    "Type",
    "get_type",

    "State",
    "get_state"
]


class Type(Enum):

    mailbox = 2
    tray = 1
    folder = 0


def get_type(value: int) -> Union[Type, None]:
    _ret = None

    for _item in Type:
        if _item.value == value:
            _ret = _item
            break
    return _ret


class State(Enum):

    closed = 0
    open = 1
    closed_unread = 2
    open_unread = 3


def get_state(value: int) -> Union[State, None]:
    _ret = None

    for _item in State:
        if _item.value == value:
            _ret = _item
            break
    return _ret
