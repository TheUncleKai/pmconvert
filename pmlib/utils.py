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
import shutil
from typing import Union

import pmlib

from pmlib.types import Entry

__all__ = [
    "create_folder",
    "clean_folder",
    "convert_bytes",
    "get_entry_type"
]


def create_folder(folder: str) -> bool:
    if os.path.exists(folder) is False:
        try:
            os.mkdir(folder)
        except OSError as e:
            pmlib.log.exception(e)
            return False

    return True


def clean_folder(folder: str) -> bool:
    for filename in os.listdir(folder):
        file_path = os.path.normpath(os.path.join(folder, filename))
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            pmlib.log.exception(e)
            return False
    return True


def convert_bytes(num: int) -> str:
    step_unit = 1000.0  # 1024 bad the size

    for x in ['bytes', 'KB', 'MB', 'GB', 'TB']:
        if num < step_unit:
            return "%3.1f %s" % (num, x)
        num /= step_unit


def get_entry_type(value: int) -> Union[Entry, None]:
    _ret = None

    for _item in Entry:
        if _item.value == value:
            _ret = _item
            break
    return _ret
