#!/usr/bin/env python
# coding:utf-8
# Refresh cocostudio SpriteFrameSheet *.csi


import os
import sys
# import xml.etree.ElementTree as ET
from lxml import etree

PNG_EXT = ".png"
IMAGE_KEY = "FilePathData"

# NOTE: MAX_SIZE needs to be a string
MAX_SIZE = "2048"


def get_atlas_name(csi_file):
    csi_file_name = os.path.basename(csi_file)
    return os.path.splitext(csi_file_name)[0]


def get_res_path(csi_file):
    atlas_name = get_atlas_name(csi_file)
    csi_path = os.path.abspath(os.path.dirname(csi_file))
    return csi_path + "/../" + atlas_name + "/"


def read_xml(xml_file):
    parser = etree.XMLParser(remove_blank_text=True)
    return etree.parse(xml_file, parser)


def write_xml(xml_tree, xml_file):
    xml_tree.write(xml_file, encoding="utf-8", pretty_print=True)


def update_max_size(xml_node):
    max_size_node = xml_node.find('MaxSize')
    max_size_node.set('Width', MAX_SIZE)
    max_size_node.set('Height', MAX_SIZE)


def clear_images(xml_node):
    for image_file in xml_node.findall(IMAGE_KEY):
        xml_node.remove(image_file)


def add_image(xml_node, image_name):
    element = etree.Element(IMAGE_KEY, {"Path": image_name})
    xml_node.append(element)


def is_image(file_name):
    if os.path.exists(file_name):
        if os.path.splitext(file_name)[1] == PNG_EXT:
            return True
    return False


def get_image_names(csi_file):
    atlas_name = get_atlas_name(csi_file)
    res_path = get_res_path(csi_file)
    image_names = set()

    for root, dirs, files in os.walk(res_path):
        for file_name in files:
            if is_image(root + file_name):
                image_name = atlas_name + "/" + file_name
                image_names.add(image_name)

    return image_names


def refresh_csi(csi_file):
    xml_tree = read_xml(csi_file)

    xml_root = xml_tree.getroot()
    content_node = xml_root.find('Content')
    images_node = content_node.find('ImageFiles')

    clear_images(images_node)
    for image_name in get_image_names(csi_file):
        add_image(images_node, image_name)

    update_max_size(content_node)

    write_xml(xml_tree, csi_file)


def main(argv):
    csi_file = argv[0]
    if os.path.exists(csi_file):
        refresh_csi(csi_file)
    else:
        err_msg = "%s is not existed!" % csi_file
        sys.stderr.write(err_msg)
        sys.exit(1)


if __name__ == "__main__":
    main(sys.argv[1:])
