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
import mailbox


import pmlib

from pmlib.convert import Converter
from pmlib.reader import Reader
from pmlib.item import Item, sort_items
from pmlib.types import Source, Target, Entry
from pmlib.utils import clean_folder, create_folder


converter = "ConvertMBox"
target = Target.mbox


class ConvertMBox(Converter):

    def __init__(self, root: Item):
        Converter.__init__(self, root)
        self.target = Target.mbox
        return

    @staticmethod
    def _store_fault(item: Item, number: int, value: bytes) -> str:
        filename = "{0:s}_{1:d}.eml".format(item.target, number)
        filename = os.path.abspath(os.path.normpath(filename))

        error_text = "Unable to decode mail {0:d} in {1:s}".format(number, item.name)

        f = open(filename, mode="wb")
        f.write(value)
        f.close()
        return error_text

    @staticmethod
    def _run_mbx(item: Item) -> bool:
        pmlib.log.warn(item.parent.name, "Unix mailbox is not yet implemented: {0:s}".format(item.name))
        return True

    def _convert_item(self, item: Item, source: Source) -> bool:
        path = "{0:s}.mbx".format(item.target)
        item.report.filename = path
        item.report.target_format = Target.mbox

        reader = Reader()

        read = reader.get_reader(source)
        if read is None:
            return False

        mbox = mailbox.mbox(path)
        mbox.lock()

        read.read(item, mbox)

        mbox.unlock()
        return True

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

    def _convert(self, item: Item) -> bool:

        if item.type is Entry.folder:
            reader =


            if item.data.type is Source.unix:
                check = self._run_mbx(item)
                return check

            if item.data.type is Source.pegasus:
                check = self._run_pmm(item)
                return check
        else:
            pmlib.log.inform("TRAY", item.full_name)

            # first convert folder
            for _item in sorted(item.children, key=sort_items):
                if _item.type is Entry.folder:
                    check = self._convert(_item)
                    if check is False:
                        return False

            # then trays
            for _item in sorted(item.children, key=sort_items):
                if _item.type is not Entry.folder:
                    check = self._convert(_item)
                    if check is False:
                        return False

        return True

    def prepare(self) -> bool:
        check = self._create_folder(self.root)
        if check is False:
            return False
        return True

    def run(self) -> bool:

        check = self._convert(self.root)
        return check

    def close(self) -> bool:
        return True
