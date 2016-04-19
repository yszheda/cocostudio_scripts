#!/usr/bin/env python
# coding:utf-8

import os
import sys
import xml.sax.xmlreader
import xml.sax.saxutils
from lxml import etree
import cStringIO


PLIST_KEY = 'PlistInfoProjectFile'
PROPERTY_KEY = 'PropertyGroup '
CONTENT_KEY = 'Content'
MAX_SIZE_KEY = 'MaxSize'
IMAGE_FILE_KEY = 'ImageFiles'


def get_property_attrib(name):
    return {
        'Type': 'Plist',
        'Name': name,
        'ID': '',
        'Version': '2.0.8.0',
    }


def get_content_attrib():
    return {
        'ExportType': 'Png',
        'SortAlgorithm': 'MaxRects',
        'PicturePadding': '0',
        'AllowRotation': 'True',
        'AllowAnySize': 'True',
        'AllowTrim': 'True',
        'ctype': 'PlistInfoData'
    }


def get_max_size_attrib():
    return {
        'Width': '2048',
        'Height': '2048',
    }


def read_xml(xml_string):
    parser = etree.XMLParser(remove_blank_text=True)
    return etree.parse(cStringIO.StringIO(xml_string), parser)


def write_xml(xml_tree, xml_file):
    xml_tree.write(xml_file, encoding="utf-8", pretty_print=True)


def gen_xml_content(csi_name):
    result = cStringIO.StringIO()
    x = xml.sax.saxutils.XMLGenerator(result)

    x.startDocument()
    x.startElement(PLIST_KEY, {})

    x.startElement(PROPERTY_KEY, get_property_attrib(csi_name))
    x.endElement(PROPERTY_KEY)

    x.startElement(CONTENT_KEY, get_content_attrib())

    x.startElement(IMAGE_FILE_KEY, {})
    x.endElement(IMAGE_FILE_KEY)

    x.startElement(MAX_SIZE_KEY, get_max_size_attrib())
    x.endElement(MAX_SIZE_KEY)

    x.endElement(CONTENT_KEY)

    x.endElement(PLIST_KEY)
    x.endDocument()

    s = result.getvalue()
    result.close()
    return s[s.find('\n') + 1:]


def main(argv):
    csi_file = argv[0]
    csi_name = os.path.basename(csi_file).split('.')[-2]

    xml_string = gen_xml_content(csi_name)
    xml_tree = read_xml(xml_string)
    write_xml(xml_tree, csi_file)


if __name__ == "__main__":
    main(sys.argv[1:])
