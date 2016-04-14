#!/usr/bin/env python
# coding:utf-8
# Refresh cocostudio csd


import os
import sys
from lxml import etree
import re


PATH_KEY = 'Path'
PLIST_KEY = 'Plist'


res_path = None


def read_xml(xml_file):
    parser = etree.XMLParser(remove_blank_text=True)
    return etree.parse(xml_file, parser)


def write_xml(xml_tree, xml_file):
    xml_tree.write(xml_file, encoding="utf-8", pretty_print=True)


def find_real_dir(file_name, old_dir_name):
    global res_path
    new_dir_name = None
    for root, dirs, files in os.walk(res_path):
        if file_name in files:
            full_path = os.path.abspath(os.path.join(root, file_name))
            full_dir = os.path.split(full_path)[0]
            # Find last occurrence of cocosstudio in the full dir
            match = re.match('.*cocosstudio', full_dir)
            if match:
                prefix_dir = match.group()
                # NOTE: the first char is '/' or '\', remove it
                new_dir_name = re.sub(prefix_dir, '', full_dir)[1:]
                # Replace Windows '\' to UNIX '/' as frame namespace
                new_dir_name.replace('\\', '/')
                if new_dir_name == old_dir_name:
                    return
    if new_dir_name:
        return new_dir_name


def update_path(xml_node):
    if xml_node.attrib['Type'] != 'MarkedSubImage':
        return
    old_frame_name = xml_node.attrib[PATH_KEY].split('/')
    dir_name = "".join(old_frame_name[:-1])
    file_name = old_frame_name[-1]
    new_dir_name = find_real_dir(file_name, dir_name)
    if new_dir_name:
        print(new_dir_name)
        new_frame_name = "%s/%s" % (new_dir_name, file_name)
        xml_node.set(PATH_KEY, new_frame_name)

        plist_node = xml_node.attrib[PLIST_KEY]
        if plist_node is None:
            print("WARNING: %s is not in csi!" % xml_node.attrib[PATH_KEY])
        new_plist_name = "windows/%s.plist" % new_dir_name
        xml_node.set(PLIST_KEY, new_plist_name)


def handle_button(xml_node):
    nodes = (xml_node.find('NormalFileData'),
             xml_node.find('PressedFileData'),
             xml_node.find('DisabledFileData'))
    for node in nodes:
        update_path(node)


def handle_image(xml_node):
    file_node = xml_node.find('FileData')
    if file_node is not None:
        update_path(file_node)


def refresh_csd(csd_file):
    xml_tree = read_xml(csd_file)

    for node in xml_tree.iterfind('.//NodeObjectData'):
        node_type = node.attrib['ctype']
        if node_type == 'ButtonObjectData':
            handle_button(node)
        elif node_type == 'ImageViewObjectData':
            handle_image(node)

    write_xml(xml_tree, csd_file)


def main(argv):
    csd_file = argv[0]
    if os.path.exists(csd_file):
        global res_path
        res_path = os.path.dirname(os.path.abspath(csd_file))
        refresh_csd(csd_file)
    else:
        err_msg = "%s is not existed!" % csd_file
        sys.stderr.write(err_msg)
        sys.exit(1)


if __name__ == "__main__":
    main(sys.argv[1:])
