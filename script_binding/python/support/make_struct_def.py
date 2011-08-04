#!/usr/bin/env python
# -*- coding: ascii -*-

import sys

from pyparsing import *

class StructDefConverter(object):
    def __init__(self):
        self._create_parse_grammer()

    def _create_parse_grammer(self):
        identity = Word(alphas + "_", alphanums + "_")
        upcase_identity = Word(srange("[A-Z_]"), srange("[0-9A-Z_]"))
        var_type = Optional("const") + identity + Optional("*")

        rval_type = var_type
        func_type = identity
        arg_list = delimitedList(Group(var_type("type") + identity("id")))
        self.func_ptr_type = Suppress("typedef") + rval_type("rval") + \
                Suppress("(") + Suppress("*") + func_type("name") + \
                Suppress(")") + Suppress("(") + \
                arg_list("args") + Suppress(")") + Suppress(";")
        self.func_ptr_type.ignore(cppStyleComment)

        array_len = Word(nums) | upcase_identity
        array_dec = Suppress("[") + array_len + Suppress("]")
        member_list = OneOrMore(Group(var_type("type") + identity("id") + \
                Optional(array_dec)("len") + Suppress(";")))
        self.struct_type = Optional("typedef")("has_alias") + \
                Suppress("struct") + identity("name") + \
                Suppress("{") + member_list("members") + Suppress("}") + \
                Optional(identity)("alias") + \
                Suppress(";")
        self.struct_type.ignore(cppStyleComment)

    def _to_python_func_ptr_type_def(self, token):
        print token.rval, token.name, token.args
        for a in token.args:
            print a.type, a.id
        return ""

    def _to_python_struct_type_def(self, token):
        print token.has_alias, token.name, token.members, token.alias
        for m in token.members:
            print m.type, m.id, m.len
        return ""

    def run(self, finput):
        self.func_ptr_type_def = []
        self.func_ptr_type_name = []
        self.struct_type_def = []
        with open(finput, "rb") as fd:
            content = fd.read()
            for token, start, end in self.func_ptr_type.scanString(content):
                self.func_ptr_type_name.append(token.name)
                self.func_ptr_type_def.append(
                        self._to_python_func_ptr_type_def(token))
            for token, start, end in self.struct_type.scanString(content):
                self.struct_type_def.append(
                        self._to_python_struct_type_def(token))

        all_def = []
        all_def.extend(self.func_ptr_type_def)
        all_def.extend(self.struct_type_def)

        return "\n".join(all_def)

if __name__ == "__main__":
    converter = StructDefConverter()
    content = converter.run("preeditor.h")
    if content:
        print content

    sys.exit(0)
