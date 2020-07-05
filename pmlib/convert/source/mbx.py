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

from pathlib import Path

import pmlib

from pmlib.convert import SourceBase
from pmlib.item import Item
from pmlib.types import Source
from pmlib.utils import convert_bytes

__all__ = [
    "name",
    "SourceMBX"
]

name = "SourceMBX"


class SourceMBX(SourceBase):

    def __init__(self):
        SourceBase.__init__(self)
        self.source: Source = Source.unix
        return

    @staticmethod
    def _store_fault(item: Item, number: int, mail: email.message.EmailMessage) -> str:
        filename = "{0:s}/{1:s}_{2:d}.eml".format(pmlib.config.target_path, item.name, number)
        filename = os.path.abspath(os.path.normpath(filename))

        error_text = "Unable to decode mail {0:d} in {1:s}".format(number, item.name)

        f = open(filename, mode="w", encoding='utf-8')
        f.write(mail.as_string())
        f.close()
        return error_text

    def read(self, item: Item, box: mailbox.Mailbox) -> bool:

        fs_info = Path(item.data.filename)
        item.size = fs_info.stat().st_size

        mbx = mailbox.mbox(item.data.filename)
        mbx.lock()

        max_count = len(mbx)

        progress = pmlib.log.progress(max_count)

        count = "{0:d}".format(max_count).rjust(6, " ")
        size = convert_bytes(item.size)

        pmlib.log.inform(item.parent.name,
                         "{0:s} mails for {1:s} ({2:s})".format(count, item.name, size))

        n = 0
        for msg in mbx:
            try:
                box.add(msg)
            except UnicodeEncodeError as e:
                text = self._store_fault(item, n, msg)
                item.add_error(n, text, e)
                item.report.failure += 1
            else:
                item.report.success += 1

            box.flush()
            progress.inc()
            n += 1
            item.report.count = n

        pmlib.log.clear()

        for _error in item.report.error:
            pmlib.log.error(_error.text)

        mbx.unlock()
        return True
