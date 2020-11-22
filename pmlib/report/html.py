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

import pmlib

from yattag import Doc, indent
from pmlib.item import Item, sort_items

from pmlib.types import Entry
from pmlib.report import Reporter, Symbol

report = "ReportHTML"

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


# noinspection PyTypeChecker
class ReportHTML(Reporter):

    def __init__(self):
        Reporter.__init__(self)
        self.name = "HTML"
        self.desc = "Create HTML report"
        self.tuple: tuple = Doc().ttl()
        self.entries: List[Item] = []
        return

    def format_symbol(self, symbol: Symbol, item: Item) -> str:
        symbol_value = self.get_symbol(symbol)
        space = self.get_symbol(Symbol.space)
        ret = "{0:s}{1:s}{2:s}".format(symbol_value, space, item.name)
        return ret

    def get_symbol(self, symbol: Symbol) -> str:
        if symbol is Symbol.root:
            return "&#9491;"

        if symbol is Symbol.tray:
            return "&#9523;"

        if symbol is Symbol.horizontal:
            return "&#9473;"

        if symbol is Symbol.vertical:
            return "&#9475;"

        if symbol is Symbol.last:
            return "&#9495;"

        if symbol is Symbol.child:
            return "&#9507;"

        if symbol is Symbol.mailbox:
            return "&#128188;"

        if symbol is Symbol.envelope:
            return "&#128195;"

        if symbol is Symbol.folder:
            return "&#128193;"

        if symbol is Symbol.space:
            return "&#8200;"

        return "&#8200;"

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
                    doc.asis(self.get_symbol(Symbol.space))

                line("th", "Count", klass="heading")
                line("th", "Success", klass="heading")
                line("th", "Failure", klass="heading")
                line("th", "Filter", klass="heading")

            for _item in self.entries:
                if _item.valid is False:
                    continue
                tr = tag("tr")
                self._create_item(tr, _item)
        return

    @staticmethod
    def _create_filter(item: Item) -> str:
        _filter = ""

        n = 0
        for _rule in item.rules:
            line = str(_rule)

            if n == 0:
                _filter = line
            else:
                _filter = "{0:s}\n{1:s}".format(_filter, line)

        return _filter

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
                colspan += 4

            if item.type is Entry.mailbox:
                colspan += 4

            last = len(item.symbols) - 1
            n = 0
            for _symbol in item.symbols:
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
                line("td", self._create_filter(item))
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
            self.set_symbol(_item)

        self.entries.append(pmlib.data.root)
        self._sort_entries(pmlib.data.root)

        filename = os.path.abspath(os.path.normpath("{0:s}/report.html".format(pmlib.config.target_path)))
        pmlib.log.inform(self.name, filename)

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
