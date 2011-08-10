#!/usr/bin/env python
# -*- coding: utf8 -*-

import sys
import os
import stat
import fnmatch
import subprocess

def setup_run_env():
    key = "PYTHONPATH"
    ftk_path = os.path.dirname(os.path.abspath(sys.argv[0]))
    if key in os.environ:
        os.environ[key] = ":".join((ftk_path, os.environ[key]))
    else:
        os.environ[key] = ftk_path

def file_executable(arg):
    info = os.stat(arg)
    if stat.S_IMODE(info.st_mode) & stat.S_IXUSR:
        return True
    else:
        return False

def exec_and_wait(fpath, args):
    cmd = [fpath]
    cmd.extend(args)
    subprocess.call(cmd)

def run_script(fpath, args):
    fname = os.path.basename(fpath)
    sys.stdout.write("****************************************\n")
    sys.stdout.write("run %s\n" % fname)
    sys.stdout.write("****************************************\n")

    if fname.startswith("test_"):
        old_cwd = os.getcwd()
        dname = os.path.dirname(fpath)
        os.chdir(dname)
        try:
            exec_and_wait("/".join((".", fname)), args)
        except Exception:
            pass
        finally:
            os.chdir(old_cwd)
    else:
        exec_and_wait(fpath, args)

def run_scripts_in_dir(dpath, args):
    for entry in os.listdir(dpath):
        fpath = os.path.join(dpath, entry)
        if os.path.isfile(fpath) and fnmatch.fnmatch(entry, "*.py") and \
                file_executable(fpath):
            run_script(fpath, args)

if __name__ == "__main__":
    if len(sys.argv) == 1:
        sys.stdout.write("Usage: %s py_script|py_scrpit_dir [arg...]\n" %
                sys.argv[0])
        sys.exit(1)

    setup_run_env()

    exe = sys.argv[1]
    args = sys.argv[2:]
    if os.path.isfile(exe) and file_executable(exe):
        run_script(os.path.abspath(exe), args)
    elif os.path.isdir(exe):
        run_scripts_in_dir(os.path.abspath(exe), args)

    sys.exit(0)
