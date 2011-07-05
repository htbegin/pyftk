#!/usr/bin/env python

'''
Usage: make_constants.py source_file include_dir

for example:
    python support/make_constants.py SDL/constants.py /usr/include/SDL
'''

__docformat__ = 'restructuredtext'
__version__ = '$Id: $'

import os
import os.path
import re
import sys

BEGIN_TAG = '#BEGIN GENERATED CONSTANTS'
END_TAG = '#END GENERATED CONSTANTS'

define_pattern = re.compile('#define[ \t]+([^ \t]+)[ \t]+((0x)?[0-9a-fA-F]+)')
def get_file_defines(include_file):
    defines = []
    for match in define_pattern.finditer(open(include_file).read(), re.M):
        num = match.groups()[1]
        try:
            if num[:2] == '0x':
                num = int(num, 16)
            else:
                num = int(num)
            name = match.groups()[0]
            defines.append('%s = 0x%08x\n' % (name, num))
        except ValueError:
            pass
    return defines

_var_pattern = r'[_a-zA-Z][_a-zA-Z0-9]*'
_enum_start_first_pattern = re.compile(r'enum\s+(%s)\s*({)?\s*$' % _var_pattern)
_enum_start_sec_pattern = re.compile(r'^\s*{\s*$')
# endded without comma, but with comment
_enum_def_first_pattern = re.compile(r'^\s*(%s)\s*(=\s*([^,]+?))?/[*/]' % _var_pattern)
# ended with comma and comment
_enum_def_sec_pattern = re.compile(r'^\s*(%s)\s*(=\s*([^,]+?))?,\s*/[*/]' % _var_pattern)
# ended with comma, but without comment
_enum_def_third_pattern = re.compile(r'^\s*(%s)\s*(=\s*([^,]+))?,\s*$' % _var_pattern)
# ended without comma and comment
_enum_def_fourth_pattern = re.compile(r'^\s*(%s)\s*(=\s*([^,]+))?$' % _var_pattern)

_enum_end_pattern = re.compile(r'^\s*}\s*(%s)?\s*;' % _var_pattern)
(ENUM_START_FIRST, ENUM_START_SEC, ENUM_DEF, ENUM_END) = range(4)
(LABEL_VAL_AUTO, LABEL_VAL_MANUAL) = range(2)
(LABEL_KEY_IDX, LABEL_VAL_TYPE_IDX, LABEL_VAL_STR_IDX, LABEL_VAL_IDX) = range(4)

def handle_enum_start_first_status(idx, line, enum_info):
    match = _enum_start_first_pattern.search(line)
    if match is not None:
        enum_info["name"] = match.groups()[0]
        enum_info["line"] = idx + 1
        if match.groups()[1] is None:
            status = ENUM_START_SEC
        else:
            status = ENUM_DEF
    else:
        status = ENUM_START_FIRST

    return status

def handle_enum_start_sec_status(idx, line, enum_info):
    match = _enum_start_sec_pattern.search(line)
    if match is not None:
        status = ENUM_DEF
    else:
        sys.stderr.write("invalid enum %s at %s:%d\n" %
                (enum_info["name"], enum_info["file"], enum_info["line"]))
        status = handle_enum_start_first_status(idx, line, enum_info)

    return status

def handle_enum_def_status(idx, line, enum_info):
    status = None
    ptn_list = (_enum_def_first_pattern, _enum_def_sec_pattern,
            _enum_def_third_pattern, _enum_def_fourth_pattern)
    for ptn in ptn_list:
        match = ptn.search(line)
        if match is not None:
            key = match.groups()[0]
            if match.groups()[1] is not None:
                val_type = LABEL_VAL_MANUAL
                val_str = match.groups()[2].strip()
                val = eval(val_str)
            else:
                val_type = LABEL_VAL_AUTO
                val_str = None
                val = None
            if "labels" not in enum_info:
                enum_info["labels"] = []
            enum_info["labels"].append([key, val_type, val_str, val])
            status = ENUM_DEF
            break

    if status is None:
        match = _enum_end_pattern.search(line)
        if match is not None:
            status = ENUM_END
        else:
            sys.stderr.write("invalid label line %d for enum %s at %s:%d\n" %
                    (idx + 1, enum_info["name"], enum_info["file"], enum_info["line"]))
            if "labels" in enum_info:
                del enum_info["labels"]
            status = handle_enum_start_first_status(idx, line, enum_info)

    return status

