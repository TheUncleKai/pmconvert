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

from typing import Union

import pmlib

from pmlib.convert import TargetBase
from pmlib.item import Item, sort_items
from pmlib.types import Target, Entry
from pmlib.utils import clean_folder, create_folder

name = "TargetMBOX"

__all__ = [
    "name",
    "TargetMaildir"
]


class TargetMaildir(TargetBase):

    def __init__(self):
        TargetBase.__init__(self)
        self.target = Target.maildir
        self.maildir: Union[mailbox.Maildir, None] = None
        self._current: Union[mailbox.Maildir, None] = None
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

    def _convert(self, item: Item, maildir: mailbox.Maildir) -> bool:

        if item.type is Entry.folder:
            newmaildir = maildir.add_folder(item.name)
            newmaildir.lock()

            source = pmlib.manager.get_source(item.data.type)
            if source is None:
                pmlib.log.warn(item.name,
                               "Mailbox format is not yet implemented: {0:s}".format(item.data.type.name))
                newmaildir.unlock()
                return True

            item.report.target_format = self.target
            check = source.read(item, newmaildir)

            newmaildir.flush()
            newmaildir.unlock()
            return check
        else:
            pmlib.log.inform("TRAY", item.full_name)
            newmaildir = maildir.add_folder(item.name)
            newmaildir.lock()

            # first convert folder
            for _item in sorted(item.children, key=sort_items):
                if _item.type is Entry.folder:
                    check = self._convert(_item, newmaildir)
                    if check is False:
                        return False

            # then trays
            for _item in sorted(item.children, key=sort_items):
                if _item.type is not Entry.folder:

                    check = self._convert(_item, newmaildir)
                    if check is False:
                        return False

            newmaildir.flush()
            newmaildir.unlock()
            maildir.flush()

        return True

    def prepare(self, root: Item) -> bool:
        self.root = root
        self.root.set_target()

        if os.path.exists(self.root.target):
            pmlib.log.inform("Mailbox", "Remove folder {0:s}".format(self.root.target))
            check = clean_folder(self.root.target)
            if check is False:
                return False

        check = create_folder(self.root.target)
        if check is False:
            pmlib.log.error("Unable to create target folder: {0:s}".format(self.root.target))
            return False

        self.maildir = mailbox.Maildir(self.root.target)
        self.maildir.lock()
        return True

    def run(self) -> bool:

        check = self._convert(self.root, self.maildir)
        return check

    def close(self) -> bool:
        self.maildir.unlock()
        return True
