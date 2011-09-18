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


class PovrayPoints(object):
    def __init__(self,points,decimals=5,indent_str="",depth=0):
        self.points = points
        self.decimals = decimals
        self.indent_str = indent_str
        self.depth = depth

    def __str__(self):
        return_str = "[\n"
        for point in self.points:
            return_str += self.indent_str*self.depth*3 + "["
            for number in point:
                number_format_str = "{number:." + str(self.decimals) + "f}"
                number_str = number_format_str.format(number=number)
                return_str += number_str
                return_str += ","
            return_str = return_str[:-1]
            return_str += "],\n"
        return_str = return_str[:-2]
        return_str += "]"
        return return_str

class POVRAYExportMap(object):
    def __init__(self,obj):
        self.indent_str = " "*4

        self.comment_str = "//"

        self.block_open_str = "{"

        self.block_close_str = "}"

        self.object_map = {'union': {'header':'union {block_open}',
                                     'footer': '{block_close}'},
                           'intersection': {'header': 'intersection {block_open}',
                                            'footer': '{block_close}'},
                           'difference': {'header': 'difference {block_open}',
                                          'footer': '{block_close}'},
                           'merge': {'header': 'merge {block_open}',
                                     'footer': '{block_close}'},
                           'box': {'header': 'box {block_open} <-{x:0.5f},-{y:0.5f},-{z:0.5f}>,<{x:0.5f},{y:0.5f},{z:0.5f}>',
                                   'footer': '{block_close}'},
                           'sphere': {'header': 'sphere {block_open} <0,0,0>,{r:0.5f}',
                                      'footer': '{block_close}'},
                           'cylinder': {'header': 'cylinder {block_open} <0,0,-{l:0.5f}>,<0,0,{l:0.5f}>,{r:0.5f}',
                                        'footer': '{block_close}'},
                           'cone': {'header': 'cone {block_open} <0,0,-{l:0.5f}>,{r_neg:0.5f},<0,0,{l:0.5f}>,{r_pos:0.5f}',
                                    'footer': ''},
                           'extrusion': {'header': 'linear_extrude(height = {l:0.5f}, center = true, convexity = 10, twist = 0) {block_open}',
                                         'footer': '{block_close}'},
                           'rotation': {'header': 'rotate_extrude(convexity = 10) {block_open}',
                                         'footer': '{block_close}'},
                           'polygon':  {'header': 'polygon(\n{indent}{indent}points = {points},\n{indent}{indent}paths = {paths});',
                                        'footer': ''},
                           }

    def get_file_header_str(self,obj,filename):
        width = 70
        str0 = self.comment_str + '='*(width-len(self.comment_str)*2) + self.comment_str + '\n'
        # see "http://docs.python.org/library/string.html#formatspec"
        str1 = (self.comment_str + '{0:=^{1}}' + self.comment_str).format(" " + filename + " ", width-len(self.comment_str)*2)
        str1 += '\n' + self.comment_str + ' '*(width-len(self.comment_str)*2) + self.comment_str + '\n'
        str2 = "Autogenerated using ros_cad. Hand editing this file is not advisable as all modifications will be lost when the program which generated this file is re-run."
        # str2 uses width-(len(self.comment_str)*2 + 1) because of the extra space after the initial slashes
        str2 = "\n".join((self.comment_str + " {0:<{1}}" + self.comment_str).format(l, width-(len(self.comment_str)*2 + 1)) for l in
                         textwrap.wrap(str2, width=width-(len(self.comment_str)*2 + 1)))
        file_header_str = str0 + str1 + str2 + '\n' + str0 + '\n'


        # defaults
        try:
            file_header_str += "#version {version:0.1f};\n".format(version = obj.get_object_parameter('povray_version'))
        except KeyError:
            file_header_str += ""
        try:
            file_header_str += "global_settings { assumed_gamma {assumed_gamma:0.1f} }\n".format(assumed_gamma = obj.get_object_parameter('assumed_gamma'))
        except KeyError:
            file_header_str += "global_settings { assumed_gamma 1.0 }\n"
        try:
            file_header_str += "#default { finish { ambient {default_ambient:0.1f} diffuse {default_diffuse:0.1f} } }\n".format(default_ambient = obj.get_object_parameter('default_ambient'),
                                                                                                                             default_diffuse = obj.get_object_parameter('default_diffuse'))
        except KeyError:
            file_header_str += "#default { finish { ambient 0.1 diffuse 0.9 } }\n"
        file_header_str += str0

        # includes
        file_header_str += '#include "colors.inc"\n'
        file_header_str += '#include "textures.inc"\n'
        file_header_str += '#include "glass.inc"\n'
        file_header_str += '#include "metals.inc"\n'
        file_header_str += '#include "golds.inc"\n'
        file_header_str += '#include "stones.inc"\n'
        file_header_str += '#include "woods.inc"\n'
        file_header_str += str0

        # camera
        file_header_str += "camera {\n"
        try:
            file_header_str += "{indent}{projection}\n".format(indent = self.indent_str, projection = obj.get_object_parameter('camera_projection'))
        except KeyError:
            pass
        file_header_str += "{indent}right -x*image_width/image_height\n".format(indent = self.indent_str) # make right-handed coordinate system
        file_header_str += "{indent}sky <0,0,1>\n".format(indent = self.indent_str)
        try:
            camera_location = obj.get_object_parameter('camera_location')
            file_header_str += "{indent}location <{camera_location[0]:0.5f},{camera_location[1]:0.5f},{camera_location[2]:0.5f}>\n".format(indent = self.indent_str, camera_location = camera_location)
        except KeyError:
            file_header_str += "{indent}location <-10000.0,-10000.0,10000.0>\n".format(indent = self.indent_str)
        try:
            camera_look_at = obj.get_object_parameter('camera_look_at')
            file_header_str += "{indent}look_at <{camera_look_at[0]:0.5f},{camera_look_at[1]:0.5f},{camera_look_at[2]:0.5f}>\n".format(indent = self.indent_str, camera_look_at = camera_look_at)
        except KeyError:
            file_header_str += "{indent}look_at <0,0,0>\n".format(indent = self.indent_str)
        try:
            file_header_str += "{indent}angle {angle:0.5f}\n".format(indent = self.indent_str,angle = obj.get_object_parameter('camera_angle'))
        except KeyError:
            # file_header_str += "{indent}angle 75\n".format(indent = self.indent_str)
            pass
        file_header_str += "}\n"
        file_header_str += str0

        # light sources
        file_header_str += "light_source {< -3000, 3000, -3000> color rgb <1.0,1.0,1.0>}\n"
        file_header_str += str0

        # sky sphere
        file_header_str += "sky_sphere { pigment { color rgb <1.0,1.0,1.0>} }\n"
        file_header_str += str0

        return file_header_str

    def get_dimensions_from_polygon(self,obj,depth):
        dimensions = obj.get_dimensions()
        points = obj.get_points()
        # print "points = "
        # print points
        decimals = obj.get_decimals()
        povray_points = PovrayPoints(points,decimals,self.indent_str,depth)
        dimensions['points'] = povray_points
        paths = obj.get_paths()
        dimensions['paths'] = paths
        return dimensions

    def get_object_str(self,obj,depth):
        primative = obj.get_primative()
        obj_str = ""
        if primative != '':
            if primative in self.object_map:
                if primative == 'polygon':
                    dimensions = self.get_dimensions_from_polygon(obj,depth)
                else:
                    dimensions = obj.get_dimensions()
                if primative == 'box':
                    dimensions['x'] /= 2
                    dimensions['y'] /= 2
                    dimensions['z'] /= 2
                elif (primative == 'cylinder') or (primative == 'cone'):
                    dimensions['l'] /= 2
                dimensions['block_open'] = '{block_open}'
                dimensions['block_close'] = '{block_close}'
                dimensions['indent'] = self.indent_str*depth
                obj_str = self.object_map[primative]['header']
                obj_str = obj_str.format(**dimensions)
        return obj_str

    def get_object_header_str(self,obj,depth):
        # position = obj.get_position()
        # rotation = obj.get_rotation()
        # scale = obj.get_scale()
        # parameters = obj.get_object_parameters()

        # if 'color' in parameters:
        #     color = parameters['color']
        # else:
        #     color = []
        # if 'slice' in parameters:
        #     slice = parameters['slice']
        # else:
        #     slice = False
        # angles = [a*(180/math.pi) for a in rotation]

        # obj_str = "{indent}{slice}{translate}{rotate}{scale}{color}"

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
        # if slice:
        #     slice_str = "projection(cut=true){block_open} "
        # else:
        #     slice_str = ""

        # obj_str = obj_str.format(indent = self.indent_str*depth,
        #                          slice = slice_str,
        #                          translate = translate_str,
        #                          rotate = rotate_str,
        #                          scale = scale_str,
        #                          color = color_str)
        # obj_str = obj_str.format(block_open = '{block_open}',
        #                          position = position,
        #                          angles = angles,
        #                          scale = scale,
        #                          color = color)
        # obj_str += '{obj}\n'
        obj_str = '{indent}'.format(indent = self.indent_str*depth)
        obj_str += '{obj}\n'
        return obj_str

    def get_object_footer_str(self,obj,depth):
        primative = obj.get_primative()
        position = obj.get_position()
        rotation = obj.get_rotation()
        scale = obj.get_scale()
        parameters = obj.get_object_parameters()

        if 'color' in parameters:
            color = parameters['color']
        else:
            color = []

        angles = [a*(180/math.pi) for a in rotation]

        obj_footer_str = ""

        if len(color) != 0:
            texture_str = "{indent}texture {block_open} pigment {block_open} color rgb<{color[0]:0.5f},{color[1]:0.5f},{color[2]:0.5f}> {block_close} finish {block_open} phong 1 reflection 0.00{block_close}{block_close}\n"
            texture_str = texture_str.format(indent = self.indent_str*(depth+1),
                                             block_open = '{block_open}',
                                             block_close = '{block_close}',
                                             color = color)
        else:
            texture_str = ""

        if not numpy.allclose(scale,[1,1,1]):
            scale_str = "scale <{scale[0]:0.5f},{scale[1]:0.5f},{scale[2]:0.5f}> "
        else:
            scale_str = ""
        if not numpy.allclose(angles,[0,0,0]):
            rotate_str = "rotate <{angles[0]:0.5f},{angles[1]:0.5f},{angles[2]:0.5f}> "
        else:
            rotate_str = ""
        if not numpy.allclose(position,[0,0,0]):
            translate_str = "translate <{position[0]:0.5f},{position[1]:0.5f},{position[2]:0.5f}> "
        else:
            translate_str = ""

        if not((scale_str == "") and (rotate_str == "") and (translate_str == "")):
            transformation_str = "{indent}{scale}{rotate}{translate}\n"
            transformation_str = transformation_str.format(indent = self.indent_str*(depth+1),
                                                           scale = scale_str,
                                                           rotate = rotate_str,
                                                           translate = translate_str)

            transformation_str = transformation_str.format(block_open = '{block_open}',
                                                           block_close = '{block_close}',
                                                           position = position,
                                                           angles = angles,
                                                           scale = scale)
        else:
            transformation_str = ""

        footer_str = ""
        if primative != '':
            if primative in self.object_map:
                footer_str = "{indent}"
                footer_str += self.object_map[primative]['footer']
                footer_str += "\n"
                footer_str = footer_str.format(indent = self.indent_str*depth,
                                               block_open = '{block_open}',
                                               block_close = '{block_close}',
                                               )

        obj_footer_str = texture_str + transformation_str + footer_str

        return obj_footer_str

    def get_objects_str(self,obj,depth=0):
        objects_str = ''
        obj_str = self.get_object_str(obj,depth)
        if obj_str != '':
            obj_header_str = self.get_object_header_str(obj,depth)
            obj_header_str = obj_header_str.format(block_open = '{block_open}',
                                                   block_close = '{block_close}',
                                                   obj = obj_str)
        else:
            obj_header_str = ''
        if obj_header_str != '':
            objects_str += obj_header_str

            if 0 < len(obj.get_obj_list()):
                for o in obj.get_obj_list():
                    objects_str = '{objects_str}{obj}'.format(objects_str = objects_str,
                                                              obj = self.get_objects_str(o,(depth+1)),
                                                              block_open = '{block_open}',
                                                              block_close = '{block_close}')
            obj_footer_str = self.get_object_footer_str(obj,depth)
            objects_str += obj_footer_str


        if depth == 0:
            objects_str = objects_str.format(block_open = self.block_open_str,
                                             block_close = self.block_close_str)

        return objects_str
        # export_obj_str = self.export_map.get_obj_str(obj=self)
        # return export_obj_str

        # def get_export_obj_header_str(self,depth):
        #     export_obj_str = self.get_export_obj_str()
        #     if export_obj_str != "":
        #         export_obj_header_str = self.export_map.get_obj_header_str(obj = self,
        #                                                                    depth = depth)
        #         export_obj_header_str = export_obj_header_str.format(block_open = '{block_open}',
        #                                                              block_close = '{block_close}',
        #                                                              obj = export_obj_str)
        #     else:
        #         export_obj_header_str = ""
        #     return export_obj_header_str

        # if depth == 0:
        #     # export_str_list = []
        #     # export_str_list.append(self.export_map.get_file_header_str(filename))
        #     export_str = self.export_map.get_file_header_str(filename,self)
        # else:
        #     export_str = ""
        # export_obj_header_str = self.get_export_obj_header_str(depth)
        # if export_obj_header_str != "":
        #     # print "export_obj_header_str = " + export_obj_header_str
        #     # print "export_obj_header_str == '.\n' " + str(export_obj_header_str == '.\n')
        #     if export_obj_header_str != '.\n':
        #         export_str += export_obj_header_str
        #     # export_str_list.append(export_obj_header_str)

        #     if 0 < len(self.get_obj_list()):
        #         for obj in self.get_obj_list():
        #             # export_str = '{export_str}{obj}'.format(export_str = export_str,
        #             #                                         obj = obj.export(depth=(depth+1)),
        #             #                                         block_open = '{block_open}',
        #             #                                         block_close = '{block_close}')
        #             export_str = '{export_str}{obj}'.format(export_str = export_str,
        #                                                     obj = obj.export(filename=filename,depth=(depth+1)),
        #                                                     block_open = '{block_open}',
        #                                                     block_close = '{block_close}')

        #     export_obj_footer_str = self.export_map.get_obj_footer_str(obj = self,
        #                                                                depth = depth)
        #     export_str = export_str + export_obj_footer_str

        # if depth == 0:
        #     fid = open(filename, 'w')
        #     # for export_str in export_str_list:
        #     #     export_str = export_str.format(block_open = self.export_map.block_open_str,
        #     #                                    block_close = self.export_map.block_close_str)
        #     #     fid.write(export_str)
        #     export_str = export_str.format(block_open = self.export_map.block_open_str,
        #                                    block_close = self.export_map.block_close_str)
        #     fid.write(export_str)
        #     fid.close()
        # else:
        #     return export_str


if __name__ == "__main__":
    povray_export_map = POVRAYExportMap()