def update_defines(defines, enum_info):
    is_sequential = True
    all_label = enum_info["labels"]
    for idx, label in enumerate(all_label):
        key, val_type, val_str, val = label
        if idx == 0:
            if val_type == LABEL_VAL_AUTO:
                expect_val = 0
            else:
                expect_val = val

        if val_type == LABEL_VAL_AUTO:
            label[LABEL_VAL_IDX] = expect_val
            expect_val += 1
        else:
            if val != expect_val:
                is_sequential = False
            expect_val = val + 1

    line = "# enum %s\n" % enum_info["name"]
    defines.append(line)

    if is_sequential:
        part = "%s,\n\t" * (len(all_label) - 1)
        fmt_str = "".join(("(", part, "%s)", " = range(%d, %d)\n\n"))
        args = [label[LABEL_KEY_IDX] for label in all_label]
        args.append(all_label[0][LABEL_VAL_IDX])
        args.append(all_label[0][LABEL_VAL_IDX] + len(all_label))
        line = fmt_str % tuple(args)
    else:
        fmt_str = "%s = %d\n" * len(all_label)
        fmt_str = "".join((fmt_str, "\n"))
        args = []
        for label in all_label:
            args.append(label[LABEL_KEY_IDX])
            args.append(label[LABEL_VAL_IDX])
        line = fmt_str % tuple(args)

    defines.append(line)

def get_file_enums(include_file):
    defines = []
    enum_info = {}
    enum_info["file"] = os.path.basename(include_file)
    status = ENUM_START_FIRST
    for idx, line in enumerate(open(include_file).readlines()):
        if not line.strip():
            continue
        if status == ENUM_START_FIRST:
            status = handle_enum_start_first_status(idx, line, enum_info)
        elif status == ENUM_START_SEC:
            status = handle_enum_start_sec_status(idx, line, enum_info)
        elif status == ENUM_DEF:
            status = handle_enum_def_status(idx, line, enum_info)
        else:
            update_defines(defines, enum_info)
            status = handle_enum_start_first_status(idx, line, enum_info)

    return defines

def make_constants(source_file, include_dir):
    lines = pre_lines = []
    post_lines = []
    for line in open(source_file).readlines():
        if line[:len(END_TAG)] == END_TAG:
            lines = post_lines
        if lines != None:
            lines.append(line)
        if line[:len(BEGIN_TAG)] == BEGIN_TAG:
            lines = None

    if lines == pre_lines:
        raise Exception, '%s does not have begin tag' % source_file
    elif lines == None:
        raise Exception, '%s does not have end tag' % source_file

    for file in os.listdir(include_dir):
        if file[-2:] == '.h':
            if file[:10] == 'SDL_config' or \
               file in ('SDL_platform.h','SDL_opengl.h'):
                continue
            defines = get_file_defines(os.path.join(include_dir, file))
            if defines:
                pre_lines.append('\n#Constants from %s:\n' % file)
                pre_lines += defines
            defines = get_file_enums(os.path.join(include_dir, file))
            if defines:
                pre_lines.append('\n#Enum from %s:\n' % file)
                pre_lines += defines

    file = open(source_file, 'w')
    for line in pre_lines + post_lines:
        file.write(line)

if __name__ == '__main__':
    if len(sys.argv) != 3:
        print __doc__
    else:
        make_constants(*sys.argv[1:])
