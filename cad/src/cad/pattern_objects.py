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


class _PatternObject(csg.Union):
    def __init__(self):
        super(_PatternObject, self).__init__()

class ArbitraryArray(_PatternObject):
    def __init__(self,obj,point_list=[[0,0,0]]):
        super(ArbitraryArray, self).__init__()
        self.point_list = self._condition_point_list(point_list)
        self._fill_array(obj)

    def _condition_point_list(self,point_list):
        point_list_conditioned = []
        for point in point_list:
            if len(point) == 3:
                point_list_conditioned.append(copy.deepcopy(point))
            elif len(point) == 2:
                point3 = [point[0],point[1],0]
                point_list_conditioned.append(copy.deepcopy(point3))
            else:
                raise ValueError("point_list must contain a list of points and the length of each point must equal 2 or 3.")
        return point_list_conditioned

    def get_point_list(self):
        return copy.deepcopy(self.point_list)

    def _fill_array(self,obj):
        self.set_obj_list()
        for point in self.point_list:
            xn = point[0]
            yn = point[1]
            zn = point[2]
            obj_copy = obj.copy()
            obj_copy.translate([xn,yn,zn])
            self.add_obj(obj_copy)


class LinearArraySet(ArbitraryArray):
    def __init__(self,obj,x=[[0]],y=[[0]],z=[[0]]):
        point_list = self._make_point_list(x,y,z)
        super(LinearArraySet, self).__init__(obj,point_list)

    def _make_point_list(self,x,y,z):
        x_len = len(x)
        y_len = len(y)
        z_len = len(z)
        set_count = max([x_len,y_len,z_len])
        if x_len == 1:
            for i in range(1,set_count):
                x.append(x[0])
        elif x_len != set_count:
            raise ValueError("len(x) must equal 1 or max([len(y),len(z)])")
        if y_len == 1:
            for i in range(1,set_count):
                y.append(y[0])
        elif y_len != set_count:
            raise ValueError("len(y) must equal 1 or max([len(x),len(z)])")
        if z_len == 1:
            for i in range(1,set_count):
                z.append(z[0])
        elif z_len != set_count:
            raise ValueError("len(z) must equal 1 or max([len(x),len(y)])")

        point_list = []
        for set in range(set_count):
            for zn in z[set]:
                for yn in y[set]:
                    for xn in x[set]:
                        point = [xn,yn,zn]
                        point_list.append(copy.deepcopy(point))
        return point_list

class LinearArray(_PatternObject):
    def __init__(self,obj,x=[0],y=[0],z=[0]):
        super(LinearArray, self).__init__()
        self._set_array_values(x,y,z)
        self._set_dimensions(x,y,z)
        self._fill_array(obj,x,y,z)

    def _make_iterable(self,x,y,z):
        try:
            len(x)
        except:
            x = [x]
        try:
            len(y)
        except:
            y = [y]
        try:
            len(z)
        except:
            z = [z]
        return x,y,z

    def _set_array_values(self,x,y,z):
        x,y,z = self._make_iterable(x,y,z)
        self.array_values = {'x': copy.deepcopy(x),
                             'y': copy.deepcopy(y),
                             'z': copy.deepcopy(z)}

    def get_array_values(self):
        return copy.deepcopy(self.array_values)

    def _set_dimensions(self,x,y,z):
        x,y,z = self._make_iterable(x,y,z)
        self.dimensions = {'x': len(x),
                           'y': len(y),
                           'z': len(z)}

    def get_dimensions(self):
        return copy.deepcopy(self.dimensions)

    def _fill_array(self,obj,x,y,z):
        x,y,z = self._make_iterable(x,y,z)
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

    def get_point_list(self):
        array_values = self.get_array_values()
        x = array_values['x']
        y = array_values['y']
        z = array_values['z']
        point_list = []
        for zn in z:
            for yn in y:
                for xn in x:
                    point = [xn,yn,zn]
                    point_list.append(point)
        return point_list


if __name__ == "__main__":
    import finite_solid_objects as fso

    obj = fso.Cylinder()
    x = [-5,5]
    y = [-5,5]
    z = [0]
    pattern = LinearArray(obj,x,y,z)
    pattern.export()
