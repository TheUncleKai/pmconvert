#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
@namespace analyzertools

Base namespace analyzertools application.
"""

import sys
import os
import configparser

from optparse import OptionParser


class Main(object):

    def __init__(self):
        self.Parser = OptionParser("usage: %prog [options]")
        self.Parser.add_option("-o", "--output", help="store data in OUTPUT", metavar="OUTPUT", type="string")
        self.Parser.add_option("-i", "--input", help="store data in INPUT", metavar="INPUT", type="string")

        (options, args) = self.Parser.parse_args()

        self.Options = options

        if self.Options.input:
            self.Input = os.path.realpath(self.Options.input)

        if self.Options.input:
            self.Output = os.path.realpath(self.Options.output)
        return



if __name__ == '__main__':
    main = Main()
