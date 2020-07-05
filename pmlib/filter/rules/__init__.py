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
]


# =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
# Headers...

#  If header "T" contains "ubuntu-security-announce@lists.ubuntu.com" Move "2Q76BD9H:22D9:FOL034E4"

#  T: To
#  F: From
#  C: Cc
#  S: Subject
#  R: Reply-to
#  E: Sender

#  contains
#  is

# =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
# Expression...

#  If expression headers matches "From: <tech@kpslashhaven.net>" Move "YZDNYMAS:3D5D:FOL00816"
#  If expression body matches "Return-path: <do-not-reply@archiveofourown.org>" Move "MDJIPSSK:0830:FOL00B44"
#  If expression both matches "Return-path: <do-not-reply@archiveofourown.org>" Move "MDJIPSSK:0830:FOL00B44"

# =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
# Message size...

#  If size > 50000 Move "BNNW0F27:6321:FOL04467"
#  If size < 50000 Move "BNNW0F27:6321:FOL04467"

# =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
# Message date...

#  If date between 0 and 50 Move "BNNW0F27:6321:FOL04467"
#  If date absolute between 280501000000 and 280601000000
#    Move "BNNW0F27:6321:FOL04467"

# =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
# Message age...

#  If age older than 50 Move "BNNW0F27:6321:FOL04467"
#  If age absolute older than 280501000000 Move "BNNW0F27:6321:FOL04467"
