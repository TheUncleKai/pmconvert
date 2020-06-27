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
from optparse import OptionParser

import pmlib
import pmlib.log

from pmlib import config

from pmlib.convert import Convert
from pmlib.hierachy import Hierarchy
from pmlib.item import Item, sort_items
from pmlib.types import Entry
from pmlib.utils import create_folder, clean_folder
from pmlib.report.html import ReportHTML


class Console(object):

    def __init__(self):
        self._converter: Convert = Convert()

        usage = "usage: %prog [options] arg1 arg2"
        self.parser: OptionParser = OptionParser(usage=usage)
        self.parser.add_option("-v", "--verbose", help="run verbose level [0..3]", type="int", metavar="1",
                               default=0)
        self.parser.add_option("-f", "--folder", help="pegasus mail folder", type="string", metavar="<FOLDER>",
                               default="")
        self.parser.add_option("-r", "--root", help="pegasus mail root mailbox", type="string", metavar="<MAILBOX>",
                               default="My mailbox")
        self.parser.add_option("-x", "--export", help="type for data export", type="string", metavar="mbox|maildir",
                               default="mbox")
        self.parser.add_option("-t", "--target", help="target path for export", type="string", metavar="<FOLDER>",
                               default="")
        return

    def _create_folder(self, item: Item) -> bool:
        item.set_target()

        if item.type is Entry.folder:
            return True

        if os.path.exists(item.target):
            pmlib.log.inform("Mailbox", "Remove folder {0:s}".format(item.target))
            check = clean_folder(item.target)
            if check is False:
                return False

        check = create_folder(item.target)
        if check is False:
            pmlib.log.error("Unable to create target folder: {0:s}".format(item.target))
            return False

        for _item in item.children:
            check = self._create_folder(_item)
            if check is False:
                return False

        return True

    def _convert_item(self, item: Item) -> bool:
        attr = self._converter.get_converter(item.data.type)
        if attr is None:
            text = "Unable to convert folder {0:s} with type {1:s} to {2:s}".format(item.name,
                                                                                    item.data.type.name,
                                                                                    pmlib.config.target_type.name)
            pmlib.log.warn("Mailbox", text)
            return True

        converter = attr()
        check = converter.prepare(item)
        if check is False:
            return False

        check = converter.run()
        if check is False:
            return False

        check = converter.close()
        if check is False:
            return False

        for _error in item.report.error:
            pmlib.log.warn(item.name, _error.text)

        return True

    def _export_item(self, item: Item) -> bool:

        if item.type is Entry.folder:
            check = self._convert_item(item)
            if check is False:
                return False
        else:
            pmlib.log.inform("TRAY", item.full_name)

            # first convert folder
            for _item in sorted(item.children, key=sort_items):
                if _item.type is Entry.folder:
                    check = self._export_item(_item)
                    if check is False:
                        return False

            # then trays
            for _item in sorted(item.children, key=sort_items):
                if _item.type is not Entry.folder:
                    check = self._export_item(_item)
                    if check is False:
                        return False

        return True

    def prepare(self) -> bool:
        (options, args) = self.parser.parse_args()

        check = config.parse(options)
        if check is False:
            return False

        pmlib.log.setup(level=config.verbose)

        pmlib.log.inform("Mail folder", "{0:s}".format(config.pegasus_path))
        pmlib.log.inform("Root Mailbox", "{0:s}".format(config.pegasus_root))
        pmlib.log.inform("Target folder", "{0:s}".format(config.target_path))

        check = create_folder(config.target_path)
        if check is False:
            pmlib.log.error("Unable to create target folder!")
            return False

        return True

    def run(self) -> bool:
        self._converter.init()

        hierarchy = Hierarchy()

        count = hierarchy.parse()
        if count == 0:
            return False

        hierarchy.sort()
        root = pmlib.data.root

        # check = self._create_folder(pmlib.data.root)
        # if check is False:
        #     return False
        #
        # check = self._export_item(pmlib.data.root)
        # if check is False:
        #     return False

        return True

    @staticmethod
    def close() -> bool:

        html = ReportHTML(pmlib.data.root)
        check = html.create()
        return check
