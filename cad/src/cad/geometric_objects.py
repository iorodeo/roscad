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
import copy

import csg_objects


class FiniteGeometricObject(csg_objects.CSGObject):
    def __init__(self):
        super(FiniteGeometricObject, self).__init__()
        self.dimensions = {}
        self.dimensions_default = {}
        self.set_color()

    def set_dimensions(self,*args,**kwargs):
        self.set_dimensions_(args,kwargs)
        # self.update_bounding_box()

    def set_dimensions_(self,args,kwargs):
        self.dimensions = self.fill_variable_with_args(args,kwargs,self.dimensions_default)

    def get_dimensions(self):
        return copy.deepcopy(self.dimensions)

    def set_dimension(self,dimension_name,value):
        self.dimensions[dimension_name] = copy.deepcopy(value)

    def get_dimension(self,dimension_name):
        return copy.deepcopy(self.dimensions[dimension_name])

    def get_obj_str(self,depth=0):
        obj_str_header = super(FiniteGeometricObject, self).get_obj_str(depth)
        obj_str = '{indent}dimensions = \n{indent}{dimensions:s}\n'
        obj_str = obj_str.format(indent = self.get_obj_parameter('indent_str')*depth,
                                 dimensions = str(self.get_dimensions()))
        obj_str = obj_str_header + obj_str
        return obj_str

if __name__ == "__main__":
    pass
