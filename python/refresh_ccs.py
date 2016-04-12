#!/usr/bin/env python
# coding:utf-8
# Refresh cocostudio ccs


import os
import sys
from lxml import etree


res_path = None

FILE_TAG_DICT = {
    "csd": "Project",
    "csi": "PlistInfo",
    "png": "Image",
}
DEFAULT_FILE_TAG = "File"

FOLDER_TAG = "Folder"


def read_xml(xml_file):
    parser = etree.XMLParser(remove_blank_text=True)
    return etree.parse(xml_file, parser)


def write_xml(xml_tree, xml_file):
    xml_tree.write(xml_file, encoding="utf-8", pretty_print=True)


def is_hidden_file(file_name):
    return file_name[0] == '.'


def create_file_node(xml_node, file_name):
    if is_hidden_file(file_name):
        return

    file_ext = file_name.split('.')[-1]
    tag = FILE_TAG_DICT.get(file_ext, DEFAULT_FILE_TAG)
    attrib = {"Name": file_name}
    child_node = etree.Element(tag, attrib)
    xml_node.append(child_node)
    return child_node


def create_dir_node(xml_node, dir_name):
    tag = FOLDER_TAG
    attrib = {"Name": dir_name}
    child_node = etree.Element(tag, attrib)
    xml_node.append(child_node)
    return child_node


def gen_nodes_for_path(xml_node, root_path):
    for item in os.listdir(root_path):
        item_path = os.path.abspath(os.path.join(root_path, item))
        if os.path.isfile(item_path):
            create_file_node(xml_node, item)
        elif os.path.isdir(item_path):
            dir_node = create_dir_node(xml_node, item)
            gen_nodes_for_path(dir_node, item_path)


def gen_all_nodes(xml_node):
    global res_path
    gen_nodes_for_path(xml_node, res_path)


def clean_all_nodes(xml_node):
    for child in xml_node.getchildren():
        xml_node.remove(child)


def refresh_ccs(ccs_file):
    xml_tree = read_xml(ccs_file)

    root_folder_node = xml_tree.find('.//RootFolder')
    clean_all_nodes(root_folder_node)
    gen_all_nodes(root_folder_node)

    write_xml(xml_tree, ccs_file)


def main(argv):
    ccs_file = argv[0]
    if os.path.exists(ccs_file):
        root_path = os.path.dirname(os.path.abspath(ccs_file))
        global res_path
        res_path = os.path.join(root_path, 'cocosstudio')
        refresh_ccs(ccs_file)
    else:
        err_msg = "%s is not existed!" % ccs_file
        sys.stderr.write(err_msg)
        sys.exit(1)


if __name__ == "__main__":
    main(sys.argv[1:])
