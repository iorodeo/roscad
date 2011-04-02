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
import random

from export.export import export_maps


class CADObject(object):
    """CAD object wrapper base class."""

    def __init__(self):
        self.obj_list = []

        self.primative = ''

        self.modifiers_default = {'transformations': {'position': [0,0,0],
                                                      'orientation': [0,0,0,1],
                                                      'scale': [1,1,1]}}

        self.export_parameters_default = {'exportable': False,
                                          'indent_str': ' '*4}

        self.set_modifiers()

        self.set_export_parameters()

    def fill_variable_with_args(self,args,kwargs,variable):
        # print "args = \n" + str(args)
        # print "len(args) = \n" + str(len(args))
        # print "kwargs = \n" + str(kwargs)
        # print "variable before = \n" + str(variable)
        variable = copy.deepcopy(variable)
        if type(variable) == dict:
            variable_keys = variable.keys()
            variable_keys.sort()
            if 0 < len(kwargs.keys()):
                if (set(kwargs.keys()) == set(variable_keys)) or (len(variable) == 0):
                    variable = copy.deepcopy(kwargs)
                else:
                    for key in kwargs.keys():
                        variable[key] = kwargs[key]
            elif len(args) == 1:
                if (type(args[0]) == list) or (type(args[0]) == tuple):
                    if len(args[0]) == 1:
                        for key in variable_keys:
                            variable[key] = args[0][0]
                    elif len(args[0]) == len(variable_keys):
                        arg_list = list(args[0])
                        for key in variable_keys:
                            variable[key] = arg_list.pop(0)
                elif (type(args[0]) == dict):
                    if (set(args[0].keys()) == set(variable_keys)):
                        variable = args[0]
                else:
                    for key in variable_keys:
                        variable[key] = args[0]
            elif len(args) == len(variable_keys):
                args = list(args)
                for key in variable_keys:
                    variable[key] = args.pop(0)
        elif type(variable) == list:
            if 0 < len(kwargs.keys()):
                kwargs_keys = kwargs.keys()
                kwargs_keys.sort()
                if len(variable) == 0:
                    for key in kwargs_keys():
                        variable.append(kwargs[key])
                elif len(kwargs_keys) <= len(variable):
                    count = 0
                    for key in kwargs_keys():
                        variable[count] = kwargs[key]
                        count += 1
            elif len(args) == 1:
                arg = args[0]
                if (type(arg) == list):
                    variable = copy.deepcopy(arg)
                elif (type(arg) == tuple):
                    variable = copy.deepcopy(list(arg))
                elif (type(arg) == dict):
                    arg_keys = arg.keys()
                    arg_keys.sort()
                    variable = []
                    for key in arg.keys:
                        variable.append(arg[key])
                else:
                    l = len(variable)
                    variable = [copy.deepcopy(arg)]*l
            elif len(args) <= len(variable):
                for count in range(len(args)):
                    variable[count] = args[count]
            else:
                variable = copy.deepcopy(args)

        # print "variable after = \n" + str(variable)
        # print "\n"
        return variable

    def set_transformations(self,transformations):
        transformations_previous = self.get_transformations()
        transformations = self.fill_variable_with_args(transformations,transformations_previous)
        self.set_modifier('transformations',transformations)

    def get_transformations(self):
        self.get_modifier('transformations')

    def set_primative(self,primative):
        if type(primative) != str:
            primative = str(primative)
        self.primative = primative

    def get_primative(self):
        return self.primative

    def add_obj(self, obj):
        """Add a CAD object to the object list."""
        if type(obj) == list:
            self.obj_list.extend(obj)
        else:
            self.obj_list.append(obj)

    def set_obj_list(self,obj_list=[]):
        self.obj_list = []
        self.add_obj(obj_list)

    def get_obj_list(self):
        return self.obj_list

    def copy(self):
        return copy.deepcopy(self)

    def set_color(self,color=[],recursive=False):
        color = copy.deepcopy(color)
        if color == []:
            color = [random.random(),random.random(),random.random(),1]
        if len(color) == 3:
            color.append(1)
        self.set_modifier('color', color)
        # print "Setting color of " + self.get_class_name() + " to " + str(color)
        if recursive:
            for obj in self.get_obj_list():
                obj.set_color(color,recursive=True)

    def get_color(self):
        if 'color' not in self.modifiers:
            return []
        else:
            return copy.deepcopy(self.get_modifier('color'))

    def set_position(self,position=[0,0,0]):
        if len(position) == 3:
            self.modifiers['transformations']['position'] = copy.deepcopy(position)

    def get_position(self):
        return copy.deepcopy(self.modifiers['transformations']['position'])

    def set_orientation(self,orientation=[0,0,0,1]):
        if len(orientation) == 4:
            self.modifiers['transformations']['orientation'] = copy.deepcopy(orientation)

    def get_orientation(self):
        return copy.deepcopy(self.modifiers['transformations']['orientation'])

    def translate(self,translation=[0,0,0]):
        if len(translation) == 3:
            position = self.get_position()
            position[0] += translation[0]
            position[1] += translation[1]
            position[2] += translation[2]
            self.set_position(position)

    def set_scale(self,scale=1):
        self.modifiers['transformations']['scale'] = [1,1,1]
        new_scale = copy.deepcopy(scale)
        try:
            if len(new_scale) == 3:
                self.modifiers['transformations']['scale'][0] = new_scale[0]
                self.modifiers['transformations']['scale'][1] = new_scale[1]
                self.modifiers['transformations']['scale'][2] = new_scale[2]
            elif len(new_scale) == 1:
                self.modifiers['transformations']['scale'][0] = new_scale[0]
                self.modifiers['transformations']['scale'][1] = new_scale[0]
                self.modifiers['transformations']['scale'][2] = new_scale[0]
        except:
            self.modifiers['transformations']['scale'][0] = scale
            self.modifiers['transformations']['scale'][1] = scale
            self.modifiers['transformations']['scale'][2] = scale

    def get_scale(self):
        return copy.deepcopy(self.modifiers['transformations']['scale'])

    def set_exportable(self,exportable=False):
        if type(exportable) == bool:
            self.export_parameters['exportable'] = exportable

    def get_exportable(self):
        return self.export_parameters['exportable']

    def set_modifiers(self,modifiers={}):
        if modifiers == {}:
            modifiers = self.modifiers_default
        if type(modifiers) == dict:
            self.modifiers = copy.deepcopy(modifiers)

    def get_modifiers(self):
        return copy.deepcopy(self.modifiers)

    def set_modifier(self,key,value):
        if type(key) != str:
            key = str(key)
        self.modifiers[key] = copy.deepcopy(value)

    def get_modifier(self,key):
        if type(key) != str:
            key = str(key)
        return copy.deepcopy(self.modifiers[key])

    def set_export_parameters(self,export_parameters={}):
        if export_parameters == {}:
            export_parameters = self.export_parameters_default
        if type(export_parameters) == dict:
            self.export_parameters = copy.deepcopy(export_parameters)

    def get_export_parameters(self):
        return copy.deepcopy(self.export_parameters)

    def set_export_parameter(self,key,value):
        if type(key) != str:
            key = str(key)
        self.export_parameters[key] = copy.deepcopy(value)

    def get_export_parameter(self,key):
        if type(key) != str:
            key = str(key)
        return copy.deepcopy(self.export_parameters[key])

    def get_class_name(self):
        class_str = str(type(self))
        m = re.match(r"<.*[.][_]?(?P<classname>.*)[_]?'>",class_str)
        return m.group('classname')

    def get_obj_str(self,depth=0):
        obj_str = '{indent}class name = \n{indent}{classname}\n{indent}modifiers = \n{indent}{modifiers}\n{indent}export_parameters = \n{indent}{export_parameters}\n{indent}obj_list = \n{indent}{obj_list}\n'
        obj_str = obj_str.format(indent = self.get_export_parameter('indent_str')*depth,
                                 classname = str(self.get_class_name()),
                                 modifiers = str(self.get_modifiers()),
                                 export_parameters = str(self.get_export_parameters()),
                                 obj_list = str(self.get_obj_list()))
        return obj_str

    def __str__(self,depth=0):
        rtn_str = self.get_obj_str(depth)

        try:
            for obj in self.get_obj_list():
                rtn_str = '{rtn_str}{obj}'.format(rtn_str = rtn_str,
                                                  obj = obj.__str__(depth+1))
        except:
            pass

        return rtn_str

    def get_export_obj_str(self):
        export_obj_str = self.export_map.get_obj_str(self.get_primative())
        return export_obj_str

    def get_export_obj_header_str(self,depth):
        export_obj_str = self.get_export_obj_str()
        if export_obj_str != "":
            export_obj_header_str = self.export_map.get_obj_header_str(depth = depth,
                                                                       position = self.get_position(),
                                                                       rotation = self.get_rotation(),
                                                                       scale = self.get_scale(),
                                                                       modifiers = self.get_modifiers())
            export_obj_header_str = export_obj_header_str.format(block_open = '{block_open}',
                                                                 block_close = '{block_close}',
                                                                 obj = export_obj_str)
        else:
            export_obj_header_str = ""
        return export_obj_header_str

    def export(self,filename="export.scad",type=None,depth=0):
        # self.export_map = export_maps.export_maps.SCADExportMap(self.export_parameters)
        self.export_map = export_maps['scad'](self.export_parameters)
        if depth == 0:
            export_str = self.export_map.get_file_header_str(filename)
        else:
            export_str = ""
        export_obj_header_str = self.get_export_obj_header_str(depth)
        if export_obj_header_str != "":
            export_str += export_obj_header_str

            if 0 < len(self.get_obj_list()):
                for obj in self.get_obj_list():
                    export_str = '{export_str}{obj}'.format(export_str = export_str,
                                                            obj = obj.export(depth=(depth+1)),
                                                            block_open = '{block_open}',
                                                            block_close = '{block_close}')

            export_obj_footer_str = self.export_map.get_obj_footer_str(primative = self.get_primative(),
                                                                       depth = depth,
                                                                       position = self.get_position(),
                                                                       rotation = self.get_rotation(),
                                                                       scale = self.get_scale(),
                                                                       modifiers = self.get_modifiers())
            export_str = export_str + export_obj_footer_str

        if depth == 0:
            fid = open(filename, 'w')
            export_str = export_str.format(block_open = self.export_map.block_open_str,
                                           block_close = self.export_map.block_close_str)
            fid.write(export_str)
            fid.close()
        else:
            return export_str

    # Placeholder method
    def update_bounding_box(self):
        pass

if __name__ == "__main__":
    cad_project = CADObject()
    cad_object = CADObject()
    cad_project.add_obj(cad_object)
    print cad_project
    cad_project.export()
