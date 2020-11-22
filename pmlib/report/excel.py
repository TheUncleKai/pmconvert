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

        self.column_tree: int = 0
        self.column_count: int = 1
        self.column_success: int = 2
        self.column_failure: int = 3
        self.column_filter: int = 4
        return

    def format_symbol(self, symbol: Symbol, item: Item) -> str:
        symbol_value = self.get_symbol(symbol)
        space = self.get_symbol(Symbol.space)
        ret = "{0:s}{1:s}{2:s}".format(symbol_value, space, item.name)
        return ret

    def get_symbol(self, symbol: Symbol) -> str:
        if symbol is Symbol.root:
            return chr(0x2510)

        if symbol is Symbol.tray:
            return chr(0x252C)

        if symbol is Symbol.horizontal:
            return chr(0x2500)

        if symbol is Symbol.vertical:
            return chr(0x2502)

        if symbol is Symbol.last:
            return chr(0x2514)

        if symbol is Symbol.child:
            return chr(0x251C)

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

        _columns = [
            "Name",
            "C",
            "+",
            "-",
            "Filter"
        ]

        n = 0
        for _column in _columns:
            self.sheet.write_string(self.row, n, _column, cell_format)
            n += 1

        self.sheet.freeze_panes(1, 0)
        self.row += 1
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

    def _write_item(self, item: Item):
        cell_tree = self.workbook.add_format()
        cell_tree.set_font_name("Lucida Console")
        cell_tree.set_font_size(8)
        cell_tree.set_align("left")
        cell_tree.set_align("vcenter")

        cell_format = self.workbook.add_format()
        cell_format.set_font_name("Arial")
        cell_format.set_font_size(8)
        cell_format.set_align("left")
        cell_format.set_align("vcenter")

        cell_filter = self.workbook.add_format()
        cell_filter.set_font_name("Arial")
        cell_filter.set_font_size(8)
        cell_filter.set_align("left")
        cell_filter.set_align("vcenter")
        cell_filter.set_text_wrap()

        text = ""
        for _symbol in item.symbols:
            if _symbol == "":
                _symbol = self.get_symbol(Symbol.space)
            if text == "":
                text = _symbol
            else:
                text += _symbol

        self.sheet.write_string(self.row, self.column_tree, text, cell_tree)
        self.sheet.write_number(self.row, self.column_count, item.report.count, cell_format)
        self.sheet.write_number(self.row, self.column_success, item.report.success, cell_format)
        self.sheet.write_number(self.row, self.column_failure, item.report.failure, cell_format)
        self.sheet.write_string(self.row, self.column_filter, self._create_filter(item), cell_filter)
        self.row += 1
        return

    def _create_item(self, item: Item):
        self.set_symbol(item)
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

        self.sheet.set_column(0, 0, 50)

        pmlib.log.inform(self.name, "Write number of rows {0:d}".format(self.row))
        try:
            self.workbook.close()
        except xlsxwriter.exceptions.FileCreateError as e:
            pmlib.log.exception(e)
            return False
        return True
