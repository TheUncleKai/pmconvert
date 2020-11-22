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

from typing import List, Union

from bbutil.utils import get_attribute

import pmlib

from pmlib.filter.types import Rule


__all__ = [
    "action",
    "rules",
    "types",

    "Filter"
]


class _Rules(object):

    def __init__(self):
        self.modules: list = []

        import pmlib.filter.rules

        for _item in pmlib.filter.rules.__all__:
            path = "pmlib.filter.rules.{0:s}".format(_item)
            class_list = get_attribute(path, "__all__")

            for _class in class_list:
                attr = get_attribute(path, _class)
                self.modules.append(attr)
        return


class Filter(object):

    def __init__(self):
        self.rules: List[Rule] = []
        return

    @property
    def count(self) -> int:
        return len(self.rules)

    def parse(self, filename: str) -> bool:

        _rules = _Rules()
        path = os.path.abspath(os.path.normpath("{0:s}/{1:s}").format(pmlib.config.pegasus_path, filename))

        if os.path.exists(path) is False:
            pmlib.log.error("Filter not found: {0:s}".format(filename))
            return False

        try:
            f = open(path, "r")
        except OSError as e:
            pmlib.log.exception(e)
            return False

        follow_rule: Union[None, Rule] = None

        for line in f:
            if follow_rule is not None:
                check = follow_rule.parse(line)
                follow_rule = None
                if check is True:
                    continue

            for attr in _rules.modules:
                rule: Rule = attr()

                check = rule.parse(line)
                if check is True:
                    rule.filename = path
                    self.rules.append(rule)

                    if rule.follow_line is True:
                        follow_rule = rule
                    break

        f.close()
        return True
