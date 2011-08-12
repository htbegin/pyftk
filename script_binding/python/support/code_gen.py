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
        self.basic_type_dict = {
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

    def _ptr_type_alias_str(self, type_str):
        result = self.pointer_re.search(type_str)
        if result is not None:
            type = result.group('type')
            if type not in self.basic_type_dict.values():
                parts = type.split(".")
                alias = "_%sPtr" % parts[-1]
                self.ptr_type_alias_dict[result.group(0)] = alias
                return self.pointer_re.sub(alias, type_str)
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

        last_idx = len(tinfo) - 1
        while tinfo[last_idx] == "*":
            deref_type_str = " ".join(tinfo[0:last_idx])
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
    ftk_window_set_animation_hint = ftk_dll.function(
            'ftk_window_set_animation_hint',
            '',
            args=['thiz', 'hint'],
            arg_types=[ftk_widget.FtkWidgetPtr, ctypes.c_char_p],
            return_type=ctypes.c_int)
    """
    def _to_python_func_dec(self, token, only_check_type=False):
        enable_check_return = False
        enable_dereference_return = False
        enable_require_return = False

        rval_type = token.rval
        rval_type_str = self._type_str(rval_type)
        if rval_type_str is None:
            if not only_check_type:
                return self._exceptional_func_dec_str(func)
            else:
                return None
        assert isinstance(rval_type_str, str)
        if only_check_type:
            self._update_global_info(rval_type_str)

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
                        return self._exceptional_func_dec_str(func)
                    else:
                        return None
                assert isinstance(arg_type_str, str)
                if only_check_type:
                    self._update_global_info(arg_type_str)
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
            if func_name_str.endswith("_create"):
                enable_require_return = True
                extra_line += 1

        indent = " " * 8
        all_line = []

        line = "%s = ftk_dll.function('%s'," % (func_name_str, func_name_str)
        all_line.append(line)

        line = "".join((indent, "'',"))
        all_line.append(line)

        line_fmt = "".join((indent, "args=[",
            ", ".join(("'%s'",) * len(arg_name_list)),
            "],"))
        line = line_fmt % tuple(arg_name_list)
        all_line.append(line)

        line_fmt = "".join((indent, "arg_types=[",
            ", ".join(("%s",) * len(arg_type_list)),
            "],"))
        line = line_fmt % tuple(arg_type_list)
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
                redefine_dict["".join(("ctypes.POINTER(", k, ")"))] = alias

        if len(redefine_dict) == 0:
            return results

        new_results = []
        for alias, line in self.priv_struct_ptr_type_list.iteritems():
            if alias not in redefine_dict.values():
                alias_def = self.priv_struct_ptr_type_list[alias]
                sub_str = "".join(("\n\n", alias_def))
                for line in results:
                    new_line = line.replace(sub_str, "")
                    new_results.append(new_line)
                results = new_results

        redefine_results = []
        for type, alias in redefine_dict.iteritems():
            if alias in self.priv_struct_ptr_type_list:
                continue
            line = "%s = %s" % (alias, type)
            redefine_results.append(line)

        for lines in results:
            for type, alias in redefine_dict.iteritems():
                if alias in self.priv_struct_ptr_type_list:
                    alias_def = self.priv_struct_ptr_type_list[alias]
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
        return line

    def _collect_private_type_info(self, content):
        self.priv_type_dict = {}
        self.dec_only_struct_type_dict = {}

        for token, start, end in self.struct_alias.scanString(content):
            if not self._in_pub_type_dict(token.alias):
                self.priv_type_dict[token.alias] = token.alias
            self.dec_only_struct_type_dict[token.name] = token.alias

        for token, start, end in self.struct_type.scanString(content):
            if token.has_alias and not self._in_pub_type_dict(token.alias):
                self.priv_type_dict[token.alias] = token.alias
            if not token.has_alias:
                if token.name in self.dec_only_struct_type_dict:
                    del self.dec_only_struct_type_dict[token.name]

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

    def _update_global_info(self, type_str):
        self._update_ptr_ref_info(type_str)
        self._update_imported_module_info(type_str)

    def _collect_global_info(self, content):
        import_ftk_dll = False

        for token, start, end in self.func_ptr_type.scanString(content):
            self._to_python_func_ptr_type_def(token, True)
        print self.ptr_type_ref_cnt_dict
        print self.imported_module_list

        for token, start, end in self.struct_type.scanString(content):
            self._to_python_struct_type_def(token, True)
        print self.ptr_type_ref_cnt_dict
        print self.imported_module_list

        for token, start, end in self.func_dec.scanString(content):
            import_ftk_dll = True
            self._to_python_func_dec(token, True)
        print self.ptr_type_ref_cnt_dict
        print self.imported_module_list

        if import_ftk_dll:
            self._add_imported_module("ftk_dll")

        print self.imported_module_list

    def _to_python_struct_type_dec(self, name):
        dec_list = []
        ptr = "ctypes.POINTER(%s)" % name
        ptr_alias = "_%sPtr" % name
        struct_ptr_line = "%s = %s" % (ptr_alias, ptr)
        self.priv_struct_ptr_type_list.append(ptr)

        struct_dec_line = "class %s(ctypes.Structure):\n    pass" % (name,)
        dec_list.append(struct_dec_line)
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
            # FIXME
            name = token.name.lstrip("_")
        ptr = "ctypes.POINTER(%s)" % name
        ptr_alias = "_%sPtr" % (name,)
        struct_ptr_line = "%s = %s" % (ptr_alias, ptr)
        self.priv_struct_ptr_type_list.append(ptr)

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

            if type_str in self.func_ptr_type_dict:
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
                def_list.append(self.func_ptr_type_dict[func_ptr])
            line_one = "class %s(ctypes.Structure):" % (name,)
            line_two = "    _fields_ = ["
            line_mems_fmt = ",\n".join((("            %s",) * len(m_list)))
            line_mems = line_mems_fmt % tuple(m_list)
            line_end = "            ]"
            struct_line = "\n".join((line_one, line_two, line_mems, line_end))
            def_list.append(struct_line)
            def_list.append(struct_ptr_line)
        else:
            struct_dec_line = "class %s(ctypes.Structure):\n    pass" % (name,)
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

        for alias in self.dec_only_struct_type_dict.itervalues():
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
        self.ptr_type_alias_dict = {}
        self.priv_struct_ptr_type_list = []
        self.ptr_type_ref_cnt_dict = {}
        self.imported_module_list = []

        results = []
        with open(finput, "rb") as fd:
            content = fd.read()

            self._collect_private_type_info(content)

            self._enable_ptr_type_alias = False
            self._collect_global_info(content)
            self._enable_ptr_type_alias = True

            """
            if struct_enabled:
                defs = self._convert_struct_type_def(content)
            else:
                defs = []
            if func_enabled:
                decs = self._convert_func_dec(content)
            else:
                decs = []
            """
        """
        results.extend(defs)
        results.extend(decs)
        """

        #results = self._redefine_pointer(results)

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

    module_path = "".join((module_name, "."))
    content = converter.run(options.file, module_path,
            not options.disable_struct, not options.disable_func)

    if content:
        print content

    sys.exit(0)
