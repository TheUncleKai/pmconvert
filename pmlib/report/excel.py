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
import xlsxwriter
import xlsxwriter.exceptions

import pmlib
from pmlib.report import Reporter, Symbol
from pmlib.item import Item, sort_items
from pmlib.types import Entry

report = "ReportExcel"

__all__ = [
    "ReportExcel"
]


class ReportExcel(Reporter):

    # noinspection PyTypeChecker
    def __init__(self):
        Reporter.__init__(self)
        self.name = "EXCEL"
        self.desc = "Create Excel report"

        self.workbook: xlsxwriter.Workbook = None
        self.sheet: xlsxwriter.workbook.Worksheet = None
        self.row: int = 0

        self.column_count = 0
        self.column_success = 0
        self.column_failure = 0
        return

    # ┓  9491  2513  BOX DRAWINGS HEAVY DOWN AND LEFT
    # ┳  9523  2533  BOX DRAWINGS HEAVY DOWN AND HORIZONTAL
    # ━  9473  2501  BOX DRAWINGS HEAVY HORIZONTAL
    # ┃  9475  2503  BOX DRAWINGS HEAVY VERTICAL
    # ┗  9495  2517  BOX DRAWINGS HEAVY UP AND RIGHT
    # ┣  9507  2523  BOX DRAWINGS HEAVY VERTICAL AND RIGHT

    def format_symbol(self, symbol: Symbol, item: Item) -> str:
        symbol_value = self.get_symbol(symbol)
        space = self.get_symbol(Symbol.space)
        ret = "{0:s}{1:s}{2:s}".format(symbol_value, space, item.name)
        return ret

    def get_symbol(self, symbol: Symbol) -> str:
        if symbol is Symbol.root:
            return chr(0x2513)

        if symbol is Symbol.tray:
            return chr(0x2533)

        if symbol is Symbol.horizontal:
            return chr(0x2501)

        if symbol is Symbol.vertical:
            return chr(0x2503)

        if symbol is Symbol.last:
            return chr(0x2517)

        if symbol is Symbol.child:
            return chr(0x2523)

        if symbol is Symbol.mailbox:
            return chr(0x1F4BC)

        if symbol is Symbol.envelope:
            return chr(0x1F4C3)

        if symbol is Symbol.folder:
            return chr(0x1F4C1)

        if symbol is Symbol.space:
            return chr(0x2008)

        return ""

    def _create_header(self):
        cell_format = self.workbook.add_format()
        cell_format.set_bottom(5)
        cell_format.set_font_name("Arial")
        cell_format.set_font_size(10)
        cell_format.set_bold()

        level = pmlib.data.level

        _columns = []

        for i in range(0, level + 1):
            _columns.append("")

        _columns.append("Count")
        _columns.append("Success")
        _columns.append("Failure")

        self.column_count = level + 1
        self.column_success = level + 2
        self.column_failure = level + 3

        n = 0
        for _column in _columns:
            self.sheet.write_string(self.row, n, _column, cell_format)
            n += 1

        self.sheet.freeze_panes(1, 0)
        self.row += 1
        return

    def _write_item(self, item: Item):
        cell_format = self.workbook.add_format()
        cell_format.set_font_name("Arial")
        cell_format.set_font_size(10)

        self.sheet.write_string(self.row, item.navigation.level, item.name, cell_format)
        self.sheet.write_number(self.row, self.column_count, item.report.count, cell_format)
        self.sheet.write_number(self.row, self.column_success, item.report.success, cell_format)
        self.sheet.write_number(self.row, self.column_failure, item.report.failure, cell_format)
        self.row += 1
        return

    def _create_item(self, item: Item):
        self._write_item(item)

        for _item in sorted(item.children, key=sort_items):
            if _item.type is Entry.folder:
                self._create_item(_item)

        for _item in sorted(item.children, key=sort_items):
            if _item.type is Entry.tray:
                self._create_item(_item)
        return

    def create(self) -> bool:
        filename = os.path.abspath(os.path.normpath("{0:s}/report.xlsx".format(pmlib.config.target_path)))
        self.workbook = xlsxwriter.Workbook(filename, {'constant_memory': True})
        self.sheet = self.workbook.add_worksheet("Report")

        pmlib.log.inform(self.name, filename)

        self._create_header()
        self._create_item(pmlib.data.root)

        pmlib.log.inform(self.name, "Write number of rows {0:d}".format(self.row))
        try:
            self.workbook.close()
        except xlsxwriter.exceptions.FileCreateError as e:
            pmlib.log.exception(e)
            return False
        return True
