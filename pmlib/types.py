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

from dataclasses import dataclass, field
from enum import Enum
from typing import Match, Union, List, Any

__all__ = [
    "Entry",
    "Source",
    "Target",
    "State",
    "Object",
    "Folder",
    "EntryData",
    "Position"
]


class Entry(Enum):

    unknown = -1
    folder = 0
    tray = 1
    mailbox = 2


class Source(Enum):

    unknown = -1
    pegasus = 0
    unix = 1


class Target(Enum):

    unknown = -1
    mbox = 0
    maildir = 1


class State(Enum):

    unknown = -1
    closed = 0
    open = 1
    closed_unread = 2
    open_unread = 3


@dataclass(init=False)
class Object(object):

    id: str
    name: str
    valid: bool = False

    def __repr__(self):
        return self.id

    def __init__(self, search: Match):
        if search is None:
            return
        self.id = search.group("ID")
        self.name = search.group("Name")
        self.valid = True
        return


@dataclass(init=False)
class Folder(Object):

    folder: str = ""
    type: Source = Source.unknown
    filename: str = ""
    indexname: str = ""

    def __init__(self, search: Match):
        Object.__init__(self, search)
        if search is None:
            return

        self.folder = search.group("Folder")
        self.valid = True
        return


@dataclass(init=False)
class ErrorReport(object):

    number: int = 0
    text: str = ""
    exception: Exception = None


@dataclass(init=False)
class EntryReport(object):

    filename: str = ""
    target_format: Target = Target.unknown
    error: List[ErrorReport] = field(default_factory=list)
    count: int = 0
    success: int = 0
    failure: int = 0


@dataclass(init=False)
class EntryData(object):

    type: Entry = Entry.unknown
    state: State = State.unknown

    data: Union[Object, Folder] = None
    size: int = 0
    count: int = 0
    children: List[Any] = field(default_factory=list)
    target: str = ""
    full_name: str = ""
    parent: Any = None
    parent_id: str = ""
    name: str = ""
    valid: bool = False
    is_root: bool = False
    is_sorted: bool = False
    report: EntryReport = field(default_factory=EntryReport)

    @property
    def id(self) -> str:
        return self.data.id


@dataclass()
class Position(object):

    start: int = 0
    end: int = 0

    @property
    def length(self) -> int:
        return self.end - self.start
