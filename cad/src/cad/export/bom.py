"""
Copyright 2010  IO Rodeo Inc.

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""
from __future__ import division
import copy
import math
import re
import textwrap
import numpy


class BOMObject(object):
    def __init__(self):
        self.parameters_key_list = ['item number',
                                    'name',
                                    'description',
                                    'dimensions',
                                    'vendor',
                                    'part number',
                                    'quantity',
                                    'cost',
                                    ]
        self.parameters_default = {}
        for key in self.parameters_key_list:
            self.parameters_default[key] = ''

        self.parameters_default['quantity'] = 1
        self.parameters_default['cost'] = 0.00
        self.set_parameters()

    def set_parameters(self,parameters={}):
        parameters = copy.deepcopy(parameters)
        if type(parameters) == dict:
            if len(parameters) == 0:
                self.parameters = self.parameters_default
            elif set(parameters.keys()) == set(self.parameters.keys()):
                self.parameters = parameters
            else:
                for key in parameter.keys():
                    self.set_parameter(key,parameters[key])

    def get_parameters(self):
        return copy.deepcopy(parameters)

    def set_parameter(self,key,value):
        if type(key) != str:
            key = str(key)
        self.parameters[key] = copy.deepcopy(value)
        if key not in set(self.parameters_key_list):
            self.parameters_key_list.append(key)

    def get_parameter(self,key):
        if type(key) != str:
            key = str(key)
        if key not in self.parameters.keys():
            return ''
        else:
            return copy.deepcopy(self.parameters[key])

    def get_parameters_key_list(self):
        return copy.deepcopy(self.parameters_key_list)

class BOMExportMap(object):
    def __init__(self,obj):
        self.indent_str = " "*4

        self.comment_str = "#"

        self.block_open_str = ""

        self.block_close_str = ""

        self.item_str = '| | {item_number} | {name} | {description} | {dimensions} | {vendor} | {part_number} | {quantity} | {cost} |\n'

    def get_file_header_str(self,obj,filename):
        width = 70
        str_ = '-*- mode:org -*-\n'
        str0 = self.comment_str + '='*(width-len(self.comment_str)*2) + self.comment_str + '\n'
        # see "http://docs.python.org/library/string.html#formatspec"
        str1 = (self.comment_str + '{0:=^{1}}' + self.comment_str).format(" " + filename + " ", width-len(self.comment_str)*2)
        str1 += '\n' + self.comment_str + ' '*(width-len(self.comment_str)*2) + self.comment_str + '\n'
        str2 = "Autogenerated using ros_cad. Hand editing this file is not advisable as all modifications will be lost when the program which generated this file is re-run."
        # str2 uses width-(len(self.comment_str)*2 + 1) because of the extra space after the initial slashes
        str2 = "\n".join((self.comment_str + " {0:<{1}}" + self.comment_str).format(l, width-(len(self.comment_str)*2 + 1)) for l in
                         textwrap.wrap(str2, width=width-(len(self.comment_str)*2 + 1)))
        file_header_str = str_ + str0 + str1 + str2 + '\n' + str0 + '\n'

        try:
            bom = obj.get_object_parameter('bom')
        except KeyError:
            bom = BOMObject()

        bom_header = '| ! '
        for item in bom.get_parameters_key_list():
            bom_header += '| {item} '.format(item = item)
        if bom_header != '':
            bom_header += '|\n|-\n'
        file_header_str += bom_header

        return file_header_str

    def convert_bom_to_str(self,bom):
        bom_str = ''
        if bom != {}:
            bom_str = self.item_str.format(item_number = bom.get_parameter('item number'),
                                           name = bom.get_parameter('name'),
                                           description = bom.get_parameter('description'),
                                           dimensions = bom.get_parameter('dimensions'),
                                           vendor = bom.get_parameter('vendor'),
                                           part_number = bom.get_parameter('part number'),
                                           quantity = bom.get_parameter('quantity'),
                                           cost = bom.get_parameter('cost'),
                                           )
        return bom_str

    def get_object_bom(self,obj):
        try:
            bom = obj.get_object_parameter('bom')
        except KeyError:
            bom = {}
        return bom

    def fill_bom_dict(self,obj,bom_dict={}):
        bom = self.get_object_bom(obj)
        if bom != {}:
            name = bom.get_parameter('name')
            if name in bom_dict.keys():
                item = bom_dict[name]
                quantity = item.get_parameter('quantity')
                if quantity == '':
                    quantity = 1
                quantity += 1
                item.set_parameter('quantity',quantity)
                bom_dict[name] = item
            else:
                bom_dict[name] = bom
        for o in obj.get_obj_list():
            bom_dict = self.fill_bom_dict(o,bom_dict)
        return bom_dict

    def get_objects_str(self,obj,depth=0):
        bom_dict = self.fill_bom_dict(obj)
        objects_str = ''
        colnum_list = []
        for key in bom_dict.keys():
            objects_str += self.convert_bom_to_str(bom_dict[key])
            colnum_list.append(len(bom_dict[key].get_parameters_key_list()))
        colnum = min(colnum_list)

        objects_str += '|-\n| # '
        objects_str += '| '*(colnum - 2)
        objects_str += '| total |'
        objects_str += ':=(@I$quantity..@II$quantity)*(@I$cost..@II$cost);%.2f;N'

        return objects_str

if __name__ == "__main__":
    bom_export_map = BOMExportMap()
