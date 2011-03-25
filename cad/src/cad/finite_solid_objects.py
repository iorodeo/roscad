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
        self.set_color()

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
        obj_str = obj_str.format(indent = self.get_export_parameter('indent_str')*depth,
                                 dimensions = str(self.get_dimensions()))
        obj_str = obj_str_header + obj_str
        return obj_str

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
        self.dimensions_default = {'r': 1}
        self.set_dimensions_(args,kwargs)
        self.set_exportable(True)

    def get_export_obj_str(self):
        dimensions = self.get_dimensions()
        export_obj_str = super(Sphere,self).get_export_obj_str()
        export_obj_str = export_obj_str.format(r = dimensions['r'])
        return export_obj_str

class Cylinder(_FiniteSolidObject):
    def __init__(self,*args,**kwargs):
        super(Cylinder, self).__init__()
        self.dimensions_default = {'l': 1, 'r': 1}
        self.set_dimensions_(args,kwargs)
        self.set_exportable(True)

    def get_export_obj_str(self):
        dimensions = self.get_dimensions()
        export_obj_str = super(Cylinder,self).get_export_obj_str()
        export_obj_str = export_obj_str.format(l = dimensions['l'],
                                               r = dimensions['r'])
        return export_obj_str

class Cone(_FiniteSolidObject):
    def __init__(self,*args,**kwargs):
        super(Cone, self).__init__()
        self.dimensions_default = {'l': 1, 'r_pos': 1, 'r_neg': 0.1}
        self.set_dimensions_(args,kwargs)
        self.set_exportable(True)

    def get_export_obj_str(self):
        dimensions = self.get_dimensions()
        export_obj_str = super(Cone,self).get_export_obj_str()
        export_obj_str = export_obj_str.format(l = dimensions['l'],
                                               r_pos = dimensions['r_pos'],
                                               r_neg = dimensions['r_neg'])
        return export_obj_str

if __name__ == "__main__":
    import math
    pi = math.pi

    sphere1 = Sphere(2)
    sphere2 = sphere1.copy()
    sphere1.translate([0,0,5])
    sphere2.translate([0,0,-5])
    cylinder = Cylinder(z=10,radius=1)
    dumbbell = (sphere1 | sphere2) | cylinder
    dumbbell.rotate(pi/4,[1,0,0])
    dumbbell.set_color([1,1,0],recursive=True)
    # print dumbbell
    # dumbbell.export()
    box1 = Box(10,10,3)
    box1.translate([30,0,0])
    box1.rotate(1,[0,0,1])
    box1.rotate(0.25,[1,0,0])
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
    arrow_x.set_color([1,0,0],recursive=True)
    arrow_y.rotate(-pi/2,[1,0,0])
    arrow_y.set_color([0,1,0],recursive=True)
    arrow_z.set_color([0,0,1],recursive=True)
    uni = uni | arrow_x | arrow_y | arrow_z
    uni.export()
