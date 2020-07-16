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

from datetime import datetime
from typing import Pattern, Union


__all__ = [
    "Date"
]

# =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
# Message date...

#  If date between 0 and 50 Move "BNNW0F27:6321:FOL04467"
#  If date absolute between 280501000000 and 280601000000
#    Move "BNNW0F27:6321:FOL04467"


class Date(Rule):

    def __repr__(self):
        if (self.days1 > 0) and (self.days2 > 0):
            text = "{0:s}: If age between {1:d} and {2:d} days".format(str(self.action), self.days1, self.days2)
        else:
            text = "{0:s}: If date between {1:s} and {2:s}".format(str(self.action), str(self.time1), str(self.time2))
        return text

    def __init__(self):
        Rule.__init__(self, "Message date...")

        self._pattern1 = re.compile(
            "If date between (?P<Days1>[0-9]+) and (?P<Days2>[0-9]+) (?P<Action>.+)")

        self._pattern2 = re.compile(
            "If date absolute between (?P<Date1>[0-9]+) and (?P<Date2>[0-9]+)")

        self._pattern_second: Pattern = re.compile(" {3}(?P<Action>.+)")

        self._date: Pattern = re.compile("(?P<YY>[0-9][0-9])(?P<MM>[0-9][0-9])(?P<DD>[0-9][0-9])(?P<hh>[0-9][0-9])(?P<mm>[0-9][0-9])(?P<ss>[0-9][0-9])")

        self.is_days: bool = False

        self.days1: int = 0
        self.days2: int = 0
        self.time1: Union[None, datetime] = None
        self.time2: Union[None, datetime] = None
        return

    def parse(self, data: str) -> bool:
        if self.follow_line is True:
            m = self._pattern_second.search(data)
            if m is None:
                return False
            self.set_action(m.group('Action'))
            return True

        m = self._pattern1.search(data)
        if m is not None:
            self.is_days = True
            self.days1 = int(m.group('Days1'))
            self.days2 = int(m.group('Days2'))
            self.set_action(m.group('Action'))
            return True

        m = self._pattern2.search(data)
        if m is not None:
            self.follow_line = True
            self.is_days = False

            d1 = self._date.search(m.group('Date1'))
            d2 = self._date.search(m.group('Date2'))
            if (d1 is None) or (d2 is None):
                return False

            self.time1 = datetime(int(d1.group('YY')),
                                  int(d1.group('MM')),
                                  int(d1.group('DD')),
                                  int(d1.group('hh')),
                                  int(d1.group('mm')),
                                  int(d1.group('ss')))

            self.time2 = datetime(int(d2.group('YY')),
                                  int(d2.group('MM')),
                                  int(d2.group('DD')),
                                  int(d2.group('hh')),
                                  int(d2.group('mm')),
                                  int(d2.group('ss')))
            return True
        return False
