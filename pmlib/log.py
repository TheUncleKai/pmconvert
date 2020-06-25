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

from bbutil.logging import Logging

_log: Logging = Logging()

__all__ = [
    "setup",
    "register",
    "get_writer",

    "inform",
    "warn",
    "error",
    "exception",
    "open",
    "close",
    "clear"
]

setup = _log.setup
register = _log.register
get_writer = _log.get_writer
progress = _log.progress

inform = _log.inform
warn = _log.warn
error = _log.error
exception = _log.exception
open = _log.open
close = _log.close
clear = _log.clear
