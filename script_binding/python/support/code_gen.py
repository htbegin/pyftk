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
        self.line_width = 79
        self.text_wrapper = textwrap.TextWrapper(width=self.line_width)

    def _create_parse_grammer(self):
        atom_var_type = Literal("void") | \
                Literal("signed char") | \
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
        self.basic_type_dict = {
                "void" : "None",
                "char" : "ctypes.c_byte",
                "signed char" : "ctypes.c_byte",
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
                "size_t" : "ctypes.c_size_t",
                }

        self.ext_type_dict = {}

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
                if self._in_pub_type_dict(key):
                    sys.stderr.write("invalid line %d: invalid key '%s'\n" % (idx + 1, key))
                    continue
                self.ext_type_dict[key] = val

    def _create_pointer_ptn(self):
        self.pointer_re = re.compile(r"ctypes.POINTER[(](?P<type>[a-zA-Z_.]+)[)]")

    def _in_pub_type_dict(self, type_str):
        if type_str in self.basic_type_dict or \
                type_str in self.ext_type_dict:
            return True
        else:
            return False

    def _in_type_dict(self, type_str):
        if self._in_pub_type_dict(type_str) or \
                type_str in self.priv_type_dict:
            return True
        else:
            return False

    def _type_dict_val(self, type_str):
        val = None
        if type_str in self.basic_type_dict:
            val = self.basic_type_dict[type_str]
        elif type_str in self.ext_type_dict:
            val = self.ext_type_dict[type_str]
        elif type_str in self.priv_type_dict:
            val = self.priv_type_dict[type_str]

        if val is not None:
            val = val.replace(self.mpath, "")

        return val

    def _need_create_ptr_type_alias(self, type):
        ptr_type = "ctypes.POINTER(%s)" % type
        if ptr_type in self.ptr_type_ref_cnt_dict:
            return True
        else:
            return False

    def _ptr_type_alias_str(self, type_str):
        result = self.pointer_re.search(type_str)
        if result is not None:
            type = result.group("type")
            ptr_type = result.group(0)
            if ptr_type in self.ptr_type_alias_dict:
                alias = self.ptr_type_alias_dict[ptr_type]
                return type_str.replace(ptr_type, alias)
            if type not in self.basic_type_dict.values() and \
                    self._need_create_ptr_type_alias(type):
                parts = type.split(".")
                alias = "_%sPtr" % parts[-1]
                self.ptr_type_alias_dict[ptr_type] = alias
                return type_str.replace(ptr_type, alias)
            else:
                return type_str
        else:
            sys.stderr.write("invalid pointer type %s\n" % type_str)
            return type_str

    def _type_str(self, tinfo):
        type_str = " ".join(tinfo)
        if self._in_type_dict(type_str):
            rval = self._type_dict_val(type_str)
            return rval

        if tinfo[0] is "const":
            first_idx = 1
        else:
            first_idx = 0
        last_idx = len(tinfo) - 1
        while tinfo[last_idx] == "*":
            deref_type_str = " ".join(tinfo[first_idx:last_idx])
            if self._in_type_dict(deref_type_str):
                prefix_str = "ctypes.POINTER(" * (len(tinfo) - last_idx)
                suffix_str = ")" * (len(tinfo) - last_idx)
                rval = "".join((prefix_str,
                    self._type_dict_val(deref_type_str), suffix_str))
                if self._enable_ptr_type_alias:
                    rval = self._ptr_type_alias_str(rval)
                return rval
            last_idx -= 1

        sys.stderr.write("unknown type '%s'\n" % type_str)
        return None

    def _exceptional_func_dec_str(self, token):
        rval_type = token.rval
        rval_type_str = " ".join(rval_type)

        func_name_str = token.name
        assert isinstance(func_name_str, str)

        arg_info_list = []
        args = token.args
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
    ftk_window_set_animation_hint = ftk_dll.function(
            'ftk_window_set_animation_hint',
            '',
            args=['thiz', 'hint'],
            arg_types=[ftk_widget.FtkWidgetPtr, ctypes.c_char_p],
            return_type=ctypes.c_int)
    """
    def _to_python_func_dec(self, token, only_check_type=False):
        all_line = []
        enable_check_return = False
        enable_dereference_return = False
        enable_require_return = False

        rval_type = token.rval
        rval_type_str = self._type_str(rval_type)
        if rval_type_str is None:
            if not only_check_type:
                return self._exceptional_func_dec_str(token)
            else:
                return None
        assert isinstance(rval_type_str, str)
        if only_check_type:
            self._update_global_info(rval_type_str, in_func_dec=True)

        func_name_str = token.name
        assert isinstance(func_name_str, str)

        arg_name_list = []
        arg_type_list = []
        args = token.args
        if len(args) != 1 or args[0] != "void":
            for arg in args:
                arg_name_str = arg.name
                assert isinstance(arg_name_str, str)
                arg_name_list.append(arg_name_str)

                arg_type_str = self._type_str(arg.type)
                if arg_type_str is None:
                    if not only_check_type:
                        return self._exceptional_func_dec_str(token)
                    else:
                        return None
                assert isinstance(arg_type_str, str)
                if only_check_type:
                    self._update_global_info(arg_type_str, in_func_dec=True)
                else:
                    if arg_type_str in self.func_ptr_type_ref_dict and \
                            self.func_ptr_type_ref_dict[arg_type_str] == 0:
                        self._update_func_ptr_type_ref_info(arg_type_str)
                        line = "".join((
                                self.func_ptr_type_def_dict[arg_type_str],
                                "\n"))
                        all_line.append(line)
                arg_type_list.append(arg_type_str)

        if only_check_type:
            return None

        extra_line = 0
        if rval_type[0] == "Ret":
            enable_check_return = True
            extra_line += 1
        if rval_type_str.startswith("ctypes.POINTER") or \
                rval_type_str in self.ptr_type_alias_dict.values():
            enable_dereference_return = True
            extra_line += 1
            if func_name_str.endswith("_create") or \
                    func_name_str.endswith("_create_ex"):
                enable_require_return = True
                extra_line += 1

        indent = " " * 8

        line = "%s = ftk_dll.function('%s'," % (func_name_str, func_name_str)
        if len(line) <= self.line_width:
            all_line.append(line)
        else:
            line = "%s = ftk_dll.function(" % func_name_str
            all_line.append(line)
            line = "%s'%s'," % (indent, func_name_str)
            all_line.append(line)

        line = "".join((indent, "'',"))
        all_line.append(line)

        self.text_wrapper.initial_indent = ""
        self.text_wrapper.subsequent_indent = " " * 12

        line_fmt = "".join((indent, "args=[",
            ", ".join(("'%s'",) * len(arg_name_list)),
            "],"))
        line = line_fmt % tuple(arg_name_list)
        line = self.text_wrapper.fill(line)
        all_line.append(line)

        line_fmt = "".join((indent, "arg_types=[",
            ", ".join(("%s",) * len(arg_type_list)),
            "],"))
        line = line_fmt % tuple(arg_type_list)
        line = self.text_wrapper.fill(line)
        all_line.append(line)

        if extra_line:
            line_end = ","
        else:
            line_end = ")"
        line = "".join((indent, "return_type=%s%s" % \
                (rval_type_str, line_end)))
        all_line.append(line)

        if enable_check_return:
            extra_line -= 1
            if extra_line:
                line_end = ","
            else:
                line_end = ")"
            line = "".join((indent, "check_return=True%s" % line_end))
            all_line.append(line)

        if enable_dereference_return:
            extra_line -= 1
            if extra_line:
                line_end = ","
            else:
                line_end = ")"
            line = "".join((indent, "dereference_return=True%s" % line_end))
            all_line.append(line)

        if enable_require_return:
            extra_line -= 1
            if extra_line:
                line_end = ","
            else:
                line_end = ")"
            line = "".join((indent, "require_return=True%s" % line_end))
            all_line.append(line)

        return "\n".join(all_line)

    """
    typedef const char * (*FtkXulTranslateText)(void * ctx, const char * text);
    ['const', 'char', '*'] FtkXulTranslateText [['void', '*', 'ctx'], ['const', 'char', '*', 'text']]
    FtkXulTranslateText = ctypes.CFUNCTYPE(ctypes.c_char_p, ctypes.c_void_p, ctypes.c_char_p)
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

    def _to_python_func_ptr_type_def(self, token, only_check_type=False):
        """
        print token.rval, token.name, token.args
        for a in token.args:
            print a.type, a.name
        """

        rval_type_str = self._type_str(token.rval)
        if rval_type_str is None:
            if not only_check_type:
                return self._exceptional_func_ptr_type_def_str(token)
            else:
                return None
        assert isinstance(rval_type_str, str)
        if only_check_type:
            self._update_global_info(rval_type_str)

        func_ptr_type_name = token.name
        assert isinstance(rval_type_str, str)

        line_content = [func_ptr_type_name, rval_type_str]
        for arg in token.args:
            arg_type_str = self._type_str(arg.type)
            if arg_type_str is None:
                if not only_check_type:
                    return self._exceptional_func_ptr_type_def_str(token)
                else:
                    return None
            assert isinstance(arg_type_str, str)
            if only_check_type:
                self._update_global_info(arg_type_str)
            line_content.append(arg_type_str)

        if only_check_type:
            return None

        line_fmt = "".join(("%s = ctypes.CFUNCTYPE(%s, ",
            ", ".join(("%s",) * len(token.args)), ")"))
        line = line_fmt % tuple(line_content)

        self.text_wrapper.initial_indent = ""
        self.text_wrapper.subsequent_indent = " " * 8
        return self.text_wrapper.fill(line)

    def _collect_private_type_info(self, content):
        self.priv_type_dict = {}
        self.dec_only_struct_type_dict = {}
        self.struct_type_alias_dict = {}
        self.all_struct_type_list = []

        for token, start, end in self.struct_alias.scanString(content):
            if not self._in_pub_type_dict(token.alias):
                self.priv_type_dict[token.alias] = token.alias
            self.dec_only_struct_type_dict[token.name] = token.alias
            self.all_struct_type_list.append(token.alias)

        for token, start, end in self.struct_type.scanString(content):
            if token.has_alias and not self._in_pub_type_dict(token.alias):
                self.priv_type_dict[token.alias] = token.alias

            if not token.has_alias:
                if token.name in self.dec_only_struct_type_dict:
                    self.struct_type_alias_dict[token.name] = \
                            self.dec_only_struct_type_dict[token.name]
                    del self.dec_only_struct_type_dict[token.name]
            else:
                self.all_struct_type_list.append(token.alias)

        for token, start, end in self.func_ptr_type.scanString(content):
            if not self._in_pub_type_dict(token.name):
                self.priv_type_dict[token.name] = token.name

    def _update_ptr_ref_info(self, type_str):
        result = self.pointer_re.search(type_str)
        if result is not None:
            type = result.group("type")
            if type not in self.basic_type_dict.values():
                ptr = result.group(0)
                if ptr not in self.ptr_type_ref_cnt_dict:
                    self.ptr_type_ref_cnt_dict[ptr] = 1
                else:
                    self.ptr_type_ref_cnt_dict[ptr] += 1

    def _add_imported_module(self, mname):
        if mname not in self.imported_module_list and mname != "ctypes":
            self.imported_module_list.append(mname)

    def _update_imported_module_info(self, type_str):
        if type_str.startswith("ctypes.POINTER"):
            result = self.pointer_re.search(type_str)
            if result is not None:
                type_str = result.group("type")
            else:
                sys.stderr.write("invalid symbol path %s\n", type_str)
                return

        parts = type_str.split(".")
        if len(parts) == 2:
            self._add_imported_module(parts[0])
        elif len(parts) != 1:
            sys.stderr.write("invalid symbol path %s\n", type_str)

    def _update_func_ptr_type_ref_info(self, type_str):
        if type_str in self.func_ptr_type_ref_dict:
            self.func_ptr_type_ref_dict[type_str] += 1

    def _update_global_info(self, type_str, in_func_dec=False):
        self._update_ptr_ref_info(type_str)
        self._update_imported_module_info(type_str)
        if not in_func_dec:
            self._update_func_ptr_type_ref_info(type_str)

    def _collect_global_info(self, content):
        import_ftk_dll = False

        for token, start, end in self.func_ptr_type.scanString(content):
            self._to_python_func_ptr_type_def(token, True)

        for token, start, end in self.struct_type.scanString(content):
            self._to_python_struct_type_def(token, True)

        for token, start, end in self.func_dec.scanString(content):
            import_ftk_dll = True
            self._to_python_func_dec(token, True)

        if import_ftk_dll:
            self._add_imported_module("ftk_dll")

    def _to_python_struct_type_dec(self, name):
        self._update_exported_symbols(name)

        dec_list = []

        struct_dec_line = "class %s(ctypes.Structure):\n    pass" % name
        dec_list.append(struct_dec_line)
        if self._need_create_ptr_type_alias(name):
            struct_ptr_line = "_%sPtr = ctypes.POINTER(%s)" % (name, name)
            dec_list.append(struct_ptr_line)

        return "\n\n".join(dec_list)

    """
    related definitions......
    class FtkXulCallbacks(ctypes.Structure):
        _fields_ = [
                ('id_a', type_a),
                ('id_b, type_b)
                ]

    class FtkImPreeditor(ctypes.Structure):
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

    def _to_python_struct_type_def(self, token, only_check_type=False):
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
            if token.name in self.struct_type_alias_dict:
                name = self.struct_type_alias_dict[token.name]
            else:
                sys.stderr.write("inconsistent struct definition style "
                    "for %s\n" % token.name)
                name = token.name.lstrip("_")

        if not only_check_type:
            self._update_exported_symbols(name)

        if self._need_create_ptr_type_alias(name):
            struct_ptr_line = "_%sPtr = ctypes.POINTER(%s)" % (name, name)

        func_ptr_list = []
        m_list = []
        for m in token.members:
            type_str = self._type_str(m.type)
            if type_str is None:
                if not only_check_type:
                    return self._exceptional_struct_type_def_str(token)
                else:
                    return None

            if only_check_type:
                self._update_global_info(type_str)
                continue

            if type_str in self.func_ptr_type_def_dict:
                func_ptr_list.append(type_str)

            if m.len:
                alen = m.len[0]
                try:
                    int(alen)
                except ValueError:
                    alen = "".join(("ftk_constants.", alen))
                    self._add_imported_module("ftk_constants")
                type_str = " * ".join((type_str, alen))
            m_str = "('%s', %s)" % (m.name, type_str)
            m_list.append(m_str)

        if only_check_type:
            return None

        def_list = []
        if token.has_alias:
            for func_ptr in func_ptr_list:
                def_list.append(self.func_ptr_type_def_dict[func_ptr])
            line_one = "class %s(ctypes.Structure):" % (name,)
            line_two = "    _fields_ = ["
            line_mems_fmt = ",\n".join((("            %s",) * len(m_list)))
            line_mems = line_mems_fmt % tuple(m_list)
            line_end = "            ]"
            struct_line = "\n".join((line_one, line_two, line_mems, line_end))
            def_list.append(struct_line)
            if self._need_create_ptr_type_alias(name):
                def_list.append(struct_ptr_line)
        else:
            struct_dec_line = "class %s(ctypes.Structure):\n    pass" % (name,)
            def_list.append(struct_dec_line)
            if self._need_create_ptr_type_alias(name):
                def_list.append(struct_ptr_line)
            for func_ptr in func_ptr_list:
                def_list.append(self.func_ptr_type_def_dict[func_ptr])
            first_line = "%s._fields_ = [" % (name,)
            middle_line_fmt = ",\n".join((("        %s",) * len(m_list)))
            middle_line = middle_line_fmt % tuple(m_list)
            last_line = "        ]"
            struct_line = "\n".join((first_line, middle_line, last_line))
            def_list.append(struct_line)
        return "\n\n".join(def_list)

    def _generate_func_ptr_type_ref_info(self, content):
        self.func_ptr_type_ref_dict = {}

        for token, start, end in self.func_ptr_type.scanString(content):
            self.func_ptr_type_ref_dict[token.name] = 0

    def _generate_func_ptr_type_def_info(self, content):
        self.func_ptr_type_def_dict = {}

        for token, start, end in self.func_ptr_type.scanString(content):
            self.func_ptr_type_def_dict[token.name] = \
                    self._to_python_func_ptr_type_def(token)

    def _convert_struct_type_def(self, content):
        struct_type_def = []

        for alias in self.dec_only_struct_type_dict.itervalues():
            struct_type_def.append(self._to_python_struct_type_dec(alias))

        for token, start, end in self.struct_type.scanString(content):
            struct_type_def.append(self._to_python_struct_type_def(token))

        return struct_type_def

    def _convert_func_dec(self, content, func=None):
        decs = []

        for token, start, end in self.func_dec.scanString(content):
            if func is not None and func != token.name:
                continue
            decs.append(self._to_python_func_dec(token))
            self._update_exported_symbols(token.name)

        if func is not None and len(decs) == 0:
            sys.stderr.write("declaration for function '%s' doesn't exist\n" % func)

        return decs

    def _generate_import_statements(self):
        import_lines = []

        mnames = ["ftk_dll", "ftk_constants", "ftk_typedef"]
        valid_mnames = [m for m in mnames if m in self.imported_module_list]
        for m in self.imported_module_list:
            if m not in mnames:
                valid_mnames.append(m)

        for m in valid_mnames:
            import_lines.append("import %s" % m)

        return "\n".join(import_lines)

    def _update_exported_symbols(self, name):
        if name not in self.exported_symbol_list:
            self.exported_symbol_list.append(name)

    def _generate_exported_symbols(self):
        symbols_fmt = ", ".join(("\"%s\"",) * len(self.exported_symbol_list))
        line_fmt = "__all__ = [%s]" % symbols_fmt
        line = line_fmt % tuple(self.exported_symbol_list)
        if len(line) > self.line_width:
            self.text_wrapper.initial_indent = ""
            self.text_wrapper.subsequent_indent = " " * 8
            line = self.text_wrapper.fill(line)
        return line

    def _generate_header(self):
        header = []
        if "%s." % self.fname[:-2] == self.mpath:
            header.append(self._generate_import_statements())
        header.append("# %s" % self.fname)
        if "%s." % self.fname[:-2] == self.mpath:
            header.append(self._generate_exported_symbols())

        return header

    def _derefer_type(self, ptr_type):
        result = self.pointer_re.search(ptr_type)
        if result is not None:
            return result.group("type")
        else:
            sys.stderr.write("invalid pointer type %s\n" % ptr_type)
            return ptr_type

    def _generate_ptr_type_aliases(self):
        indent = " " * 8
        lines = []
        for ptr_type, alias in self.ptr_type_alias_dict.iteritems():
            if self._derefer_type(ptr_type) not in self.all_struct_type_list:
                line = "%s = %s" % (alias, ptr_type)
                if len(line) > self.line_width:
                    line = "%s = \\\n%s%s" % (alias, indent, ptr_type)
                lines.append(line)
        return lines

    def run(self, finput, mpath, struct_enabled, func_enabled, func_name):
        self.fname = os.path.basename(os.path.abspath(finput))
        self.mpath = mpath
        self.ptr_type_alias_dict = {}
        self.priv_struct_ptr_type_list = []
        self.ptr_type_ref_cnt_dict = {}
        self.imported_module_list = []
        self.exported_symbol_list = []

        results = []
        with open(finput, "rb") as fd:
            content = fd.read()

            self._collect_private_type_info(content)

            self._generate_func_ptr_type_ref_info(content)

            self._enable_ptr_type_alias = False
            self._collect_global_info(content)
            self._enable_ptr_type_alias = True

            self._generate_func_ptr_type_def_info(content)

            if struct_enabled:
                defs = self._convert_struct_type_def(content)
            else:
                defs = []
            if func_enabled:
                decs = self._convert_func_dec(content, func_name)
            else:
                decs = []

        if struct_enabled and func_enabled:
            header = self._generate_header()
            results.extend(header)

            ptr_type_aliases = self._generate_ptr_type_aliases()
            results.extend(ptr_type_aliases)

        results.extend(defs)
        results.extend(decs)

        return "\n\n".join(results)

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
    opt_parser.add_option("-o", "--only", dest="func_name",
            help="only execute code generation for this function",
            metavar="FUNC_NAME")
    (options, args) = opt_parser.parse_args()

    if options.file is None or not os.path.isfile(options.file) or \
            not fnmatch.fnmatch(options.file, "*.h") or \
            (options.m_name is not None and \
            not isinstance(options.m_name, str)) or \
            (options.func_name is not None and \
            not isinstance(options.func_name, str)):
        opt_parser.print_help()
        sys.exit(1)

    cfg_file = os.path.join(os.path.dirname(sys.argv[0]), "typedef")
    converter = C2PythonConverter(cfg_file)

    if options.m_name is None:
        fname = os.path.basename(options.file)
        module_name = fname[:-2]
    else:
        module_name = options.m_name

    if options.func_name is not None:
        options.disable_struct = True
        options.disable_func = False

    module_path = "".join((module_name, "."))
    content = converter.run(options.file, module_path,
            not options.disable_struct, not options.disable_func,
            options.func_name)

    if content:
        print content

    sys.exit(0)
