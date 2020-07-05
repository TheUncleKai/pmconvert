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
import abc
from abc import ABCMeta
from enum import Enum


class RuleType(Enum):

    Header = "header"
    Expression = "expression"
    Size = "size"
    Date = "date"
    Age = "age"


#     Delete = "Delete"
#     Forward = "Forward"
#     Extract = "eXtract"
#     Append = "Append"
#     Print = "Print"
#     SendTextFile = "SendTextFile"
#     SendBinaryFile = "SendBinaryFile"
#     AddToList = "AddToList"
#     RemoveFromList = "RemoveFromList"
#     RunAProgram = "Run"
#     Highlight = "Highlight"
#     Expire = "Expire"
#     Select = "Select"
#     Exit = "Exit"
#     MarkRead = "MarkRead"
#     PlaySound = "PlaySound"
#     CallLabel = "Call"
#     Return = "Return"
#     GotoLabel = "Goto"
#     SkipNext = "SkipNext"
#     Dialog = "Dialog"
#     SetIdentity = "SetIdentity"
#     LogicalAnd = "LogicalAnd"
#     MarkSignificant = "MarkSignificant"
#     AddHeader = "AddHeader"


class Action(metaclass=ABCMeta):

    def __init__(self):
        self.name: str = ""
        self.filter: str = ""
        return

    @abc.abstractmethod
    def parse(self, data: str) -> bool:
        pass

    @abc.abstractmethod
    def result(self) -> str:
        pass


class Rule(metaclass=ABCMeta):

    def __init__(self):
        self.name: str = ""
        return

    @abc.abstractmethod
    def parse(self, data: str) -> bool:
        pass
