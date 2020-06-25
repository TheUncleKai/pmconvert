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

import pmlib

from yattag import Doc, indent
from pmlib.item import Item, sort_items

from pmlib.report import Report
from pmlib.report.js import report_script
from pmlib.types import Entry


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

.folder {
    cursor: pointer;
    -webkit-user-select: none; /* Safari 3.1+ */
    -moz-user-select: none; /* Firefox 2+ */
    -ms-user-select: none; /* IE 10+ */
    user-select: none;
    font-family: Arial, Helvetica, sans-serif;
    padding-top: 12px;
    padding-bottom: 12px;
    color: blue;
    cursor: pointer;
    width: 100%;
    border: none;
    text-align: left;
    outline: none;
    font-size: 14px;
    background-color: #F0FFFF
}

.folder:hover {
    background-color: #F0F8FF;
    font-weight: bold;
}

.tray {
    font-family: Arial, Helvetica, sans-serif;
    cursor: pointer;
    width: 100%;
    border: none;
    text-align: left;
    outline: none;
    font-size: 14px;
    padding-top: 12px;
    margin-top: 2px;
    margin-bottom: 2px;
}

"""


# noinspection PyTypeChecker
class ReportHTML(Report):

    def __init__(self):
        Report.__init__(self)
        self.tuple: tuple = Doc().ttl()
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

    def _create_report(self, div, item: Item):
        doc, tag, text, line = self.tuple
        with div:
            with tag("table"):
                with tag("tr"):
                    line("td", "Folder", klass="firstcolumn")
                    line("td", "{0:s}".format(item.report.filename))
                with tag("tr"):
                    line("td", "Mails", klass="firstcolumn")
                    line("td", "{0:d}".format(item.report.count))
                with tag("tr"):
                    line("td", "Success", klass="firstcolumn")
                    line("td", "{0:d}".format(item.report.success))
                if item.report.failure != 0:
                    with tag("tr"):
                        line("td", "Failure", klass="firstfailure")
                        line("td", "{0:d}".format(item.report.failure))
        return

    def _create_table(self, table):
        doc, tag, text, line = self.tuple
        with table:

            line("th", colspan="")

            with tag("span", klass="caret"):
                text(item.name)

            ul = tag("ul", klass="nested")
            with ul:
                for _item in sorted(item.children, key=sort_items):
                    if _item.type is Entry.folder:
                        with tag("li"):
                            with tag("button", type="button", klass="folder"):
                                text("{0:s} ({1:d})".format(_item.name, _item.report.count))
                            div = tag("div", klass="content")
                            self._create_report(div, _item)

                for _item in sorted(item.children, key=sort_items):
                    if _item.type is Entry.tray:
                        _li = tag("li", klass="tray")
                        self._create_item(_li, _item)
        return

    def _create_body(self, body):
        doc, tag, text, line = self.tuple

        with body:
            with tag("h2"):
                text("Mailbox Folder Report")

            table = tag("table", id="")


        return

    def create(self) -> bool:
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
            f = open(filename, "w")
            f.write(result)
            f.close()
        except OSError as e:
            pmlib.log.exception(e)
            return False
        return True
