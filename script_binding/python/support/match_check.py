#!/usr/bin/env python
# -*- coding: utf8 -*

import sys
import os
import re
import fnmatch

extra_fpath_map = {
        "ftk_allocator.py" : ["ftk_allocator_default.h"],
        "ftk_source.py" : ["ftk_source_idle.h",
            "ftk_source_primary.h",
            "ftk_source_timer.h"],
        "ftk_image_decoder.py" : ["ftk_image_bmp_decoder.h",
            "ftk_image_jpeg_decoder.h",
            "ftk_image_png_decoder.h"],
        "ftk_interpolator.py" : ["ftk_interpolator_acc_decelerate.h",
            "ftk_interpolator_accelerate.h",
            "ftk_interpolator_bounce.h",
            "ftk_interpolator_decelerate.h",
            "ftk_interpolator_linear.h"],
        "ftk_animation.py" : ["ftk_animation_alpha.h",
            "ftk_animation_expand.h",
            "ftk_animation_scale.h",
            "ftk_animation_translate.h"],
        "ftk_list_model.py" : ["ftk_list_model_default.h"],
        "ftk_list_render.py" : ["ftk_list_render_default.h"],
        "ftk_wnd_manager.py" : ["ftk_wnd_manager_default.h"],
        "ftk_animation_trigger.py" : ["ftk_animation_trigger_default.h",
        "ftk_animation_trigger_silence.h"],
        "ftk_input_method_preeditor.py" : ["ftk_input_method_preeditor_default.h"],
        }

def create_path_map(py_bdir, header_bdir):
    fpath_map = {}
    exclude_py_entries = ["__init__.py", "ftk_util.py", "template.py",
            "ftk_dll.py", "ftk_error.py", "ftk_macros.py", "ftk_constants.py"]

    for py_entry in os.listdir(py_bdir):
        py_path = os.path.join(py_bdir, py_entry)
        if os.path.isfile(py_path) and fnmatch.fnmatch(py_entry, "*.py") and \
                py_entry not in exclude_py_entries:
            fpath_map[py_path] = []
            py_module_name = py_entry[:-3]

            header_entry = ".".join((py_module_name, "h"))
            header_path = os.path.join(header_bdir, header_entry)
            if os.path.isfile(header_path):
                fpath_map[py_path].append(header_path)

            if py_entry in extra_fpath_map:
                fpath_map[py_path].extend(
                        map(lambda e: os.path.join(header_bdir, e),
                            extra_fpath_map[py_entry]))

    return fpath_map

def check_match_condition(name, fpath_dict, key_ptn, val_ptn):
    for key_path in fpath_dict.iterkeys():
        with open(key_path, "rb") as fd:
            key_matched_cnt = len(key_ptn.findall(fd.read()))
        all_val_path = fpath_dict[key_path]
        val_matched_cnt = 0
        for val_path in all_val_path:
            with open(val_path, "rb") as fd:
                val_matched_cnt += len(val_ptn.findall(fd.read()))

        if key_matched_cnt != val_matched_cnt:
            sys.stdout.write("*************************************\n")
            sys.stdout.write("unmatch pattern count %d/%d for %s\n" %
                    (key_matched_cnt, val_matched_cnt, name))
            sys.stdout.write("left input is %s\n" % key_path)
            sys.stdout.write("right input is %s\n" % all_val_path)

if __name__ == "__main__":
    script_bdir = os.path.dirname(os.path.abspath(sys.argv[0]))
    py_bdir = os.path.abspath(os.path.join(script_bdir, "../ftk"))
    header_bdir = os.path.abspath(os.path.join(script_bdir, "../../../src"))
    py_to_header_dict = create_path_map(py_bdir, header_bdir)

    """
    name = "size_t"
    py_ptn = re.compile(r"ctypes\.c_size_t")
    header_ptn = re.compile(r"size_t")
    check_match_condition(name, py_to_header_dict, py_ptn, header_ptn)
    """
    
    """
    name = "Ret"
    py_ptn = re.compile(r"check_return=True")
    header_ptn = re.compile(r"^Ret", re.MULTILINE)
    check_match_condition(name, py_to_header_dict, py_ptn, header_ptn)
    """

    sys.exit(0)
