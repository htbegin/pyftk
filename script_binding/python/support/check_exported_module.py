#!/usr/bin/env python
# -*- coding: utf8 -*-

import sys
import os
import fnmatch
import re

def get_defined_modules(dname):
    excluded_modules = ["__init__", "template", "dll", "error", "macros",
            "priv_util"]
    modules = []
    for entry in os.listdir(dname):
        if fnmatch.fnmatch(entry, "*.py"):
            m = entry[:-len(".py")]
            if m not in excluded_modules:
                modules.append(m)
    return modules

def get_exported_modules(dname):
    modules = []
    ptn = re.compile(r"from\s+ftk\.([A-Z0-9a-z_]+)\s+import\s+\*")
    with open(os.path.join(dname, "__init__.py"), "rb") as fd:
        content = fd.read()
        modules = ptn.findall(content)
        modules.sort()
        for i in range(1, len(modules)):
            if modules[i] == modules[i - 1]:
                sys.stdout.write("%s export module %s duplicatively\n" %
                        (dname, modules[i]))
    return modules

if __name__ == "__main__":
    if len(sys.argv) != 2 or not os.path.isdir(sys.argv[1]) \
            or not os.path.isfile(os.path.join(sys.argv[1], "__init__.py")):
        sys.stdout.write("Usage: %s py_package_dir\n" % sys.argv[0])
        sys.exit(1)

    defined_modules = get_defined_modules(sys.argv[1])
    exported_modules = get_exported_modules(sys.argv[1])

    for m in defined_modules:
        if m not in exported_modules:
            sys.stdout.write("%s doesn't export module %s\n" %
                    (sys.argv[1], m))

    sys.exit(0)
