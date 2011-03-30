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


class POVRAYExportMap(object):
    def __init__(self,export_file_parameters={}):
        self.indent_str = " "*4

        self.comment_str = "//"

        self.block_open_str = "{"

        self.block_close_str = "}"

        if type(export_file_parameters) == dict:
            self.export_file_parameters = copy.deepcopy(export_file_parameters)

        self.fn_default = 50

        self.object_map = {'Union': {'header':'union() {block_open}',
                                     'footer': '{block_close}'},
                           'Intersection': {'header': 'intersection() {block_open}',
                                            'footer': '{block_close}'},
                           'Difference': {'header': 'difference() {block_open}',
                                          'footer': '{block_close}'},
                           'Merge': {'header': 'union() {block_open}',
                                     'footer': '{block_close}'},
                           'Box': {'header': 'cube(size = [{x:0.5f},{y:0.5f},{z:0.5f}], center = true);',
                                   'footer': ''},
                           'Sphere': {'header': 'sphere(r = {r:0.5f}, center = true);',
                                      'footer': ''},
                           'Cylinder': {'header': 'cylinder(h = {l:0.5f}, r = {r:0.5f}, center = true);',
                                        'footer': ''},
                           'Cone': {'header': 'cylinder(h = {l:0.5f}, r1 = {r_neg:0.5f}, r2 = {r_pos:0.5f}, center = true);',
                                    'footer': ''}}

    def get_file_header_str(self,filename):
        width = 70
        str0 = self.comment_str + '='*(width-len(self.comment_str)*2) + self.comment_str + '\n'
        # see "http://docs.python.org/library/string.html#formatspec"
        str1 = '//{0:=^{1}}//'.format(" " + filename + " ", width-len(self.comment_str)*2)
        str1 += '\n' + self.comment_str + ' '*(width-len(self.comment_str)*2) + self.comment_str + '\n'
        str2 = "Autogenerated using ros_cad. Hand editing this file is not advisable as all modifications will be lost when the program which generated this file is re-run."
        # str2 uses width-(len(self.comment_str)*2 + 1) because of the extra space after the initial slashes
        str2 = "\n".join((self.comment_str + " {0:<{1}}" + self.comment_str).format(l, width-(len(self.comment_str)*2 + 1)) for l in
                         textwrap.wrap(str2, width=width-(len(self.comment_str)*2 + 1)))
        file_header_str = str0 + str1 + str2 + '\n' + str0 + '\n'

        facets_written = False
        try:
            file_header_str += '$fn = {facets.fn:d};\n'.format(facets = self.export_file_parameters['facets'])
            facets_written = True
        except:
            pass
        try:
            file_header_str += '$fa = {facets.fa:d};\n'.format(facets = self.export_file_parameters['facets'])
            facets_written = True
        except:
            pass
        try:
            file_header_str += '$fs = {facets.fs:d};\n'.format(facets = self.export_file_parameters['facets'])
            facets_written = True
        except:
            pass
        if not facets_written:
            file_header_str += '$fn = {fn:d};\n'.format(fn = self.fn_default)

        return file_header_str

    def get_obj_str(self,class_name):
        try:
            obj_str = self.object_map[class_name]['header']
        except:
            obj_str = ""
        return obj_str

    def get_obj_header_str(self,depth,position,rotation,scale,modifiers):
        if 'color' in modifiers:
            color = modifiers['color']
        else:
            color = []
        angles = [a*(180/math.pi) for a in rotation]
        obj_str = "{indent}{translate}{rotate}{scale}{color}"
        if not numpy.allclose(position,[0,0,0]):
            translate_str = "translate(v=[{position[0]:0.5f},{position[1]:0.5f},{position[2]:0.5f}]){block_open} "
        else:
            translate_str = ""
        if not numpy.allclose(angles,[0,0,0]):
            rotate_str = "rotate(a=[{angles[0]:0.5f},{angles[1]:0.5f},{angles[2]:0.5f}]){block_open} "
        else:
            rotate_str = ""
        if not numpy.allclose(scale,[1,1,1]):
            scale_str = "scale(v=[{scale[0]:0.5f},{scale[1]:0.5f},{scale[2]:0.5f}]){block_open} "
        else:
            scale_str = ""
        if len(color) != 0:
            color_str = "color([{color[0]:0.5f},{color[1]:0.5f},{color[2]:0.5f},{color[3]:0.5f}]){block_open} "
        else:
            color_str = ""
        # obj_str = "{indent}translate(v=[{position[0]:0.5f},{position[1]:0.5f},{position[2]:0.5f}]){block_open} rotate(a=[{angle[0]:0.5f},{angle[1]:0.5f},{angle[2]:0.5f}]){block_open} scale(v=[{scale[0]:0.5f},{scale[1]:0.5f},{scale[2]:0.5f}]){block_open} color([{color[0]:0.5f},{color[1]:0.5f},{color[2]:0.5f},{color[3]:0.5f}]){block_open} {obj}\n"
        obj_str = obj_str.format(indent = self.indent_str*depth,
                                 translate = translate_str,
                                 rotate = rotate_str,
                                 scale = scale_str,
                                 color = color_str)
        obj_str = obj_str.format(block_open = '{block_open}',
                                 position = position,
                                 angles = angles,
                                 scale = scale,
                                 color = color)
        obj_str += '{obj}\n'
        return obj_str

    def get_obj_footer_str(self,class_name,depth,position,rotation,scale,modifiers):
        if 'color' in modifiers:
            color = modifiers['color']
        else:
            color = []
        angles = [a*(180/math.pi) for a in rotation],
        obj_footer_str = "{indent}{translate}{rotate}{scale}{color}{obj_footer}\n"
        if not numpy.allclose(position,[0,0,0]):
            translate_str = "{block_close}"
        else:
            translate_str = ""
        if not numpy.allclose(angles,[0,0,0]):
            rotate_str = "{block_close}"
        else:
            rotate_str = ""
        if not numpy.allclose(scale,[1,1,1]):
            scale_str = "{block_close}"
        else:
            scale_str = ""
        if len(color) != 0:
            color_str = "{block_close}"
        else:
            color_str = ""

        try:
            footer_str = self.object_map[class_name]['footer']
        except:
            footer_str = ""

        obj_footer_str = obj_footer_str.format(indent = self.indent_str*depth,
                                               translate = translate_str,
                                               rotate = rotate_str,
                                               scale = scale_str,
                                               color = color_str,
                                               obj_footer = footer_str)
        # obj_footer_str = "{indent}{block_close}{block_close}{block_close}{block_close}" + footer_str + "\n"
        # obj_footer_str = obj_footer_str.format(indent = self.indent_str*depth,
        #                                        block_close = '{block_close}')
        return obj_footer_str

if __name__ == "__main__":
    povray_export_map = POVRAYExportMap()