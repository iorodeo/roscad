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

import export_maps


class CADObject(object):
    """CAD object wrapper base class."""

    def __init__(self, position=[0,0,0], orientation=[0,0,0,1], scale=1, exportable=False, modifiers={}):
        self.obj_list = []

        self.set_position(position)

        self.set_orientation(orientation)

        self.set_scale(scale)

        self.set_exportable(exportable)

        self.set_modifiers(modifiers)

        self.indent_str = " "*4

    def add_obj(self, obj):
        """Add a CAD object to the object list."""
        if type(obj) == list:
            self.obj_list.extend(obj)
        else:
            self.obj_list.append(obj)

    def copy(self):
        return copy.deepcopy(self)

    def set_position(self,position=[0,0,0]):
        if len(position) == 3:
            self.position = copy.deepcopy(position)

    def get_position(self):
        return copy.deepcopy(self.position)

    def set_orientation(self,orientation=[0,0,0,1]):
        if len(orientation) == 4:
            self.orientation = copy.deepcopy(orientation)

    def get_orientation(self):
        return copy.deepcopy(self.orientation)

    def translate(self,translation=[0,0,0]):
        if len(translation) == 3:
            position = self.get_position()
            position[0] += translation[0]
            position[1] += translation[1]
            position[2] += translation[2]
            self.set_position(position)

    def set_scale(self,scale=1):
        self.scale = [1,1,1]
        new_scale = copy.deepcopy(scale)
        try:
            if len(new_scale) == 3:
                self.scale[0] = new_scale[0]
                self.scale[1] = new_scale[1]
                self.scale[2] = new_scale[2]
            elif len(new_scale) == 1:
                self.scale[0] = new_scale[0]
                self.scale[1] = new_scale[0]
                self.scale[2] = new_scale[0]
        except:
            self.scale[0] = scale
            self.scale[1] = scale
            self.scale[2] = scale

    def get_scale(self):
        return copy.deepcopy(self.scale)

    def set_exportable(self,exportable=False):
        if type(exportable) == bool:
            self.exportable = exportable

    def get_exportable(self):
        return self.exportable

    def set_modifiers(self,modifiers={}):
        if type(modifiers) == dict:
            self.modifiers = copy.deepcopy(modifiers)

    def get_modifiers(self):
        return copy.deepcopy(self.modifiers)

    def add_modifier(self,key,value):
        if type(key) == str:
            self.modifiers[key] = copy.deepcopy(value)
        else:
            self.modifiers[str(key)] = copy.deepcopy(value)

    def get_modifier(self,key):
        if type(key) == str:
            return copy.deepcopy(self.modifiers[key])
        else:
            return copy.deepcopy(self.modifiers[str(key)])

    def get_class_name(self):
        class_str = str(type(self))
        m = re.match(r"<.*[.][_]?(?P<classname>.*)[_]?'>",class_str)
        return m.group('classname')

    def get_obj_str(self,depth=0):
        obj_str = '{indent}class name = \n{indent}{classname:s}\n{indent}position = \n{indent}{position:s}\n{indent}orientation = \n{indent}{orientation:s}\n{indent}scale = \n{indent}{scale:s}\n{indent}exportable = \n{indent}{exportable:s}\n{indent}modifiers = \n{indent}{modifiers:s}\n'
        obj_str = obj_str.format(indent = self.indent_str*depth,
                                 classname = str(self.get_class_name()),
                                 position = str(self.get_position()),
                                 orientation = str(self.get_orientation()),
                                 scale = str(self.get_scale()),
                                 exportable = str(self.get_exportable()),
                                 modifiers = str(self.get_modifiers()))
        return obj_str

    def __str__(self,depth=0):
        rtn_str = self.get_obj_str(depth)

        try:
            for obj in self.obj_list:
                rtn_str = '{rtn_str}{obj}\n'.format(rtn_str = rtn_str,
                                                    obj = obj.__str__(depth+1))
        except:
            pass

        return rtn_str

    def get_export_obj_str(self):
        class_name = self.get_class_name()
        export_obj_str = self.export_map.get_obj_str(class_name)
        return export_obj_str

    def get_export_obj_header_str(self,depth):
        export_obj_str = self.get_export_obj_str()
        export_obj_header_str = self.export_map.get_obj_header_str()
        export_obj_header_str = export_obj_header_str.format(indent = self.export_map.indent_str*depth,
                                                             block_open = self.export_map.block_open_str,
                                                             position = self.position,
                                                             angle = [a*(180/math.pi) for a in self.get_rotation()],
                                                             scale = self.scale,
                                                             obj = export_obj_str)
        return export_obj_header_str

    def export(self,filename="export.txt",type=None,depth=0):
        self.export_map = export_maps.SCADExportMap()
        if self.exportable == True:
            export_file_header_str = self.export_map.get_file_header_str(filename,depth)
            export_obj_header_str = self.get_export_obj_header_str(depth)
            export_str = export_file_header_str + export_obj_header_str

        try:
            for obj in self.obj_list:
                export_str = '{export_str}{obj}\n'.format(export_str = export_str,
                                                          obj = obj.export(depth=(depth+1)))
        except:
            pass

        export_obj_footer_str = self.export_map.get_obj_footer_str(depth)
        export_str = export_str + export_obj_footer_str

        if depth == 0:
            fid = open(filename, 'w')
            fid.write('{export_str}'.format(export_str = export_str))
            fid.close()
        else:
            return export_str

if __name__ == "__main__":
    cad_project = CADObject()
    cad_object = CADObject()
    cad_project.add_obj(cad_object)
    print cad_project
    cad_project.export()
