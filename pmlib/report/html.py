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
from typing import List
from enum import Enum

import pmlib

from yattag import Doc, indent
from pmlib.item import Item, sort_items

from pmlib.types import Entry, Report

__all__ = [
    "ReportHTML"
]

_style = """

body {
    font-family: Arial, Helvetica, sans-serif;
    font-size: 14px;
    margin-top: 2px;
    margin-bottom: 2px;
}

button {
    background-color: #FFFFFF;
    font-weight: bold;

}

table {
    border-spacing: 5px;
}

.heading {
    font-family: Arial, Helvetica, sans-serif;
    border: none;
    text-align: left;
    outline: none;
    font-size: 14px;
}

.tree {
    font-family: Arial, Helvetica, sans-serif;
    color: blue;
    border: none;
    text-align: left;
    outline: none;
    font-size: 14px;
}

"""


# ┓  9491  2513  BOX DRAWINGS HEAVY DOWN AND LEFT
# ┳  9523  2533  BOX DRAWINGS HEAVY DOWN AND HORIZONTAL
# ━  9473  2501  BOX DRAWINGS HEAVY HORIZONTAL
# ┃  9475  2503  BOX DRAWINGS HEAVY VERTICAL
# ┗  9495  2517  BOX DRAWINGS HEAVY UP AND RIGHT
# ┣  9507  2523  BOX DRAWINGS HEAVY VERTICAL AND RIGHT


class Symbol(Enum):

    root = "&#9491;"
    tray = "&#9523;"
    horizontal = "&#9473;"
    vertical = "&#9475;"
    last = "&#9495;"
    child = "&#9507;"
    mailbox = "&#128188;"
    envelope = "&#128195;"
    folder = "&#128193;"
    space = "&#8200;"


# noinspection PyTypeChecker
class ReportHTML(Report):

    def __init__(self):
        Report.__init__(self)
        self.tuple: tuple = Doc().ttl()
        self.entries: List[Item] = []
        return

    def _set_symbol(self, item: Item):
        level = item.navigation.level

        if item.is_root is True:
            item.symbols[level + 1] = "{0:s}{1:s}{2:s}".format(Symbol.mailbox.value, Symbol.space.value, item.name)
            item.symbols[0] = Symbol.root.value
            return

        if item.type is Entry.tray:
            item.symbols[level + 1] = "{0:s}{1:s}{2:s}".format(Symbol.folder.value, Symbol.space.value, item.name)
            item.symbols[level] = Symbol.tray.value

        if item.type is Entry.folder:
            item.symbols[level + 1] = "{0:s}{1:s}{2:s}".format(Symbol.envelope.value, Symbol.space.value, item.name)
            item.symbols[level] = Symbol.horizontal.value

        self._set_parent_symbols(item, item.parent, item)
        return

    def _set_parent_symbols(self, work_item: Item, parent: Item, child: Item):

        if parent is None:
            return

        level = parent.navigation.level

        if work_item.parent is parent:
            if work_item.navigation.is_last is False:
                work_item.symbols[level] = Symbol.child.value
            else:
                work_item.symbols[level] = Symbol.last.value

        else:
            if parent.navigation.is_last is True:
                if child.navigation.is_last is False:
                    work_item.symbols[level] = Symbol.vertical.value
            else:
                if child.navigation.is_last is False:
                    work_item.symbols[level] = Symbol.vertical.value

        self._set_parent_symbols(work_item, parent.parent, parent)
        return

    def _create_head(self, head):
        doc, tag, text, line = self.tuple

        with head:
            with tag("title"):
                text("pmconvert: Pegasus Mail Converter: {0:s}".format(self.root.name))

            doc.stag('meta', name='viewport', content='width=device-width, initial-scale=1')
            with tag("style"):
                text(_style)

        return

    def _create_body(self, body):
        doc, tag, text, line = self.tuple

        with body:
            with tag("h2"):
                text("Mailbox Folder Report")

            table = tag("table", id="")
            self._create_table(table)
        return

    def _create_table(self, table):
        doc, tag, text, line = self.tuple
        with table:
            with tag("tr"):
                max_len = len(pmlib.data.root.symbols)
                with tag("th", colspan=max_len, klass="heading"):
                    doc.asis(Symbol.space.value)

                line("th", "Count", klass="heading")
                line("th", "Success", klass="heading")
                line("th", "Failure", klass="heading")

            for _item in self.entries:
                tr = tag("tr")
                self._create_item(tr, _item)
        return

    def _create_item(self, tr, item: Item):
        doc, tag, text, line = self.tuple
        with tr:
            max_len = len(item.symbols)

            for i in range(max_len - 1, -1, -1):
                _symbol = item.symbols[i]
                if _symbol == "":
                    item.symbols.pop(i)
                else:
                    break

            colspan = max_len - len(item.symbols) + 1

            if item.type is Entry.tray:
                colspan += 3

            if item.type is Entry.mailbox:
                colspan += 3

            last = len(item.symbols) - 1
            n = 0
            for _symbol in item.symbols:
                if _symbol == "":
                    _symbol = Symbol.space.value

                if (n == last) and (colspan != 0):
                    with tag("td", klass="tree", colspan=colspan):
                        doc.asis(_symbol)
                else:
                    with tag("td", klass="tree"):
                        doc.asis(_symbol)
                n += 1

            if item.type is Entry.folder:
                line("td", "{0:d}".format(item.report.count))
                line("td", "{0:d}".format(item.report.success))
                line("td", "{0:d}".format(item.report.failure))
        return

    def _sort_entries(self, item: Item):

        for _items in sorted(item.children, key=sort_items):
            if _items.type is Entry.folder:
                self.entries.append(_items)

        for _items in sorted(item.children, key=sort_items):
            if _items.type is Entry.tray:
                self.entries.append(_items)
                self._sort_entries(_items)
        return

    def create(self) -> bool:
        for _item in pmlib.data.entries:
            symbols = []
            for _ in range(pmlib.data.level + 2):
                symbols.append("")

            _item.symbols = symbols

        for _item in pmlib.data.entries:
            self._set_symbol(_item)

        self.entries.append(pmlib.data.root)
        self._sort_entries(pmlib.data.root)

        filename = os.path.abspath(os.path.normpath("{0:s}/report.html".format(pmlib.config.target_path)))
        pmlib.log.inform("REPORT", filename)

        doc, tag, text, line = self.tuple
        doc.asis('<!DOCTYPE html>')
        html = tag("html")

        with html:
            head = tag("head")
            self._create_head(head)

            body = tag("body")
            self._create_body(body)

        result = indent(
            doc.getvalue(),
            indentation='  ',
            newline='\n',
            indent_text=False
        )

        try:
            f = open(filename, "w", encoding="utf-8")
            f.write(result)
            f.close()
        except OSError as e:
            pmlib.log.exception(e)
            return False
        return True
