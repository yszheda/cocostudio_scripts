#!/usr/bin/env python
# coding:utf-8
# Copy text-related png to the cocosstudio dir of the given cocosstudio project.

import os
import sys
import re
import shutil
import create_csi
import refresh_csi


LANG = 'zh_TW'


# http://pythoncentral.io/how-to-recursively-copy-a-directory-folder-in-python/
def copy_dir(src, dest):
    try:
        shutil.copytree(src, dest)
        # Directories are the same
    except shutil.Error as e:
        print('Directory not copied. Error: %s' % e)
        # Any error saying that the directory doesn't exist
    except OSError as e:
        print('Directory not copied. Error: %s' % e)


def sync_dir(src, dist):
    lib_path = os.path.abspath('rsync.py')
    sys.path.append(lib_path)
    import rsync
    args = [
        '-ru',
        '--delete_excluded',
        src,
        dist,
    ]
    rsync.main(args)


def trim_last_num(string):
    return re.sub(r'\d+$', '', string)


def get_tp_res_path(atlas_name):
    pwd = os.path.realpath(__file__)
    tp_proj_root = os.path.abspath(os.path.join(pwd, '..', 'tp_projects', LANG))
    res_path = os.path.join(tp_proj_root, atlas_name, atlas_name)
    if os.path.exists(res_path):
        return res_path


def get_csi_path(res_path, atlas_name):
    return os.path.abspath(os.path.join(res_path, 'windows', atlas_name))


def copy_text_pngs(ui_proj_path):
    for root, dirs, files in os.walk(ui_proj_path):
        match = re.match('.*cocosstudio$', root)
        if match:
            res_path = os.path.abspath(root)

            atlas_names = set()
            for dir_name in dirs:
                atlas_names.add(dir_name)
                atlas_names.add(trim_last_num(dir_name))

            for atlas_name in atlas_names:
                text_atlas_name = "%s_text" % atlas_name
                text_res_path = get_tp_res_path(text_atlas_name)
                if text_res_path:
                    print "Copy %s to %s" % (text_res_path, res_path)
                    copy_dir(text_res_path, res_path)

                    text_csi_name = "%s.csi" % text_atlas_name
                    text_csi_file = get_csi_path(res_path, text_csi_name)
                    args = [text_csi_file]
                    create_csi.main(args)
                    refresh_csi.main(args)


def main(argv):
    ui_proj_path = argv[0]
    if ui_proj_path is None:
        ui_proj_path = '.'
    if os.path.exists(ui_proj_path):
        copy_text_pngs(ui_proj_path)
    else:
        err_msg = "%s is not existed!" % ui_proj_path
        sys.stderr.write(err_msg)
        sys.exit(1)


if __name__ == "__main__":
    main(sys.argv[1:])
