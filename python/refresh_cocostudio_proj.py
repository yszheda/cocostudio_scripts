#!/usr/bin/env python
# coding:utf-8
# Refresh the following files of the given cocostudio project:
# *.ccs
# *.csi: cocostudio SpriteFrameSheet


import os
import sys
import refresh_csi
import refresh_csd
import refresh_ccs


PROGRAM_DIST = {
    "csi": refresh_csi.main,
    "csd": refresh_csd.main,
    "ccs": refresh_ccs.main,
}


def get_file_ext(file_name):
    return file_name.split('.')[-1]


def refresh_ui_proj(ui_proj_path):
    for root, dirs, files in os.walk(ui_proj_path):
        for file_name in files:
            file_full_name = os.path.abspath(os.path.join(root, file_name))
            program = PROGRAM_DIST.get(get_file_ext(file_name))
            if program:
                print "Refresh %s" % file_full_name
                args = [file_full_name]
                program(args)


def main(argv):
    ui_proj_path = argv[0]
    if ui_proj_path is None:
        ui_proj_path = '.'
    if os.path.exists(ui_proj_path):
        refresh_ui_proj(ui_proj_path)
    else:
        err_msg = "%s is not existed!" % ui_proj_path
        sys.stderr.write(err_msg)
        sys.exit(1)


if __name__ == "__main__":
    main(sys.argv[1:])
