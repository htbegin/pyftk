#!/usr/bin/env python
# -*- coding: utf8 -*-

import sys
import os
import fnmatch
import stat

_unittest_template = """\
#!/usr/bin/env python

import unittest

from ftk.%s import *

class Test%s(unittest.TestCase):
    def _test(self):
        pass

if __name__ == "__main__":
    unittest.main()"""

def create_empty_unittest_file(test_bdir, fname):
    module_name = fname[:-3]
    ut_fname = "test_%s.py" % module_name
    ut_fpath = os.path.join(test_bdir, ut_fname)
    if os.path.exists(ut_fpath):
        sys.stdout.write("%s exists\n" % ut_fname)
        return

    parts = module_name.split("_")
    cls_name = "".join([p.capitalize() for p in parts])
    with open(ut_fpath, "wb") as fd:
        fd.write(_unittest_template % (module_name, cls_name))

    os.chmod(ut_fpath, stat.S_IRUSR | stat.S_IWUSR | stat.S_IXUSR | \
            stat.S_IRGRP | stat.S_IXGRP | \
            stat.S_IROTH | stat.S_IXOTH)

def create_empty_unittest_file_bundle(test_bdir, dname):
    for entry in os.listdir(dname):
        if fnmatch.fnmatch(entry, "ftk_*.py"):
            create_empty_unittest_file(test_bdir, entry)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.stdout.write("Usage: %s py_dir|py_file\n" % sys.argv[0])
        sys.exit(1)

    self_bdir = os.path.dirname(os.path.abspath(sys.argv[0]))
    test_bdir = os.path.abspath(os.path.join(self_bdir, "../test"))
    if os.path.isfile(sys.argv[1]):
        fname = os.path.basename(os.path.abspath(sys.argv[1]))
        if fnmatch.fnmatch(fname, "ftk_*.py"):
            create_empty_unittest_file(test_bdir, fname)
    elif os.path.isdir(sys.argv[1]):
        create_empty_unittest_file_bundle(test_bdir, sys.argv[1])

    sys.exit(0)
