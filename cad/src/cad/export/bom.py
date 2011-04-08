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
                                    'vender',
                                    'part number',
                                    'quantity',
                                    'cost',
                                    ]
        self.parameters_default = {}
        for key in self.parameters_key_list:
            self.parameters_default[key] = ''

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

        # self.object_map = {'union': {'header':'union() {block_open}',
        #                              'footer': '{block_close}'},
        #                    'intersection': {'header': 'intersection() {block_open}',
        #                                     'footer': '{block_close}'},
        #                    'difference': {'header': 'difference() {block_open}',
        #                                   'footer': '{block_close}'},
        #                    'merge': {'header': 'union() {block_open}',
        #                              'footer': '{block_close}'},
        #                    'box': {'header': 'cube(size = [{x:0.5f},{y:0.5f},{z:0.5f}], center = true);',
        #                            'footer': ''},
        #                    'sphere': {'header': 'sphere(r = {r:0.5f}, center = true);',
        #                               'footer': ''},
        #                    'cylinder': {'header': 'cylinder(h = {l:0.5f}, r = {r:0.5f}, center = true);',
        #                                 'footer': ''},
        #                    'cone': {'header': 'cylinder(h = {l:0.5f}, r1 = {r_neg:0.5f}, r2 = {r_pos:0.5f}, center = true);',
        #                             'footer': ''},
        #                    'extrusion': {'header': 'linear_extrude(file = "{profile}", height = {l:0.5f}, center = true, convexity=10);',
        #                             'footer': ''}}
        # {'header':'| {item_number} | {name} | {description} | {dimensions} | {vender} | {part_number} | {quantity} | {cost} |{block_open}',
        # self.item_str = '| {item_number} | {name} | {description} | {dimensions} | {vender} | {part_number} | {quantity} | {cost} |{block_open}'
        self.object_map = {'union': {'header':'| {item_number} | {name} | {description} | {dimensions} | {vender} | {part_number} | {quantity} | {cost} |{block_open}',
                                     'footer': '{block_close}'},
                           'intersection': {'header':'| {item_number} | {name} | {description} | {dimensions} | {vender} | {part_number} | {quantity} | {cost} |{block_open}',
                                            'footer': '{block_close}'},
                           'difference': {'header':'| {item_number} | {name} | {description} | {dimensions} | {vender} | {part_number} | {quantity} | {cost} |{block_open}',
                                          'footer': '{block_close}'},
                           'merge': {'header':'| {item_number} | {name} | {description} | {dimensions} | {vender} | {part_number} | {quantity} | {cost} |{block_open}',
                                     'footer': '{block_close}'},
                           'box': {'header':'| {item_number} | {name} | {description} | {dimensions} | {vender} | {part_number} | {quantity} | {cost} |{block_open}',
                                   'footer': ''},
                           'sphere': {'header':'| {item_number} | {name} | {description} | {dimensions} | {vender} | {part_number} | {quantity} | {cost} |{block_open}',
                                      'footer': ''},
                           'cylinder': {'header':'| {item_number} | {name} | {description} | {dimensions} | {vender} | {part_number} | {quantity} | {cost} |{block_open}',
                                        'footer': ''},
                           'cone': {'header':'| {item_number} | {name} | {description} | {dimensions} | {vender} | {part_number} | {quantity} | {cost} |{block_open}',
                                    'footer': ''},
                           'extrusion': {'header':'| {item_number} | {name} | {description} | {dimensions} | {vender} | {part_number} | {quantity} | {cost} |{block_open}',
                                    'footer': ''}}

    def get_file_header_str(self,filename,obj):
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

        bom_header = ''
        for item in bom.get_parameters_key_list():
            bom_header += '| {item} '.format(item = item)
        if bom_header != '':
            bom_header += '|\n|-\n'
        file_header_str += bom_header

        return file_header_str

    def get_obj_str(self,obj):
        obj_str = "."
        try:
            bom = obj.get_object_parameter('bom')
        except KeyError:
            bom = {}

        if bom != {}:
            primative = obj.get_primative()
            if primative != '':
                if primative in self.object_map:
                    obj_str = self.object_map[primative]['header']
                    obj_str = obj_str.format(block_open = '{block_open}',
                                             block_close = '{block_close}',
                                             item_number = bom.get_parameter('item number'),
                                             name = bom.get_parameter('name'),
                                             description = bom.get_parameter('description'),
                                             dimensions = bom.get_parameter('dimensions'),
                                             vender = bom.get_parameter('vender'),
                                             part_number = bom.get_parameter('part number'),
                                             quantity = bom.get_parameter('quantity'),
                                             cost = bom.get_parameter('cost'),
                                             )
        return obj_str

    def get_obj_header_str(self,obj,depth):
        # if 'color' in modifiers:
        #     color = modifiers['color']
        # else:
        #     color = []
        # angles = [a*(180/math.pi) for a in rotation]
        # obj_str = "{indent}{translate}{rotate}{scale}{color}"
        # if not numpy.allclose(position,[0,0,0]):
        #     translate_str = "translate(v=[{position[0]:0.5f},{position[1]:0.5f},{position[2]:0.5f}]){block_open} "
        # else:
        #     translate_str = ""
        # if not numpy.allclose(angles,[0,0,0]):
        #     rotate_str = "rotate(a=[{angles[0]:0.5f},{angles[1]:0.5f},{angles[2]:0.5f}]){block_open} "
        # else:
        #     rotate_str = ""
        # if not numpy.allclose(scale,[1,1,1]):
        #     scale_str = "scale(v=[{scale[0]:0.5f},{scale[1]:0.5f},{scale[2]:0.5f}]){block_open} "
        # else:
        #     scale_str = ""
        # if len(color) != 0:
        #     color_str = "color([{color[0]:0.5f},{color[1]:0.5f},{color[2]:0.5f},{color[3]:0.5f}]){block_open} "
        # else:
        #     color_str = ""
        # # obj_str = "{indent}translate(v=[{position[0]:0.5f},{position[1]:0.5f},{position[2]:0.5f}]){block_open} rotate(a=[{angle[0]:0.5f},{angle[1]:0.5f},{angle[2]:0.5f}]){block_open} scale(v=[{scale[0]:0.5f},{scale[1]:0.5f},{scale[2]:0.5f}]){block_open} color([{color[0]:0.5f},{color[1]:0.5f},{color[2]:0.5f},{color[3]:0.5f}]){block_open} {obj}\n"
        # obj_str = obj_str.format(indent = self.indent_str*depth,
        #                          translate = translate_str,
        #                          rotate = rotate_str,
        #                          scale = scale_str,
        #                          color = color_str)
        # obj_str = obj_str.format(block_open = '{block_open}',
        #                          position = position,
        #                          angles = angles,
        #                          scale = scale,
        #                          color = color)
        obj_str = ''
        obj_str += '{obj}\n'
        return obj_str

    def get_obj_footer_str(self,obj,depth):
        # if 'color' in modifiers:
        #     color = modifiers['color']
        # else:
        #     color = []
        # angles = [a*(180/math.pi) for a in rotation],
        # obj_footer_str = "{indent}{translate}{rotate}{scale}{color}{obj_footer}\n"
        # if not numpy.allclose(position,[0,0,0]):
        #     translate_str = "{block_close}"
        # else:
        #     translate_str = ""
        # if not numpy.allclose(angles,[0,0,0]):
        #     rotate_str = "{block_close}"
        # else:
        #     rotate_str = ""
        # if not numpy.allclose(scale,[1,1,1]):
        #     scale_str = "{block_close}"
        # else:
        #     scale_str = ""
        # if len(color) != 0:
        #     color_str = "{block_close}"
        # else:
        #     color_str = ""

        # footer_str = ""
        # if primative != '':
        #     if primative in self.object_map:
        #         footer_str = self.object_map[primative]['footer']

        # obj_footer_str = obj_footer_str.format(indent = self.indent_str*depth,
        #                                        translate = translate_str,
        #                                        rotate = rotate_str,
        #                                        scale = scale_str,
        #                                        color = color_str,
        #                                        obj_footer = footer_str)
        # obj_footer_str = "{indent}{block_close}{block_close}{block_close}{block_close}" + footer_str + "\n"
        # obj_footer_str = obj_footer_str.format(indent = self.indent_str*depth,
        #                                        block_close = '{block_close}')
        obj_footer_str = ''
        return obj_footer_str

if __name__ == "__main__":
    bom_export_map = BOMExportMap()
