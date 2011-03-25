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
import random


class _FiniteSolidObject(csg_objects.CSGObject):
    def __init__(self):
        super(_FiniteSolidObject, self).__init__()
        self.dimensions = {}
        self.dimensions_default = {}
        self.set_color([random.random(),random.random(),random.random(),1])

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

    def get_export_obj_str(self):
        dimensions = self.get_dimensions()
        export_obj_str = super(Box,self).get_export_obj_str()
        export_obj_str = export_obj_str.format(x = dimensions['x'],
                                               y = dimensions['y'],
                                               z = dimensions['z'])
        return export_obj_str

class Sphere(_FiniteSolidObject):
    def __init__(self,*args,**kwargs):
        super(Sphere, self).__init__()
        self.dimensions_default = {'radius': 1}
        self.set_dimensions_(args,kwargs)
        self.set_exportable(True)

    def get_export_obj_str(self):
        dimensions = self.get_dimensions()
        export_obj_str = super(Sphere,self).get_export_obj_str()
        export_obj_str = export_obj_str.format(radius = dimensions['radius'])
        return export_obj_str

class Cylinder(_FiniteSolidObject):
    def __init__(self,*args,**kwargs):
        super(Cylinder, self).__init__()
        self.dimensions_default = {'z': 1, 'radius': 1}
        self.set_dimensions_(args,kwargs)
        self.set_exportable(True)

    def get_export_obj_str(self):
        dimensions = self.get_dimensions()
        export_obj_str = super(Cylinder,self).get_export_obj_str()
        export_obj_str = export_obj_str.format(z = dimensions['z'],
                                               radius = dimensions['radius'])
        return export_obj_str

class Cone(_FiniteSolidObject):
    def __init__(self,*args,**kwargs):
        super(Cone, self).__init__()
        self.dimensions_default = {'z': 1, 'radius_pos': 1, 'radius_neg': 0.1}
        self.set_dimensions_(args,kwargs)
        self.set_exportable(True)

    def get_export_obj_str(self):
        dimensions = self.get_dimensions()
        export_obj_str = super(Cone,self).get_export_obj_str()
        export_obj_str = export_obj_str.format(z = dimensions['z'],
                                               radius_pos = dimensions['radius_pos'],
                                               radius_neg = dimensions['radius_neg'])
        return export_obj_str

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
    # box = Box([1,2,3])
    # box.rotate(1.2,[1,0,0])
    # print box
    # box.rotate(-0.3,[0,1,0])
    # print box
    # box2 = box.copy()
    # box2.translate([10,0,0])
    # box2.rotate(0.3,[0,1,0])
    # sphere = Sphere(2)
    # uni = box | (box2 & sphere)
    # uni.translate([0,-14,9])
    # print uni
    # uni.export()

    import math
    pi = math.pi

    sphere1 = Sphere(2)
    sphere2 = sphere1.copy()
    sphere1.translate([0,0,5])
    sphere2.translate([0,0,-5])
    cylinder = Cylinder(z=10,radius=1)
    dumbbell = (sphere1 | sphere2) | cylinder
    # print dumbbell
    # dumbbell.export()
    box1 = Box(10,10,3)
    box1.rotate(1,[0,0,1])
    box1.rotate(1,[1,0,0])
    uni = dumbbell | box1

    cylinder = Cylinder(z=20,radius=0.5)
    cone = Cone(z=4,radius_pos=0.1,radius_neg=1)
    cone.translate([0,0,10])
    arrow = cylinder | cone
    arrow.translate([0,0,10])

    arrow_x = arrow.copy()
    arrow_y = arrow.copy()
    arrow_z = arrow.copy()
    arrow_x.rotate(pi/2,[0,1,0])
    arrow_x.set_color([1,0,0])
    arrow_y.rotate(pi/2,[1,0,0])
    arrow_y.set_color([0,1,0])
    arrow_z.set_color([0,0,1])
    uni = uni | arrow_x | arrow_y | arrow_z
    uni.export()
