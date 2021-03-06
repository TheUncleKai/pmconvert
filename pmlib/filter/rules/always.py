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

import re

from pmlib.filter.types import Rule

__all__ = [
    "Always"
]

# =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
# Always

# Always MarkRead ""


class Always(Rule):

    def __repr__(self):
        text = "{0:s}: Always".format(str(self.action))
        return text

    def __init__(self):
        Rule.__init__(self, "Always")

        self._pattern = re.compile(
            "Always (?P<Action>.+)")
        return

    def parse(self, data: str) -> bool:
        m = self._pattern.search(data)
        if m is None:
            return False

        _action = m.group('Action')
        self.set_action(_action)
        return True
