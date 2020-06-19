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

import os
from typing import Union

import pmlib
from pmlib.types import TypeEntry, EntryState


def create_folder(folder: str) -> bool:
    if os.path.exists(folder) is False:
        try:
            os.mkdir(folder)
        except OSError as e:
            pmlib.log.exception(e)
            return False

    return True


def get_entry_type(value: int) -> Union[TypeEntry, None]:
    _ret = None

    for _item in TypeEntry:
        if _item.value == value:
            _ret = _item
            break
    return _ret


def get_entry_state(value: int) -> Union[EntryState, None]:
    _ret = None

    for _item in EntryState:
        if _item.value == value:
            _ret = _item
            break
    return _ret
