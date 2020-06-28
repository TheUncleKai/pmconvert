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
import email

from typing import List

import pmlib

from pmlib.convert import Converter
from pmlib.item import Item, sort_items
from pmlib.types import Source, Target, Position, Entry
from pmlib.utils import convert_bytes, clean_folder, create_folder


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

    def _run_pmm(self, item: Item) -> bool:
        path = "{0:s}.mbx".format(item.target)
        item.report.filename = path
        item.report.target_format = Target.mbox

        mbox = mailbox.mbox(path)
        mbox.lock()

        try:
            f = open(item.data.filename, mode='rb')
        except OSError as e:
            pmlib.log.exception(e)
            return False

        f.seek(128)  # move to first mail

        n = 0
        count = 1

        stream = f.read(-1)
        item.size = len(stream)
        positions: List[Position] = []

        start = 0
        for byte in stream:
            if byte == 0x1a:  # 1A seperates the mails
                pos = Position(start=start, end=n)
                positions.append(pos)
                count += 1
                start = n + 1
            n += 1

        item.count = len(positions)

        count = "{0:d}".format(item.count).rjust(6, " ")
        size = convert_bytes(item.size)

        pmlib.log.inform(item.parent.name,
                         "{0:s} mails for {1:s} ({2:s})".format(count, item.name, size))

        progress = pmlib.log.progress(item.count)

        n = 0
        for _pos in positions:
            value = stream[_pos.start:_pos.end]

            msg = email.message_from_bytes(value)
            try:
                mbox.add(msg)
            except UnicodeEncodeError as e:
                text = self._store_fault(item, n, value)
                item.add_error(n, text, e)
                item.report.failure += 1
            else:
                item.report.success += 1

            mbox.flush()
            progress.inc()
            n += 1
            item.report.count = n

        pmlib.log.clear()

        for _error in item.report.error:
            pmlib.log.error(_error.text)

        f.close()
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
