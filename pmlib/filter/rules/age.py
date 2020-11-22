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
from typing import Union, Pattern

from datetime import datetime

__all__ = [
    "Age"
]

# =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
# Message age...

#  If age older than 50 Move "BNNW0F27:6321:FOL04467"
#  If age absolute older than 280501000000 Move "BNNW0F27:6321:FOL04467"
#  If age absolute older than 011212112233 Move "49ZTFXJP:12B4:FOL069F6"
#  01 12 12 11 22 33


class Age(Rule):

    def __repr__(self):
        if self.days > 0:
            text = "{0:s}: If older than {1:d} days".format(str(self.action), self.days)
        else:
            text = "{0:s}: If older than {1:s}".format(str(self.action), str(self.time))
        return text

    def __init__(self):
        Rule.__init__(self, "Message age...")

        self._pattern1 = re.compile(
            "If age older than (?P<Days>[0-9]+) (?P<Action>.+)")

        self._pattern2 = re.compile(
            "If age absolute older than (?P<Date>[0-9]+) (?P<Action>.+)")

        self._date: Pattern = re.compile("(?P<YY>[0-9][0-9])(?P<MM>[0-9][0-9])(?P<DD>[0-9][0-9])(?P<hh>[0-9][0-9])(?P<mm>[0-9][0-9])(?P<ss>[0-9][0-9])")

        self.days: int = -1
        self.time: Union[None, datetime] = None
        return

    def parse(self, data: str) -> bool:

        m = self._pattern1.search(data)
        if m is not None:
            _action = m.group('Action')
            self.days = int(m.group('Days'))
            self.set_action(m.group('Action'))
            return True

        m = self._pattern2.search(data)
        if m is not None:

            d = self._date.search(m.group('Date'))
            if d is None:
                return False

            year = int(d.group('YY'))
            month = int(d.group('MM'))
            day = int(d.group('DD'))
            hour = int(d.group('hh'))
            minute = int(d.group('mm'))
            seconds = int(d.group('ss'))

            self.time = datetime(year, month, day, hour, minute, seconds)
            self.set_action(m.group('Action'))
            return True

        return False
