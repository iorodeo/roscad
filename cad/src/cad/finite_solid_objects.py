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


class _FiniteSolidObject(csg_objects.CSGObject):
    def __init__(self):
        super(_FiniteSolidObject, self).__init__()
        self.dimensions = {}
        self.dimensions_default = {}

    def set_dimensions(self,*args,**kwargs):
        self.set_dimensions_(args,kwargs)

    def set_dimensions_(self,args,kwargs):
        # print args
        # print "len(args) = " + str(len(args))
        # print kwargs
        self.dimensions = self.dimensions_default
        if 0 < len(kwargs.keys()):
            if set(kwargs.keys()) == set(self.dimensions_default.keys()):
                self.dimensions = kwargs
        elif len(args) == 1:
            if (type(args[0]) == list) or (type(args[0]) == tuple):
                if len(args[0]) == 1:
                    for k, v in self.dimensions_default.iteritems():
                        self.dimensions[k] = args[0][0]
                elif len(args[0]) == len(self.dimensions_default.keys()):
                    arg_list = list(args[0])
                    for k, v in self.dimensions_default.iteritems():
                        self.dimensions[k] = arg_list.pop(0)
            elif (type(args[0]) == dict):
                if (set(args[0].keys()) == set(self.dimensions_default.keys())):
                    self.dimensions = args[0]
            else:
                for k, v in self.dimensions_default.iteritems():
                    self.dimensions[k] = args[0]
        elif len(args) == len(self.dimensions_default.keys()):
            args = list(args)
            for k, v in self.dimensions_default.iteritems():
                self.dimensions[k] = args.pop(0)

    def get_dimensions(self):
        return copy.deepcopy(self.dimensions)

    def get_obj_str(self,depth=0):
        obj_str_header = super(_FiniteSolidObject, self).get_obj_str(depth)
        obj_str = '{indent}dimensions = \n{indent}{dimensions:s}\n'
        obj_str = obj_str.format(indent = self.indent_str*depth,
                                 dimensions = str(self.get_dimensions()))
        obj_str = obj_str_header + obj_str
        return obj_str

    # def __str__(self):
    #     rtn_str_header = super(_FiniteSolidObject, self).__str__()
    #     rtn_str = 'dimensions = \n{dimensions:s}\n'
    #     rtn_str = rtn_str.format(dimensions = str(self.get_dimensions()))
    #     rtn_str = rtn_str_header + rtn_str
    #     return rtn_str

class Box(_FiniteSolidObject):
    def __init__(self,*args,**kwargs):
        super(Box, self).__init__()
        self.dimensions_default = {'x': 1, 'y': 1, 'z': 1}
        self.set_dimensions_(args,kwargs)
        self.set_exportable(True)

class Sphere(_FiniteSolidObject):
    def __init__(self,*args,**kwargs):
        super(Sphere, self).__init__()
        self.dimensions_default = {'radius': 1}
        self.set_dimensions_(args,kwargs)
        self.set_exportable(True)

class Cylinder(_FiniteSolidObject):
    def __init__(self,*args,**kwargs):
        super(Cylinder, self).__init__()
        self.dimensions_default = {'z': 1, 'radius': 1}
        self.set_dimensions_(args,kwargs)
        self.set_exportable(True)


if __name__ == "__main__":
    # box = Box([1,2,3])
    # print box
    # sphere = Sphere()
    # print sphere
    # diff = box - sphere
    # print diff
    # box.set_dimensions(5)
    # sphere.translate([0.5,0,0])
    # uni = box | sphere
    # print uni
    # print box
    # print sphere
    # print diff

    # sphere2 = sphere.copy()
    # sphere2.translate([-5,13,1])
    # uni2 = uni | sphere2
    # print uni2
    # box = Box(4)
    # print box
    # box = Box(4,2,3)
    # print box
    # box = Box(x=14,y=12,z=13)
    # print box
    # box = Box([100])
    # print box
    # box = Box([100,200,300])
    # print box
    # box = Box({'x': 42, 'y': 52, 'z': 73})
    # print box

    # cylinder = Cylinder(1234)
    # print cylinder
    # cylinder = Cylinder([1000])
    # print cylinder
    # cylinder = Cylinder([100,200])
    # print cylinder
    # cylinder = Cylinder(z=22,radius=5000)
    # print cylinder
    # cylinder = Cylinder({'z': 42, 'radius': 52})
    # print cylinder
    box = Box([1,2,3])
    box.rotate(1.2,[1,0,0])
    print box
    box.rotate(-0.3,[0,1,0])
    print box
    box2 = box.copy()
    box2.translate([10,0,0])
    box2.rotate(0.3,[0,1,0])
    sphere = Sphere(18)
    uni = box | (box2 & sphere)
    uni.translate([0,-14,9])
    print uni
