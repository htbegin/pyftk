#!/usr/bin/env python
# -*- coding: ascii -*-

import sys
import os
from optparse import OptionParser
import fnmatch
import re
import textwrap

from pyparsing import *

class C2PythonConverter(object):
    def __init__(self, typedef_fname=None):
        self._create_parse_grammer()
        self._create_type_dict(typedef_fname)
        self._create_pointer_ptn()

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
        upcase_identity = Word(srange("[A-Z_]"), srange("[0-9A-Z_]"))
        var_type = Optional("const") + (atom_var_type | identity) + \
                Optional("*") + Optional("*")

        rval_type = var_type
        void_arg_list = Literal("void")
        no_void_arg_list = delimitedList(Group(var_type("type") + identity("name")))
        arg_list = Group(void_arg_list | no_void_arg_list)
        self.func_dec = rval_type("rval") + identity("name") + Suppress("(") + \
                arg_list("args") + Suppress(")") + Suppress(";")
        self.func_dec.ignore(cppStyleComment)

        self.func_ptr_type = Suppress("typedef") + rval_type("rval") + \
                Suppress("(") + Suppress("*") + identity("name") + \
                Suppress(")") + Suppress("(") + \
                no_void_arg_list("args") + Suppress(")") + Suppress(";")
        self.func_ptr_type.ignore(cppStyleComment)

        array_len = Word(nums) | upcase_identity
        array_dec = Suppress("[") + array_len + Suppress("]")
        member_list = OneOrMore(Group(var_type("type") + identity("name") + \
                Optional(array_dec)("len") + Suppress(";")))
        self.struct_type = Optional("typedef")("has_alias") + \
                Suppress("struct") + identity("name") + \
                Suppress("{") + member_list("members") + Suppress("}") + \
                Optional(identity)("alias") + \
                Suppress(";")
        self.struct_type.ignore(cppStyleComment)

        self.struct_alias = Suppress("typedef") + Suppress("struct") + \
                identity("name") + identity("alias") + Suppress(";")
        self.struct_alias.ignore(cppStyleComment)

    def _create_type_dict(self, fname):
        self.type_dict = {
                "void" : "None",
                "char" : "ctypes.c_byte",
                "unsigned char" : "ctypes.c_ubyte",
                "short" : "ctypes.c_short",
                "unsigned short" : "ctypes.c_ushort",
                "int" : "ctypes.c_int",
                "unsigned int" : "ctypes.c_uint",
                "long" : "ctypes.c_long",
                "unsigned long" : "ctypes.c_ulong",
                "long long" : "ctypes.c_longlong",
                "unsigned long long" : "ctypes.c_ulonglong",
                "float" : "ctypes.c_float",
                "double" : "ctypes.c_double",
                "long double" : "ctypes.c_longdouble",
                "const char *" : "ctypes.c_char_p",
                "const unsigned char *" : "ctypes.c_char_p",
                "char *" : "ctypes.c_char_p",
                "unsigned char *" : "ctypes.c_char_p",
                "void *" : "ctypes.c_void_p",
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

    def _create_pointer_ptn(self):
        self.pointer_re = re.compile(r"POINTER[(](?P<type>[a-zA-Z_.]+)[)]")

    def _scan_func_decs(self, content):
        results = []

        for token, start, end in self.func_dec.scanString(content):
            results.append([token.rval, token.name, token.args])

        return results

    def _gather_pointer_statistics(self, type_str):
        result = self.pointer_re.search(type_str)
        if result is not None:
            type = result.group('type')
            if type in self.pointer_dict:
                self.pointer_dict[type] += 1
            else:
                self.pointer_dict[type] = 1

    def _in_type_dict(self, type_str):
        if type_str in self.type_dict or type_str in self.private_types:
            return True
        else:
            return False

    def _type_dict_val(self, type_str):
        val = None
        if type_str in self.type_dict:
            val = self.type_dict[type_str]
        elif type_str in self.private_types:
            val = type_str

        if val is not None:
            val = val.replace(self.mpath, "")

        return val

    def _type_str(self, tinfo):
        type_str = " ".join(tinfo)
        if self._in_type_dict(type_str):
            rval = self._type_dict_val(type_str)
            self._gather_pointer_statistics(rval)
            return rval

        last_idx = len(tinfo) - 1
        while tinfo[last_idx] == "*":
            deref_type_str = " ".join(tinfo[0:last_idx])
            if self._in_type_dict(deref_type_str):
                prefix_str = "POINTER(" * (len(tinfo) - last_idx)
                suffix_str = ")" * (len(tinfo) - last_idx)
                rval = "".join((prefix_str,
                    self._type_dict_val(deref_type_str), suffix_str))
                self._gather_pointer_statistics(rval)
                return rval
            last_idx -= 1

        sys.stderr.write("unknown type '%s'\n" % type_str)
        return None

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

        new_results = []
        for alias, line in self.local_struct_type_ptr_dict.iteritems():
            if alias not in redefine_dict.values():
                alias_def = self.local_struct_type_ptr_dict[alias]
                sub_str = "".join(("\n\n", alias_def))
                for line in results:
                    new_line = line.replace(sub_str, "")
                    new_results.append(new_line)
                results = new_results

        redefine_results = []
        for type, alias in redefine_dict.iteritems():
            if alias in self.local_struct_type_ptr_dict:
                continue
            line = "%s = %s" % (alias, type)
            redefine_results.append(line)

        for lines in results:
            for type, alias in redefine_dict.iteritems():
                if alias in self.local_struct_type_ptr_dict:
                    alias_def = self.local_struct_type_ptr_dict[alias]
                    s_idx = lines.find(alias_def)
                    if s_idx != -1:
                        s_idx += len(alias_def)
                        redefine_lines = "".join((lines[:s_idx],
                                lines[s_idx:].replace(type, alias)))
                    else:
                        redefine_lines = lines.replace(type, alias)
                else:
                    redefine_lines = lines.replace(type, alias)
                lines = redefine_lines
            redefine_results.append(redefine_lines)

        return redefine_results

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
            print a.type, a.name
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

        line_fmt = "".join(("%s = CFUNCTYPE(%s, ",
            ", ".join(("%s",) * len(token.args)), ")"))
        line = line_fmt % tuple(line_content)
        return line

    def _create_private_types(self, content):
        self.private_types = []
        self.dec_only_struct_types = {}
        for token, start, end in self.struct_alias.scanString(content):
            if token.alias not in self.type_dict:
                self.private_types.append(token.alias)
            self.dec_only_struct_types[token.name] = token.alias

        for token, start, end in self.struct_type.scanString(content):
            if token.has_alias and token.alias not in self.type_dict:
                self.private_types.append(token.alias)
            if not token.has_alias:
                if token.name in self.dec_only_struct_types:
                    del self.dec_only_struct_types[token.name]

        for token, start, end in self.func_ptr_type.scanString(content):
            if token.name not in self.type_dict:
                self.private_types.append(token.name)

    def _to_python_struct_type_dec(self, name):
        dec_list = []
        struct_ptr = "_%sPtr" % (name,)
        struct_ptr_line = "%s = POINTER(%s)" % (struct_ptr, name)
        self.local_struct_type_ptr_dict[struct_ptr] = struct_ptr_line

        struct_dec_line = "class %s(Structure):\n    pass" % (name,)
        dec_list.append(struct_dec_line)
        dec_list.append(struct_ptr_line)

        return "\n\n".join(dec_list)

    """
    related definitions......
    class FtkXulCallbacks(Structure):
        _fields_ = [
                ('id_a', type_a),
                ('id_b, type_b)
                ]

    class FtkImPreeditor(Structure):
        pass
    related definitions......
    FtkImPreeditor._fields_ = ['id_c' : type_c, 'id_d' : type_d]
    """
    def _exceptional_struct_type_def_str(self, token):
        indent = " " * 4
        name = token.name
        m_str_list = []
        for m in token.members:
            if m.len:
                m_str = "".join((indent, " ".join(m.type),
                    "".join((" ", m.name, "[", m.len[0], "];"))))
            else:
                m_str = "".join((indent, " ".join(m), ";"))
            m_str_list.append(m_str)
        ms_str = "\n".join(m_str_list)
        return '"""\nstruct %s\n{\n%s\n};\n"""' % (name, ms_str)

    def _to_python_struct_type_def(self, token):
        """
        print "------------------------------------------------------"
        print token.has_alias, token.name, token.members, token.alias
        for m in token.members:
            print m.type, m.name, m.len
        print "------------------------------------------------------"
        """
        if token.has_alias:
            name = token.alias
        else:
            name = token.name.lstrip("_")
        struct_ptr = "_%sPtr" % (name,)
        struct_ptr_line = "%s = POINTER(%s)" % (struct_ptr, name)
        self.local_struct_type_ptr_dict[struct_ptr] = struct_ptr_line

        func_ptr_list = []
        m_list = []
        for m in token.members:
            type_str = self._type_str(m.type)
            if type_str is None:
                return self._exceptional_struct_type_def_str(token)

            if type_str in self.func_ptr_type_dict:
                func_ptr_list.append(type_str)

            if m.len:
                alen = m.len[0]
                try:
                    int(alen)
                except ValueError:
                    alen = "".join(("ftk.constants.", alen))
                type_str = " * ".join((type_str, alen))
            m_str = "('%s', %s)" % (m.name, type_str)
            m_list.append(m_str)

        def_list = []
        if token.has_alias:
            for func_ptr in func_ptr_list:
                def_list.append(self.func_ptr_type_dict[func_ptr])
            line_one = "class %s(Structure):" % (name,)
            line_two = "    _fields_ = ["
            line_mems_fmt = ",\n".join((("            %s",) * len(m_list)))
            line_mems = line_mems_fmt % tuple(m_list)
            line_end = "            ]"
            struct_line = "\n".join((line_one, line_two, line_mems, line_end))
            def_list.append(struct_line)
            def_list.append(struct_ptr_line)
        else:
            struct_dec_line = "class %s(Structure):\n    pass" % (name,)
            def_list.append(struct_dec_line)
            def_list.append(struct_ptr_line)
            for func_ptr in func_ptr_list:
                def_list.append(self.func_ptr_type_dict[func_ptr])
            first_line = "%s._fields_ = [" % (name,)
            middle_line_fmt = ",\n".join((("        %s",) * len(m_list)))
            middle_line = middle_line_fmt % tuple(m_list)
            last_line = "        ]"
            struct_line = "\n".join((first_line, middle_line, last_line))
            def_list.append(struct_line)
        return "\n\n".join(def_list)

    def _convert_struct_type_def(self, content):
        self.func_ptr_type_dict = {}
        struct_type_def = []

        for token, start, end in self.func_ptr_type.scanString(content):
            self.func_ptr_type_dict[token.name] = \
                    self._to_python_func_ptr_type_def(token)

        for token, start, end in self.struct_type.scanString(content):
            struct_type_def.append(self._to_python_struct_type_def(token))

        for alias in self.dec_only_struct_types.itervalues():
            struct_type_def.append(self._to_python_struct_type_dec(alias))

        return struct_type_def

    def _convert_func_dec(self, content, func=None):
        decs = []
        func_decs = self._scan_func_decs(content)
        for dec in func_decs:
            if func is not None and func != self._func_dec_name(dec):
                continue
            s = self._func_dec_str(dec)
            decs.append(s)

        if func is not None and len(decs) == 0:
            sys.stderr.write("declaration for function '%s' doesn't exist\n" % func)

        return decs

    def run(self, finput, mpath, struct_enabled, func_enabled):
        self.mpath = mpath
        self.pointer_dict = {}
        self.local_struct_type_ptr_dict = {}

        results = []
        with open(finput, "rb") as fd:
            content = fd.read()

            self._create_private_types(content)

            if struct_enabled:
                defs = self._convert_struct_type_def(content)
            else:
                defs = []
            if func_enabled:
                decs = self._convert_func_dec(content)
            else:
                decs = []

        results.extend(defs)
        results.extend(decs)

        results = self._redefine_pointer(results)

        return "\n\n".join(results)

def strip_symbol_path(path, symbol):
    return symbol.replace(path, "")

if __name__ == "__main__":
    opt_parser = OptionParser()
    opt_parser.add_option("-i", "--input", dest="file",
            help="c header file", metavar="FILE")
    opt_parser.add_option("-m", "--module", dest="m_name",
            help="set the module name manually", metavar="STRING")
    opt_parser.add_option("-s", "--struct", dest="disable_struct",
            action="store_true", default=False,
            help="disable the generation of struct definitions")
    opt_parser.add_option("-f", "--function", dest="disable_func",
            action="store_true", default=False,
            help="disable the generation of function definitions")
    (options, args) = opt_parser.parse_args()

    if options.file is None or not os.path.isfile(options.file) or \
            not fnmatch.fnmatch(options.file, "*.h") or \
            (options.m_name is not None and not isinstance(options.m_name, str)):
        opt_parser.print_help()
        sys.exit(1)

    cfg_file = os.path.join(os.path.dirname(sys.argv[0]), "typedef")
    converter = C2PythonConverter(cfg_file)

    if options.m_name is None:
        fname = os.path.basename(options.file)
        module_name = fname[:-2]
    else:
        module_name = options.m_name

    module_path = module_name
    content = converter.run(options.file, module_path,
            not options.disable_struct, not options.disable_func)

    if content:
        print content

    sys.exit(0)
