#!/usr/bin/env python
# -*- coding: ascii -*-

import sys
import os
from optparse import OptionParser
import fnmatch
import re

from pyparsing import *

class CtypeFuncDecConverter(object):
    def __init__(self, typedef_fname=None):
        self._create_parse_grammer()
        self._create_type_dict(typedef_fname)
        self._create_pointer_info()

    def _create_parse_grammer(self):
        atom_var_type = Literal("void") | \
                Literal("char") | Literal("unsigned char") | \
                Literal("short") | Literal("unsigned short") | \
                Literal("int") | Literal("unsigned int") | \
                Literal("long") | Literal("unsigned long") | \
                Literal("long long") | Literal("unsigned long long") | \
                Literal("float") | Literal("double") | \
                Literal("long double")
        identity = Word(alphas + "_", alphanums + "_")
        var_type = Optional("const") + (atom_var_type | identity) + \
                Optional("*") + Optional("*")
        rval_type = var_type
        void_arg_list = Literal("void")
        no_void_arg_list = delimitedList(Group(var_type("type") + identity("name")))
        arg_list = Group(void_arg_list | no_void_arg_list)
        self.func_dec = rval_type("rval") + identity("name") + Suppress("(") + \
                arg_list("args") + Suppress(")") + Suppress(";")
        self.func_dec.ignore(cppStyleComment)

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

    def _create_pointer_info(self):
        self.pointer_re = re.compile(r"POINTER[(](?P<type>[a-zA-Z_.]+)[)]")
        self.pointer_dict = {}

    def _scan_func_decs(self, content):
        results = []

        for token, start, end in self.func_dec.scanString(content):
            results.append([token.rval, token.name, token.args])

        return results

    def _type_str(self, tinfo):
        result = self._pre_type_str(tinfo)
        if result is not None and self.type_str_post_fn is not None:
            return self.type_str_post_fn(self.ctx, result)
        else:
            return result

    def _pre_type_str(self, tinfo):
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

    def _gather_pointer_statistics(self, type_str):
        result = self.pointer_re.search(type_str)
        if result is not None:
            type = result.group('type')
            if type in self.pointer_dict:
                self.pointer_dict[type] += 1
            else:
                self.pointer_dict[type] = 1

    def _exceptional_func_dec_str(self, func):
        (FUNC_RVAL_IDX, FUNC_NAME_IDX, FUNC_ARGS_IDX) = range(3)

        rval_type = func[FUNC_RVAL_IDX]
        rval_type_str = " ".join(rval_type)

        func_name_str = func[FUNC_NAME_IDX]
        assert isinstance(func_name_str, str)

        arg_info_list = []
        args = func[FUNC_ARGS_IDX]
        if len(args) != 1 or args[0] != "void":
            for arg in args:
                arg_name_str = arg.name
                assert isinstance(arg_name_str, str)

                arg_type_str = " ".join(arg.type)

                arg_info_list.append(" ".join((arg_type_str, arg_name_str)))

        arg_info_str = ", ".join(arg_info_list)
        if not arg_info_str:
            arg_info_str = "void"

        return "\n".join(("'''",
            "".join((rval_type_str, " ", func_name_str,
                "(", arg_info_str, ");")),
            "'''"))

    """
    ftk_window_set_animation_hint = ftk.dll.function('ftk_window_set_animation_hint',
            '',
            args=['thiz', 'hint'],
            arg_types=[ftk.widget.FtkWidgetPtr, c_char_p],
            return_type=c_int)
    """
    def _func_dec_str(self, func):
        (FUNC_RVAL_IDX, FUNC_NAME_IDX, FUNC_ARGS_IDX) = range(3)

        rval_type = func[FUNC_RVAL_IDX]
        rval_type_str = self._type_str(rval_type)
        if rval_type_str is None:
            return self._exceptional_func_dec_str(func)
        assert isinstance(rval_type_str, str)
        self._gather_pointer_statistics(rval_type_str)

        func_name_str = func[FUNC_NAME_IDX]
        assert isinstance(func_name_str, str)

        arg_name_list = []
        arg_type_list = []
        args = func[FUNC_ARGS_IDX]
        if len(args) != 1 or args[0] != "void":
            for arg in args:
                arg_name_str = arg.name
                assert isinstance(arg_name_str, str)
                arg_name_list.append(arg_name_str)

                arg_type_str = self._type_str(arg.type)
                if arg_type_str is None:
                    return self._exceptional_func_dec_str(func)
                assert isinstance(arg_type_str, str)
                self._gather_pointer_statistics(arg_type_str)
                arg_type_list.append(arg_type_str)

        line_one = "%s = ftk.dll.function('%s'," % (func_name_str, func_name_str)
        if len(line_one) > 80:
            line_one_fmt = "".join(("%s = ftk.dll.function(\n",
                " " * 8, "'%s',"))
            line_one = line_one_fmt % (func_name_str, func_name_str)
        line_two = "".join((" " * 8, "'',"))
        line_three_fmt = "".join((" " * 8, "args=[",
            ", ".join(("'%s'",) * len(arg_name_list)),
            "],"))
        line_three = line_three_fmt % tuple(arg_name_list)
        line_four_fmt = "".join((" " * 8, "arg_types=[",
            ", ".join(("%s",) * len(arg_type_list)),
            "],"))
        line_four = line_four_fmt % tuple(arg_type_list)
        line_five = "".join((" " * 8, "return_type=%s)")) % rval_type_str

        return "\n".join((line_one, line_two, line_three, line_four, line_five))

    def _func_dec_name(self, func):
        FUNC_NAME_IDX = 1
        func_name_str = func[FUNC_NAME_IDX]
        assert isinstance(func_name_str, str)
        return func_name_str

    def _get_pointer_type_alias(self, pointer_type):
        lists = pointer_type.split(".")
        return "".join(("_", lists[-1], "Ptr"))

    def _redefine_pointer(self, results):
        REDEFINE_THRESHOLD = 2
        redefine_dict = {}
        for k, v in self.pointer_dict.iteritems():
            if v >= REDEFINE_THRESHOLD:
                alias = self._get_pointer_type_alias(k)
                redefine_dict["".join(("POINTER(", k, ")"))] = alias

        if len(redefine_dict) == 0:
            return results

        redefine_results = []
        for type, alias in redefine_dict.iteritems():
            line = "%s = %s" % (alias, type)
            redefine_results.append(line)

        for lines in results:
            for type, alias in redefine_dict.iteritems():
                redefine_lines = lines.replace(type, alias)
                lines = redefine_lines
            redefine_results.append(redefine_lines)

        return redefine_results

    def run(self, finput, func, type_str_post_fn=None, ctx=None):
        self.type_str_post_fn = type_str_post_fn
        self.ctx = ctx
        results = []
        with open(finput, "rb") as fd:
            func_decs = self._scan_func_decs(fd.read())
            for dec in func_decs:
                if func is not None and func != self._func_dec_name(dec):
                    continue
                s = self._func_dec_str(dec)
                results.append(s)
        if func is not None and len(results) == 0:
            sys.stderr.write("declaration for function '%s' doesn't exist\n" % func)
        results = self._redefine_pointer(results)
        self.pointer_dict = {}
        return "\n\n".join(results)

