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
        self.update_bounding_box()

    def set_dimensions_(self,args,kwargs):
        self.dimensions = self.fill_variable_with_args(args,kwargs,self.dimensions_default)

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
        self.set_primative('box')

    def update_bounding_box(self):
        dimensions = self.get_dimensions()
        super(Box, self).update_bounding_box(dimensions)

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
        self.dimensions_default = {'r': 0.5}
        self.set_dimensions_(args,kwargs)
        self.set_exportable(True)
        self.set_primative('sphere')

    def update_bounding_box(self):
        dimensions = self.get_dimensions()
        diameter = dimensions['r']*2
        super(Sphere, self).update_bounding_box(x=diameter,y=diameter,z=diameter)

    def get_export_obj_str(self):
        dimensions = self.get_dimensions()
        export_obj_str = super(Sphere,self).get_export_obj_str()
        export_obj_str = export_obj_str.format(r = dimensions['r'])
        return export_obj_str

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

    def get_export_obj_str(self):
        dimensions = self.get_dimensions()
        export_obj_str = super(Cylinder,self).get_export_obj_str()
        export_obj_str = export_obj_str.format(l = dimensions['l'],
                                               r = dimensions['r'])
        return export_obj_str

class Cone(_FiniteSolidObject):
    def __init__(self,*args,**kwargs):
        super(Cone, self).__init__()
        self.dimensions_default = {'l': 1, 'r_pos': 0.1, 'r_neg': 0.5}
        self.set_dimensions_(args,kwargs)
        self.set_exportable(True)
        self.set_primative('cone')

    def update_bounding_box(self):
        dimensions = self.get_dimensions()
        r_max = max(dimensions['r_pos'],dimensions['r_neg'])
        diameter = r_max*2
        super(Cone, self).update_bounding_box(x=diameter,y=diameter,z=dimensions['l'])

    def get_export_obj_str(self):
        dimensions = self.get_dimensions()
        export_obj_str = super(Cone,self).get_export_obj_str()
        export_obj_str = export_obj_str.format(l = dimensions['l'],
                                               r_pos = dimensions['r_pos'],
                                               r_neg = dimensions['r_neg'])
        return export_obj_str

class Extrusion(_FiniteSolidObject):
    def __init__(self,*args,**kwargs):
        super(Extrusion, self).__init__()
        self.dimensions_default = {'l': 1, 'profile': '', 'x': 1, 'y': 1}
        self.set_dimensions_(args,kwargs)
        self.set_exportable(True)
        self.set_primative('extrusion')
        self.bounding_box = Box()

    def update_bounding_box(self):
        dimensions = self.get_dimensions()
        super(Extrusion, self).update_bounding_box(x=dimensions['x'],y=dimensions['y'],z=dimensions['l'])

    def get_export_obj_str(self):
        dimensions = self.get_dimensions()
        export_obj_str = super(Extrusion,self).get_export_obj_str()
        export_obj_str = export_obj_str.format(l = dimensions['l'],
                                               profile = dimensions['profile'])
        return export_obj_str

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

    beam = Extrusion(profile='import/1010.dxf',l=20)
    uni = uni | beam
    uni.export()
