#!/usr/bin/env python
# -*- coding: ascii -*-

import sys

from pyparsing import *

def parse_file_for_func_dec(content):
    results = []

    identity = Word(alphas + "_", alphanums + "_")
    var_type = Optional("const") + identity + Optional("*") + Optional("*")
    rval_type = var_type
    arg_list = delimitedList(Group(var_type("type") + identity("name")))
    func_dec = rval_type("rval") + identity("name") + Suppress("(") + \
            arg_list("args") + Suppress(")") + Suppress(";")
    func_dec.ignore(cppStyleComment)

    for token, start, end in func_dec.scanString(content):
        print token.name, token.rval
        for a in token.args:
            print " -", a.type, a.name
        print
        results.append((token.rval, token.name, token.args))

    return results

def generate_ctypes_func_dec(finput):
    with open(finput, "rb") as fd:
        results = parse_file_for_func_dec(fd.read())
        print len(results)

if __name__ == "__main__":
    """
    iterate each c header files under a directory
    for each header file, generate the corresponding function declaration
    """
    finput = "ftk_widget.h"
    generate_ctypes_func_dec(finput)
    sys.exit(0)
