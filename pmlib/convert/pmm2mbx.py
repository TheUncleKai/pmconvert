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

from typing import List, Union

import pmlib

from pmlib.convert import Converter
from pmlib.item import Item
from pmlib.types import Source, Target, Position
from pmlib.utils import convert_bytes


converter = "ConvertPMM2MBox"


class ConvertPMM2MBox(Converter):

    def __init__(self):
        Converter.__init__(self)
        self.errors: list = []
        self.source = Source.pegasus
        self.target = Target.mbox
        self.mbox: Union[mailbox.mbox, None] = None

        self.f = None
        self.positions: List[Position] = []
        return

    def prepare(self, item: Item) -> bool:
        self.item = item
        try:
            self.f = open(self.item.data.filename, mode='rb')
        except OSError as e:
            pmlib.log.exception(e)
            return False

        self.f.seek(128)  # move to first mail

        path = "{0:s}.mbx".format(self.item.target)
        self.mbox = mailbox.mbox(path)
        self.mbox.lock()
        return True

    def _store_fault(self, number: int, value: bytes):
        filename = "{0:s}_{1:d}.eml".format(self.item.target, number)
        filename = os.path.abspath(os.path.normpath(filename))

        self.errors.append("Unable to decode mail {0:d} in {1:s}".format(number, self.item.name))

        f = open(filename, mode="wb")
        f.write(value)
        f.close()
        return

    def run(self) -> bool:
        n = 0
        count = 1

        stream = self.f.read(-1)

        self.item.size = len(stream)

        start = 0
        for byte in stream:
            if byte == 0x1a:  # 1A seperates the mails
                pos = Position(start=start, end=n)
                self.positions.append(pos)
                count += 1
                start = n + 1
            n += 1

        self.item.count = len(self.positions)

        count = "{0:d}".format(self.item.count).rjust(6, " ")
        size = convert_bytes(self.item.size)

        pmlib.log.inform(self.item.parent.name,
                         "{0:s} mails for {1:s} ({2:s})".format(count, self.item.name, size))

        progress = pmlib.log.progress(self.item.count)

        n = 0
        for _pos in self.positions:
            value = stream[_pos.start:_pos.end]

            # m = 0
            # for i in range(len(value)):
            #     _n = value[i:i+1]
            #     _num = ord(_n)
            #     if _num > 128:
            #         pmlib.log.error("Stream out of range: {0:d}, pos {1:d}".format(_num, m))
            #     m += 1

            msg = email.message_from_bytes(value)
            try:
                self.mbox.add(msg)
            except UnicodeEncodeError as e:
                self._store_fault(n, value)

            self.mbox.flush()
            progress.inc()
            n += 1

        pmlib.log.clear()

        for _error in self.errors:
            pmlib.log.error(_error)
        return True

    def close(self) -> bool:
        self.f.close()
        self.mbox.unlock()

        del self.f
        del self.mbox

        self.item = None
        self.f = None
        self.mbox = None
        self.positions = []
        return True
