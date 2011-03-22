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


class CADObject(object):
    """CAD object wrapper base class."""

    def __init__(self, position=[0,0,0], orientation=[0,0,0,1], scale=1, exportable=False, modifiers={}):
        self.objlist = []
        self.set_position(position)

        self.set_orientation(orientation)

        self.set_scale(scale)

        self.set_exportable(exportable)

        self.set_modifiers(modifiers)

    def add_obj(self, obj):
        """Add a CAD object to the object list."""
        if type(obj) == list:
            self.objlist.extend(obj)
        else:
            self.objlist.append(obj)

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


    def cmd_str(self,tab_level=0):
        return 'CADObect'

    def __str__(self):
        rtn_str_header = '\nCADObject\n'
        rtn_str = 'class = \n{class_:s}\nposition = \n{position:s}\norientation = \n{orientation:s}\nscale = \n{scale:s}\nexportable = \n{exportable:s}\nmodifiers = \n{modifiers:s}\n'
        rtn_str = rtn_str.format(class_ = str(self.__class__),
                                 position = str(self.get_position()),
                                 orientation = str(self.get_orientation()),
                                 scale = str(self.get_scale()),
                                 exportable = str(self.get_exportable()),
                                 modifiers = str(self.get_modifiers()))

        rtn_str = rtn_str_header + rtn_str

        try:
            for obj in self.objlist:
                rtn_str = '%s%s'%(rtn_str,obj)
        except:
            pass

        return rtn_str

    def export(self,depth=0):
        pass

if __name__ == "__main__":
    cad_project = CADObject()
    cad_object = CADObject()
    cad_project.add_obj(cad_object)
    print cad_project
