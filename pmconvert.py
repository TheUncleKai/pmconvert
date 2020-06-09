#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
@namespace analyzertools

Base namespace analyzertools application.
"""

import sys
import os
import re
import colorama
import traceback

from optparse import OptionParser
from enum import Enum, unique


@unique
class FileType(Enum):
    STATE = "STATE.PMJ"
    HIERARCH = "HIERARCH.PM"


@unique
class ItemType(Enum):
    FOLDER = 0
    TRAY = 1


def _create_scheme(style="", fore="", back=""):
    scheme = ""

    text_style = None
    text_fore = None
    text_back = None

    if style != "":
        text_style = getattr(colorama.Style, style)

    if fore != "":
        text_fore = getattr(colorama.Fore, fore)

    if back != "":
        text_back = getattr(colorama.Back, back)

    if text_style is not None:
        scheme += text_style

    if text_fore is not None:
        scheme += text_fore

    if text_back is not None:
        scheme += text_back
    return scheme


def _write_stdout(content, raw=False):
    sys.stdout.write(content)
    if raw is True:
        return
    sys.stdout.write("\n")
    return


def _write_stderr(content, raw=False):
    sys.stderr.write(content)
    if raw is True:
        return
    sys.stderr.write("\n")
    return


class Log(object):

    def __init__(self):
        self.reset = colorama.Style.RESET_ALL
        self.LabelNum = 15
        self.Seperator = "| "
        return

    def inform(self, tag, text):

        scheme = _create_scheme("BRIGHT", "GREEN")

        content = self.reset + scheme + " " + tag.ljust(self.LabelNum) + self.Seperator + self.reset + text
        _write_stdout(content)
        return

    def warn(self, tag, text):

        scheme = _create_scheme("BRIGHT", "MAGENTA")

        content = self.reset + scheme + " " + tag.ljust(self.LabelNum) + self.Seperator + self.reset + text
        _write_stdout(content)
        return

    def error(self, text):

        scheme = _create_scheme("BRIGHT", "RED")
        tag = "ERROR"

        content = self.reset + scheme + " " + tag.ljust(self.LabelNum) + self.Seperator + self.reset + text
        _write_stderr(content)
        return

    def log_traceback(self):
        """Log most recent exception.

        @param
            self: The object pointer. (LOG)
        """

        ttype, value, tb = sys.exc_info()
        self.error("Uncaught exception")
        self.error("Type:      " + str(ttype))
        self.error("Value:     " + str(value))

        lines = traceback.format_tb(tb)
        for line in lines:
            _write_stderr(line, True)
        return

    def exception(self, e):

        scheme = _create_scheme("BRIGHT", "RED")
        tag = "EXCEPTION"
        text = str(e)

        content = self.reset + scheme + " " + tag.ljust(self.LabelNum) + self.Seperator + self.reset + text
        _write_stderr(content)
        return


colorama.init()
log = Log()


class Item(object):

    def __init__(self):

        # 1
        self.Type = None

        # 2
        self.Flags = 0

        # 3a
        self.UID = ""

        # 3b
        self.Entry = ""

        # 4
        self.ParentID = ""

        # 4
        self.Parent = None

        # 5
        self.Name = ""
        self.Children = []
        self.Level = 0
        self.Pos = 0
        self.Max = 0
        self.Filename = ""
        return

    def _get_parent_uid(self, parent):
        re_entry = re.compile("(?P<UID>[a-zA-Z0-9]+):(?P<Parent>.+)")

        m = re_entry.search(parent)
        if m:
            self.ParentID = m.group('UID')
            return True

        return False

    def _get_uid(self, uid):
        re_file = re.compile("(?P<UID>[a-zA-Z0-9]+):(?P<SUID>[a-zA-Z0-9]+):(?P<Filename>.+)")
        re_entry = re.compile("(?P<UID>[a-zA-Z0-9]+):(?P<Entry>.+)")

        m = re_file.search(uid)
        if m:
            self.UID = m.group('UID')
            self.Entry = m.group('Filename')
            return True

        m = re_entry.search(uid)
        if m:
            self.UID = m.group('UID')
            self.Entry = m.group('Entry')
            return True

        return False

    def parse(self, line):
        line = line.replace("\"", "")
        items = line.split(",")

        count = len(items)
        if (count != 5) and (count != 7):
            log.error("Invalid item size: " + str(count))
            log.error(line)
            return False

        item_type = int(items[0])

        try:
            self.Type = ItemType(item_type)
        except:
            log.error("Invalid type: " + str(item_type))
            return False

        self.Flags = items[1]
        self.Name = str(items[4])

        uid = str(items[2])
        check = self._get_uid(uid)
        if check is False:
            return False

        parent = str(items[3])
        check = self._get_parent_uid(parent)
        if check is False:
            return False

        if self.Name == "Name_Unavailable":
            return False

        return True

    def info(self):
        count = len(self.Children)
        if count > 0:
            log.inform(self.Name, str(count) + " children")
        return


class Main(object):

    def __init__(self):
        self.Parser = OptionParser("usage: %prog [options]")
        self.Options = None
        self.Input = ""
        self.Output = ""
        self.Hierarchy = ""
        self.State = ""
        self.Root = None
        self.Entries = {}
        self.Tree = ""
        self.IsTree = False
        return

    def init(self):
        self.Parser.add_option("-o", "--output", help="store data in OUTPUT", metavar="OUTPUT", type="string")
        self.Parser.add_option("-i", "--input", help="store data in INPUT", metavar="INPUT", type="string")
        self.Parser.add_option("-t", "--tree", help="add a tree file", action="store_true")

        (options, args) = self.Parser.parse_args()

        if not options.input:
            log.error("Missing input!")
            return False

        if not options.output:
            log.error("Missing output!")
            return False

        if options.tree:
            self.IsTree = True

        input_path = os.path.realpath(options.input)
        self.Output = os.path.realpath(options.output)

        check = os.path.exists(input_path)
        if check is False:
            log.error("Does not exists: " + input_path)
            return False

        self.Input = input_path

        hierarch = os.path.normpath(input_path + "/" + FileType.HIERARCH.value)
        if os.path.exists(hierarch) is False:
            log.error("Not found: " + hierarch)
            return False

        self.Hierarchy = hierarch

        state = os.path.normpath(input_path + "/" + FileType.STATE.value)
        if os.path.exists(state) is False:
            log.error("Not found: " + state)
            return False

        self.State = state

        log.inform("PARSE", "State:     " + self.State)
        log.inform("PARSE", "Hierarchy: " + self.Hierarchy)
        return True

    def parse(self):
        f = open(self.State, 'r')

        re_default = re.compile("DEFAULT=[0-9]+,[0-9]+,[0-9]+,[0-9]+,\"(?P<UID>[a-zA-Z0-9]+):(?P<Name>.+)\"")

        for line in f:
            line = line.replace("\r\n", "")
            line = line.replace("\n", "")

            m = re_default.search(line)
            if m:
                root = Item()
                root.Name = m.group('Name')
                root.UID = m.group('UID')
                self.Root = root
                break
            continue
        f.close()

        if self.Root is None:
            log.error("Root not found!")
            return False

        log.inform("ROOT", self.Root.Name + " (" + self.Root.UID + ")")

        f = open(self.Hierarchy, 'r')
        for line in f:
            line = line.replace("\r\n", "")
            line = line.replace("\n", "")

            item = Item()
            check = item.parse(line)
            if check is True:
                if list(self.Entries).count(item.UID) != 0:
                    log.warn("ITEM", "Duplicate UID for " + item.Name + " (" + item.UID + ")")
                    continue
                log.inform("ADD", item.Type.name + ": " + item.Name + " (" + item.UID + ")")
                self.Entries[item.UID] = item
        f.close()
        return True

    def _sort_entries(self, entries):
        names = {}

        for entry in list(entries):
            names[entry.Name] = entry

        newlist = []

        for key in sorted(list(names)):
            newlist.append(names[key])

        return newlist

    def _get_children(self, uid):
        children = []

        keys = list(self.Entries)
        for key in keys:
            entry = self.Entries[key]
            if entry.ParentID == uid:
                children.append(entry)

        newlist = self._sort_entries(children)
        return newlist

    def _parse_children(self, entry):

        if entry.Type == ItemType.FOLDER:
            path = os.path.normpath(self.Input + "/" + entry.Entry + ".PMM")
            if os.path.exists(path):
                entry.Filename = path

        children = self._get_children(entry.UID)
        count = len(children)

        for child in children:
            child.Parent = entry
            entry.Children.append(child)

        for child in children:
            self._parse_children(child)

        entry.info()
        return

    def _show_tree_item(self, entry):
        level = entry.Level

        show = ""

        if level == 0:
            show = "* " + entry.Name + "\n"
            return show

        sep = ""
        item = entry

        while True:
            if item is None:
                break

            n = item.Level

            if n == level:
                if item.Pos == item.Max:
                    sep = "`-- " + item.Name
                else:
                    sep = "+-- " + item.Name

            if n < level:
                if item.Pos == item.Max:
                    sep = "    " + sep
                else:
                    sep = "|   " + sep

            item = item.Parent

        if (entry.Type == ItemType.FOLDER) and (entry.Filename != ""):
            show = sep.ljust(60) + entry.Filename + "\n"
        else:
            show = sep + "\n"

        return show

    def _create_tree(self, entry=None, level=0):

        if entry is None:
            entry = self.Root
            level = 0
            self.Show = ""

        entry.Level = level

        self.Tree += self._show_tree_item(entry)

        max = len(entry.Children)
        if max > 0:
            level += 1

        n = 1
        for child in entry.Children:
            child.Pos = n
            child.Max = max
            self._create_tree(child, level)
            n += 1
        return

    def build_tree(self):
        self._parse_children(self.Root)
        self._create_tree()

        if self.IsTree is False:
            return

        path = os.path.normpath("tree.txt")
        log.inform("TREE", "Write tree: " + path)
        f = open(path, "w", encoding="utf-8", newline="\n")
        # f.write(str.encode(self.Tree))
        f.write(self.Tree)
        f.close()
        return

if __name__ == '__main__':
    main = Main()
    check = main.init()
    if check is False:
        sys.exit(1)

    check = main.parse()
    main.build_tree()
    sys.stdout.write(main.Show)
    sys.stdout.write("\n")
