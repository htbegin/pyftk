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
_enum_def_pattern = re.compile(r'^\s*(%s)\s*(=\s*([^\s]+)\s*)?(,)?' % _var_pattern)
_enum_end_pattern = re.compile(r'^\s*}\s*(%s)?\s*;' % _var_pattern)
(ENUM_START_FIRST, ENUM_START_SEC, ENUM_DEF, ENUM_END) = range(4)

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

def get_file_enums(include_file):
    '''
    iterate each line
    if find the start of enum, advance the status
    if the start of enum has been found, then find the enum
        save the found enum (label, string value, integer value)
    if find the end of enum, generate the enum in python-style
        if the integer values are sequential, then using the range,
        else assignment theme individually.
    '''
    return []
    defines = []
    enum_info = {}
    enum_info["file"] = include_file
    status = ENUM_START_FIRST
    for idx, line in enumerate(open(include_file).readlines()):
        if status == ENUM_START_FIRST:
            status = handle_enum_start_first_status(idx, line, enum_info)
        elif status == ENUM_START_SEC:
            status = handle_enum_start_sec_status(idx, line, enum_info)

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