def strip_symbol_path(path, symbol):
    return symbol.replace(path, "")

if __name__ == "__main__":
    opt_parser = OptionParser()
    opt_parser.add_option("-f", "--file", dest="file",
            help="the path of c header file", metavar="FILE")
    opt_parser.add_option("-d", "--declaration", dest="func",
            help="the name of the specific function", metavar="STRING")
    opt_parser.add_option("-m", "--module", dest="m_name",
            help="set the module name manually", metavar="STRING")
    (options, args) = opt_parser.parse_args()

    if options.file is None or not os.path.isfile(options.file) or \
            not fnmatch.fnmatch(options.file, "*.h") or \
            (options.func is not None and not isinstance(options.func, str)) or \
            (options.m_name is not None and not isinstance(options.m_name, str)):
        opt_parser.print_help()
        sys.exit(1)

    cfg_file = os.path.join(os.path.dirname(sys.argv[0]), "typedef")
    converter = CtypeFuncDecConverter(cfg_file)

    if options.m_name is None:
        fname = os.path.basename(options.file)
        if fnmatch.fnmatch(fname, "ftk_*.h"):
            module_name = fname[4:-2]
        else:
            module_name = fname[0:-2]
    else:
        module_name = options.m_name
    module_path = "".join(("ftk.", module_name, "."))

    content = converter.run(options.file, options.func,
            strip_symbol_path, module_path)
    if content:
        print content

    sys.exit(0)
