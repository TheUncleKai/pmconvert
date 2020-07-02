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

from pmlib.reader import Reader
from pmlib.item import Item
from pmlib.types import Source, Position
from pmlib.utils import convert_bytes

source = "ReaderMBX"


class ReaderMBX(Reader):

    def __init__(self, item: Item, box: mailbox.Mailbox):
        Reader.__init__(self, item, box)
        self.source: Source = Source.unix
        return

    @staticmethod
    def _store_fault(item: Item, number: int, value: bytes) -> str:
        filename = "{0:s}/{1:s}_{2:d}.eml".format(pmlib.config.target_path, item.name, number)
        filename = os.path.abspath(os.path.normpath(filename))

        error_text = "Unable to decode mail {0:d} in {1:s}".format(number, item.name)

        f = open(filename, mode="wb")
        f.write(value)
        f.close()
        return error_text

    def read(self) -> int:
        try:
            f = open(self.item.data.filename, mode='rb')
        except OSError as e:
            pmlib.log.exception(e)
            return False

        f.seek(128)  # move to first mail

        n = 0
        count = 1

        stream = f.read(-1)
        self.item.size = len(stream)
        positions: List[Position] = []

        start = 0
        for byte in stream:
            if byte == 0x1a:  # 1A seperates the mails
                pos = Position(start=start, end=n)
                positions.append(pos)
                count += 1
                start = n + 1
            n += 1

        self.item.count = len(positions)

        count = "{0:d}".format(self.item.count).rjust(6, " ")
        size = convert_bytes(self.item.size)

        pmlib.log.inform(self.item.parent.name,
                         "{0:s} mails for {1:s} ({2:s})".format(count, self.item.name, size))

        progress = pmlib.log.progress(self.item.count)

        n = 0
        for _pos in positions:
            value = stream[_pos.start:_pos.end]

            msg = email.message_from_bytes(value)
            try:
                self.box.add(msg)
            except UnicodeEncodeError as e:
                text = self._store_fault(self.item, n, value)
                self.item.add_error(n, text, e)
                self.item.report.failure += 1
            else:
                self.item.report.success += 1

            self.box.flush()
            progress.inc()
            n += 1
            self.item.report.count = n

        pmlib.log.clear()

        for _error in self.item.report.error:
            pmlib.log.error(_error.text)

        f.close()
        self.box.unlock()
        return self.item.report.count
