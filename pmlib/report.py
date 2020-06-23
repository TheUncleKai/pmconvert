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
from pmlib.item import Item
from pmlib.types import Entry


__all__ = [
    "Report"
]

__css__ = """
body {
    font-family: Arial, Helvetica, sans-serif;
    font-size: 14px;
}

table {
    border-spacing: 5px;
}

ul, #myUL {
    list-style-type: none;
}

#myUL {
    margin: 0;
    padding: 0;
}

.caret {
    cursor: pointer;
    -webkit-user-select: none; /* Safari 3.1+ */
    -moz-user-select: none; /* Firefox 2+ */
    -ms-user-select: none; /* IE 10+ */
    user-select: none;
}

.caret::before {
    content: '\25B6';
    color: black;
    display: inline-block;
    margin-right: 6px;
}

.caret-down::before {
    -ms-transform: rotate(90deg); /* IE 9 */
    -webkit-transform: rotate(90deg); /* Safari */'
    transform: rotate(90deg);  
}

.nested {
    display: none;
}

.activetray {
    display: block;
}

.folder {
    font-family: Arial, Helvetica, sans-serif;
    padding: 6px;
    color: blue;
    cursor: pointer;
    width: 20%;
    border: none;
    text-align: left;
    outline: none;
    font-size: 14px;
}

.tray {
    font-family: Arial, Helvetica, sans-serif;
    padding: 6px;
    cursor: pointer;
    width: 20%;
    border: none;
    text-align: left;
    outline: none;
    font-size: 14px;
}

.active, .folder:hover {
    font-family: Arial, Helvetica, sans-serif;
    background-color: #00FFFF;
    padding: 12px;
    font-weight: bold;
}

.content {
    box-shadow: 0 4px 8px 0 rgba(0, 0, 0, 0.2);
    padding-top: 20px; 
    padding-left: 20px; 
    padding-bottom: 20px; 
    display: none;
    overflow: hidden;
    width: 80%;
    background-color: #F0FFFF;
    margin-bottom: 30px;
}

.firstcolumn {
    width: 30%;
    font-weight: bold;
}
"""

__script__ = """
var toggler = document.getElementsByClassName("caret");
var coll = document.getElementsByClassName("collapsible");
var i;

for (i = 0; i < toggler.length; i++) {
  toggler[i].addEventListener("click", function() {
    this.parentElement.querySelector(".nested").classList.toggle("activetray");
    this.classList.toggle("caret-down");
  });
}

for (i = 0; i < coll.length; i++) {
  coll[i].addEventListener("click", function() {
    this.classList.toggle("active");
    var content = this.nextElementSibling;
    if (content.style.display === "block") {
      content.style.display = "none";
    } else {
      content.style.display = "block";
    }
  });
}
"""


def _sort_name(item: Item):
    return item.name


# noinspection PyTypeChecker
class Report(object):

    def __init__(self, item: Item):
        self.root: Item = item
        self.tuple: tuple = Doc().ttl()
        return

    def _create_head(self, head):
        doc, tag, text, line = self.tuple

        with head:
            with tag("title"):
                text("pmconvert: Pegasus Mail Converter: {0:s}".format(self.root.name))

            doc.stag('meta', name='viewport', content='width=device-width, initial-scale=1')
            with tag("style"):
                text(__css__)

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
                with tag("tr"):
                    line("td", "failure", klass="firstcolumn")
                    line("td", "{0:d}".format(item.report.failure))
        return

    def _create_item(self, li, item: Item):
        doc, tag, text, line = self.tuple
        with li:
            with tag("span", klass="caret"):
                text(item.name)

            ul = tag("ul", klass="nested")
            with ul:
                for _item in sorted(item.children, key=_sort_name):
                    if _item.type is Entry.folder:
                        with tag("li"):
                            with tag("button", type="button", klass="collapsible"):
                                text(_item.name)
                            div = tag("div", klass="content")
                            self._create_report(div, _item)

                for _item in sorted(item.children, key=_sort_name):
                    if _item.type is Entry.tray:
                        _li = tag("li")
                        self._create_item(_li, _item)
        return

    def _create_body(self, body):
        doc, tag, text, line = self.tuple

        with body:
            with tag("h2"):
                text("Mailbox Folder Report")

            with tag("ul", id="myUL"):
                root = tag("li")
                self._create_item(root, self.root)

            with tag("script"):
                doc.asis(__script__)

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
