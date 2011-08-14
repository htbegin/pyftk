#!/usr/bin/env python
# -*- coding: utf8 -*-

import sys
import os
import fnmatch
import re

def check_missed_import(fname):
    with open(fname, "rb") as fd:
        content = fd.read()
        import_modules = import_module_ptn.findall(content)
        used_modules = list(set(used_module_ptn.findall(content)))
        for m in used_modules:
            if m not in import_modules:
                sys.stdout.write("missed import module %s in %s\n" % (m, fname))

if __name__ == "__main__":
    if len(sys.argv) == 1:
        sys.stdout.write("Usage: %s py_script...\n" % sys.argv[0])
        sys.exit(1)

    module_ptn = r"ftk_[a-zA-Z][a-zA-Z0-9_]+"
    import_module_ptn = re.compile(r"^\s*import\s+(%s)\s*$" % module_ptn,
            re.MULTILINE)
    used_module_ptn = re.compile(r"(%s)\.[a-zA-Z][a-zA-Z0-9_]+" % module_ptn)

    for fname in sys.argv[1:]:
        if os.path.isfile(fname) and fnmatch.fnmatch(fname, "*.py"):
            check_missed_import(fname)

    sys.exit(0)
