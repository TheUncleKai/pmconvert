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

__all__ = [
    "report_style"
]

report_style = """

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

.activetray {
    display: block;
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

.active::before {
    content: '\\25C6';
    color: black;
    display: inline-block;
    margin-right: 6px;
}

.active {
    font-family: Arial, Helvetica, sans-serif;
    background-color: #FFFFFF;
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

.content {
    box-shadow: 0 4px 8px 0 rgba(0, 0, 0, 0.2);
    padding-top: 20px; 
    padding-left: 20px; 
    display: none;
    overflow: hidden;
    width: 100%;
    background-color: #F0FFFF;
    margin-bottom: 6px;
}

.firstcolumn {
    width: 30%;
    font-weight: bold;
}

.firstfailure {
    width: 30%;
    color: red;
    font-weight: bold;
}


"""
