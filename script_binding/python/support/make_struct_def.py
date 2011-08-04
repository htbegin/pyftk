#!/usr/bin/env python
# -*- coding: ascii -*-

import sys
import textwrap

from pyparsing import *

class StructDefConverter(object):
    def __init__(self):
        self._create_parse_grammer()
        self._create_type_dict("typedef")

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

    def _create_type_dict(self, fname):
        self.type_dict = {
                "void" : "None",
                "char" : "c_byte",
                "unsigned char" : "c_ubyte",
                "short" : "c_short",
                "unsigned short" : "c_ushort",
                "int" : "c_int",
                "unsigned int" : "c_uint",
                "long" : "c_long",
                "unsigned long" : "c_ulong",
                "long long" : "c_longlong",
                "unsigned long long" : "c_ulonglong",
                "float" : "c_float",
                "double" : "c_double",
                "long double" : "c_longdouble",
                "const char *" : "c_char_p",
                "const unsigned char *" : "c_char_p",
                "void *" : "c_void_p",
                }

        if fname is None:
            return

        with open(fname, "rb") as fd:
            for idx, line in enumerate(fd.readlines()):
                line = line.strip()
                if not line or line.startswith("#"):
                    continue
                key, val = line.split("=", 1)
                key = key.strip()
                val = val.strip()
                if not key or not val:
                    sys.stderr.write("invalid line %d: incomplete k-v pair\n" % idx + 1)
                    continue
                if key in self.type_dict:
                    sys.stderr.write("invalid line %d: invalid key '%s'\n" % (idx + 1, key))
                    continue
                self.type_dict[key] = val

    def _type_str(self, tinfo):
        type_str = " ".join(tinfo)
        if type_str in self.type_dict:
            return self.type_dict[type_str]

        if (tinfo[0] == "char" or (tinfo[0] == "unsigned char")) and tinfo[1] == "*":
            sys.stderr.write("unhandled type '%s'\n" % type_str)
            return None

        last_idx = len(tinfo) - 1
        while tinfo[last_idx] == "*":
            deref_type_str = " ".join(tinfo[0:last_idx])
            if deref_type_str in self.type_dict:
                prefix_str = "POINTER(" * (len(tinfo) - last_idx)
                suffix_str = ")" * (len(tinfo) - last_idx)
                return "".join((prefix_str, self.type_dict[deref_type_str], suffix_str))
            last_idx -= 1

        sys.stderr.write("unknown type '%s'\n" % type_str)
        return None

    """
    typedef const char * (*FtkXulTranslateText)(void * ctx, const char * text);
    ['const', 'char', '*'] FtkXulTranslateText [['void', '*', 'ctx'], ['const', 'char', '*', 'text']]
    FtkXulTranslateText = CFUNCTYPE(c_char_p, c_void_p, c_char_p)
    """
    def _exceptional_func_ptr_type_def_str(self, token):
        rval_type_str = " ".join(token.rval)
        func_name_str = token.name
        arg_str_list = []
        for arg in token.args:
            arg_str = " ".join(arg)
            arg_str_list.append(arg_str)
        args_str = ", ".join(arg_str_list)
        line = "".join(("#typedef ", rval_type_str, " (*", func_name_str, ")",
            "(", args_str, ");"))
        return line

    def _to_python_func_ptr_type_def(self, token):
        """
        print token.rval, token.name, token.args
        for a in token.args:
            print a.type, a.id
        """

        rval_type_str = self._type_str(token.rval)
        if rval_type_str is None:
            return self._exceptional_func_ptr_type_def_str(token)
        assert isinstance(rval_type_str, str)

        func_ptr_type_name = token.name
        assert isinstance(rval_type_str, str)

        line_content = [func_ptr_type_name, rval_type_str]
        for arg in token.args:
            arg_type_str = self._type_str(arg.type)
            if arg_type_str is None:
                return self._exceptional_func_ptr_type_def_str(token)
            assert isinstance(arg_type_str, str)
            line_content.append(arg_type_str)

        """
        FtkXulTranslateText = CFUNCTYPE(c_char_p, c_void_p, c_char_p)
        """
        line_fmt = "".join(("%s = CFUNCTYPE(%s, ",
            ", ".join(("%s",) * len(token.args)), ")"))
        line = line_fmt % tuple(line_content)
        return line

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
