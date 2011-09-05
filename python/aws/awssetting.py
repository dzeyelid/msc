#!/usr/bin/env python
# coding: utf-8

from xml.etree import ElementTree
from xml.etree.ElementTree import Element, SubElement
from xml.dom import minidom

import os.path
import sys


class AwsSetting:

    def save(self, data):
        # define variables
        xml_file_name = './awssetting.xml'

        # create dom
        root = None
        if os.path.exists(xml_file_name) == True:
            root = ElementTree.parse(open(xml_file_name)).getroot()
        else:
            root = Element('setting')

        # create xml dom
        keys_basic = ['ownerid', 'region']
        node_basic = SubElement(root, 'basic')
        for key in keys_basic:
            node = SubElement(node_basic, key)
            node.text = data[key]

        keys_security_group = ['security_group_name']
        for key in keys_security_group:
            node = SubElement(root, 'security_group')
            node.text = data[key]

        # format
        rough_string = ElementTree.tostring(root, 'utf-8')
        reparsed = minidom.parseString(rough_string)
        reparsed = reparsed.toprettyxml(indent='    ')

        # write into a xml file
        f = open(xml_file_name, 'w')
        f.write(reparsed)
        f.close()

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print "Plese give some argment."
        print "example : python awssetting.py ownerid region security_group_name"
        sys.exit(2)

    data = {}
    data['ownerid'] = sys.argv[1]
    data['region'] = sys.argv[2]
    data['security_group_name'] = sys.argv[3]

    setting = AwsSetting()
    setting.save(data)
