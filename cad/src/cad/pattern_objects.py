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
import csg_objects as csg


class LinearArray(csg.Union):
    def __init__(self,obj=[],x=[0],y=[0],z=[0]):
        super(LinearArray, self).__init__()
        self._set_array_values(x,y,z)
        self._set_dimensions(x,y,z)
        self._fill_array(obj,x,y,z)

    def _set_array_values(self,x,y,z):
        self.array_values = {'x': copy.deepcopy(x),
                             'y': copy.deepcopy(y),
                             'z': copy.deepcopy(z)}

    def get_array_values(self):
        return copy.deepcopy(self.array_values)

    def _set_dimensions(self,x,y,z):
        self.dimensions = {'x': len(x),
                           'y': len(y),
                           'z': len(z)}

    def get_dimensions(self):
        return copy.deepcopy(self.dimensions)

    def _fill_array(self,obj,x,y,z):
        self.set_obj_list()
        for zn in z:
            for yn in y:
                for xn in x:
                    obj_copy = obj.copy()
                    obj_copy.translate([xn,yn,zn])
                    self.add_obj(obj_copy)

    def set_array(self,x=[0],y=[0],z=[0]):
        self._set_dimensions(x,y,z)
        obj_list = self.get_obj_list()
        obj = obj_list[0]
        self._fill_array(obj,x,y,z)


if __name__ == "__main__":
    import finite_solid_objects as fso

    obj = fso.Cylinder()
    x = [-5,5]
    y = [-5,5]
    z = [0]
    pattern = LinearArray(obj,x,y,z)
    pattern.export()
