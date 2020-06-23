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
  content: '\\25B6';
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

.active {
  display: block;
}
"""

__script__ = """
var toggler = document.getElementsByClassName("caret");
var i;

for (i = 0; i < toggler.length; i++) {
  toggler[i].addEventListener("click", function() {
    this.parentElement.querySelector(".nested").classList.toggle("active");
    this.classList.toggle("caret-down");
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

            # doc.stag('meta', ('http-equiv', 'Content-Type'), ('content', 'text/html; charset=utf-8'))
            # doc.stag('meta', ('http-equiv', 'Content-Style-Type'), ('content', 'text/css'))
            doc.stag('meta', name='viewport', content='width=device-width, initial-scale=1')
            with tag("style"):
                text(__css__)

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
                        line("li", _item.name)

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
