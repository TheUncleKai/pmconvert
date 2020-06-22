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


# noinspection PyTypeChecker
class Report(object):

    def __init__(self, item: Item):
        self.root: Item = item
        self.tuple: tuple = Doc().ttl()
        return

    def _create_head(self, html):
        doc, tag, text, line = self.tuple

        with html:
            with tag("head"):
                with tag("title"):
                    text("pmconvert: Pegasus Mail Converter: {0:s}".format(self.root.name))

                # doc.stag('meta', ('http-equiv', 'Content-Type'), ('content', 'text/html; charset=utf-8'))
                # doc.stag('meta', ('http-equiv', 'Content-Style-Type'), ('content', 'text/css'))
                doc.stag('meta', name='viewport', content='width=device-width, initial-scale=1')
                with tag("style"):
                    text(__css__)

        return

    def create(self) -> bool:
        filename = os.path.abspath(os.path.normpath("{0:s}/report.html".format(pmlib.config.target_path)))
        pmlib.log.inform("REPORT", filename)

        doc, tag, text, line = self.tuple
        doc.asis('<!DOCTYPE html>')
        html = tag("html")

        self._create_head(html)

        result = indent(
            doc.getvalue(),
            indentation='    ',
            newline='\n',
            indent_text=True
        )

        try:
            f = open(filename, "w")
            f.write(result)
            f.close()
        except OSError as e:
            pmlib.log.exception(e)
            return False
        return True
