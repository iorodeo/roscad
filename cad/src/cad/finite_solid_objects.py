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

import geometric_objects
import finite_patch_objects



class _FiniteSolidObject(geometric_objects.FiniteGeometricObject):
    def __init__(self,*args,**kwargs):
        super(_FiniteSolidObject, self).__init__()

class Box(_FiniteSolidObject):
    def __init__(self,*args,**kwargs):
        super(Box, self).__init__()
        self.dimensions_default = {'x': 1, 'y': 1, 'z': 1}
        self.set_dimensions_(args,kwargs)
        self.set_exportable(True)
        self.set_primative('box')

    def update_bounding_box(self):
        dimensions = self.get_dimensions()
        super(Box, self).update_bounding_box(dimensions)

class Sphere(_FiniteSolidObject):
    def __init__(self,*args,**kwargs):
        super(Sphere, self).__init__()
        self.dimensions_default = {'r': 0.5}
        self.set_dimensions_(args,kwargs)
        self.set_exportable(True)
        self.set_primative('sphere')

    def update_bounding_box(self):
        dimensions = self.get_dimensions()
        diameter = dimensions['r']*2
        super(Sphere, self).update_bounding_box(x=diameter,y=diameter,z=diameter)

class Cylinder(_FiniteSolidObject):
    def __init__(self,*args,**kwargs):
        super(Cylinder, self).__init__()
        self.dimensions_default = {'l': 1, 'r': 0.5}
        self.set_dimensions_(args,kwargs)
        self.set_exportable(True)
        self.set_primative('cylinder')

    def update_bounding_box(self):
        dimensions = self.get_dimensions()
        diameter = dimensions['r']*2
        super(Cylinder, self).update_bounding_box(x=diameter,y=diameter,z=dimensions['l'])

class Cone(_FiniteSolidObject):
    def __init__(self,*args,**kwargs):
        super(Cone, self).__init__()
        self.dimensions_default = {'l': 1, 'r_pos': 0.1, 'r_neg': 0.5}
        self.set_dimensions(args,kwargs)
        self.set_exportable(True)
        self.set_primative('cone')

    def update_bounding_box(self):
        dimensions = self.get_dimensions()
        r_max = max(dimensions['r_pos'],dimensions['r_neg'])
        diameter = r_max*2
        super(Cone, self).update_bounding_box(x=diameter,y=diameter,z=dimensions['l'])

class Extrusion(_FiniteSolidObject):
    def __init__(self,*args,**kwargs):
        super(Extrusion, self).__init__()
        self.dimensions_default = {'l': 1}
        self.set_dimensions_(args,kwargs)
        self.set_exportable(True)
        self.set_primative('extrusion')
        self.bounding_box = Box()

    def get_profile(self):
        obj_list = self.get_obj_list()
        if len(obj_list) == 1:
            return obj_list[0]

    def set_dimensions_(self,args,kwargs):
        self.add_obj(finite_patch_objects.Polygon(*args,**kwargs))
        super(Extrusion, self).set_dimensions_(args,kwargs)

    def update_bounding_box(self):
        dimensions = self.get_dimensions()
        super(Extrusion, self).update_bounding_box(x=1,y=1,z=dimensions['l'])

class Rotation(_FiniteSolidObject):
    def __init__(self,*args,**kwargs):
        super(Rotation, self).__init__()
        self.dimensions_default = {}
        self.set_dimensions_(args,kwargs)
        self.set_exportable(True)
        self.set_primative('rotation')
        self.bounding_box = Box()

    def get_profile(self):
        obj_list = self.get_obj_list()
        if len(obj_list) == 1:
            return obj_list[0]

    def set_dimensions_(self,args,kwargs):
        self.add_obj(finite_patch_objects.Polygon(*args,**kwargs))
        super(Rotation, self).set_dimensions_(args,kwargs)

    def update_bounding_box(self):
        dimensions = self.get_dimensions()
        super(Rotation, self).update_bounding_box(x=1,y=1,z=1)


if __name__ == "__main__":
    import math
    pi = math.pi

    sphere1 = Sphere(2)
    sphere2 = sphere1.copy()
    sphere1.translate([0,0,5])
    sphere2.translate([0,0,-5])
    cylinder = Cylinder(l=10,r=1)
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

    cylinder = Cylinder(l=20,r=0.5)
    cone = Cone(l=4,r_pos=0.1,r_neg=1)
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
