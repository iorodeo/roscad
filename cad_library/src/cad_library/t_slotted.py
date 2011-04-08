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
import roslib
roslib.load_manifest('cad_library')
import rospy
import cad.csg_objects as csg
import cad.finite_solid_objects as fso
import cad.pattern_objects as po
import cad.export.bom as bom

import math
import copy
import numpy


# Data for profiles
EXTRUSION_DXF = {
    '1010'            : 't_slotted/extrusion/1010.dxf',
    '1020'            : 't_slotted/extrusion/1020.dxf',
    '1030'            : 't_slotted/extrusion/1030.dxf',
    '2040'            : 't_slotted/extrusion/2040.dxf',
    '1545'            : 't_slotted/extrusion/1545.dxf',
    '3030'            : 't_slotted/extrusion/3030.dxf',
    '3060'            : 't_slotted/extrusion/3060.dxf',
    }

LBRACKET_DXF = {
    '1010'            : 't_slotted/lbracket/1010.dxf',
    # '1020'            : 't_slotted/lbracket/1020.dxf',
    # '1030'            : 't_slotted/lbracket/1030.dxf',
    '2020'            : 't_slotted/lbracket/2020.dxf',
    # '2040'            : 't_slotted/lbracket/2040.dxf',
    # '1545'            : 't_slotted/lbracket/1545.dxf',
    # '3030'            : 't_slotted/lbracket/3030.dxf',
    # '3060'            : 't_slotted/lbracket/3060.dxf',
    }

DATA_1010 = {
    'x' : 1.0,
    'y' : 1.0,
    'slot_x' : (0.0,),
    'slot_y' : (0.0,),
    'lbracket': {'single': {'l': 0.875,
                            'hole_r': 0.1285,
                            'hole_l': 0.5,
                            'hole_x': (0.5,),
                            'hole_y': (0.5,),
                            'hole_z': (0.0,)},
                 'double': {'l': 1.875,
                            'hole_r': 0.1285,
                            'hole_l': 0.5,
                            'hole_x': (0.5,),
                            'hole_y': (0.5,),
                            'hole_z': (-0.5,0.5)}
                     },
    }

DATA_1020 = {
    'x' : 1.0,
    'y' : 2.0,
    'slot_x' : (0.0,),
    'slot_y' : (-0.5,0.5),
    }

DATA_1030 = {
    'x' : 1.0,
    'y' : 3.0,
    'slot_x' : (0.0,),
    'slot_y' : (-1.0, 0.0, 1.0),
    }

DATA_2020 = {
    'x' : 2.0,
    'y' : 2.0,
    'slot_x' : (-0.5,0.5),
    'slot_y' : (-0.5,0.5),
    'lbracket': {'single': {'l': 0.875,
                            'hole_r': 0.1285,
                            'hole_l': 0.5,
                            'hole_x': (0.5,1.5),
                            'hole_y': (0.5,1.5),
                            'hole_z': (0.0,)},
                 'double': {'l': 1.875,
                            'hole_r': 0.1285,
                            'hole_l': 0.5,
                            'hole_x': (0.5,1.5),
                            'hole_y': (0.5,1.5),
                            'hole_z': (0.5,-0.5)}
                     },
    }

DATA_2040 = {
    'x' : 2.0,
    'y' : 4.0,
    'slot_x' : (-0.5, 0.5),
    'slot_y' : (-1.5, -0.5, 0.5, 1.5),
    }

DATA_1545 = {
    'x' : 1.5,
    'y' : 4.5,
    'slot_x' : (0,),
    'slot_y' : (-1.5, 0.0, 1.5),
    }

DATA_3030 = {
    'dx' : 3.0,
    'dy' : 3.0,
    'slot_x' : (-0.75, 0.75),
    'slot_y' : (-0.75, 0.75),
    }

DATA_3060 = {
    'x' : 3.0,
    'y' : 6.0,
    'slot_x' : (-0.75, 0.75),
    'slot_y' : (-2.25, -0.75, 0.75, 2.25),
    }

PROFILE_DATA = {
    '1010'            : DATA_1010,
    '1020'            : DATA_1020,
    '1030'            : DATA_1030,
    '2020'            : DATA_2020,
    '2040'            : DATA_2040,
    '1545'            : DATA_1545,
    '3030'            : DATA_3030,
    '3060'            : DATA_3060,
    }

PROFILE_DIMENSION_MAP = {
    '1.0': {'1.0': '1010',
            '2.0': '1020',
            '3.0': '1030',
            },
    '2.0': {'2.0': '2020',
            '4.0': '2040',
            },
    '1.5': {'4.5': '1545',
            },
    '3.0': {'3.0': '3030',
            '6.0': '3060',
            },
    }

X_AXIS = [1,0,0]
Y_AXIS = [0,1,0]
Z_AXIS = [0,0,1]

class Extrusion(fso.Extrusion):
    def __init__(self,*args,**kwargs):
        dimensions_default = {'x': 1,
                              'y': 1,
                              'z': 12}
        dimensions = self.fill_variable_with_args(args,kwargs,dimensions_default)
        dimension_list = [dimensions['x'],dimensions['y'],dimensions['z']]
        dimension_list.sort()
        dimension_0 = "{dimension:0.1f}".format(dimension=dimension_list[0])
        dimension_1 = "{dimension:0.1f}".format(dimension=dimension_list[1])
        profile = PROFILE_DIMENSION_MAP[dimension_0][dimension_1]
        # print profile
        l = dimension_list[2]

        self.profile_name = profile
        if profile in EXTRUSION_DXF:
            profile_dxf = EXTRUSION_DXF[profile]
        else:
            profile_dxf = ''

        super(Extrusion, self).__init__(profile=profile_dxf,l=l)

        if dimensions['x'] == dimension_list[0]:
            if dimensions['z'] < dimensions['y']:
                self.rotate(angle=-math.pi/2,axis=[1,0,0])
        elif dimensions['x'] == dimension_list[1]:
            if dimensions['z'] < dimensions['y']:
                self.rotate(angle=math.pi/2,axis=[0,0,1])
                self.rotate(angle=-math.pi/2,axis=[1,0,0])
            else:
                self.rotate(angle=math.pi/2,axis=[0,0,1])
        else:
            if dimensions['z'] < dimensions['y']:
                self.rotate(angle=math.pi/2,axis=[0,1,0])
            else:
                self.rotate(angle=math.pi/2,axis=[0,0,1])
                self.rotate(angle=math.pi/2,axis=[0,1,0])

        # self.update_bounding_box(dimensions)
        self.__set_bom()
        self.set_color([0.5,0.5,0.5])

    def __set_bom(self):
        scale = self.get_scale()
        BOM = bom.BOMObject()
        BOM.set_parameter('name',(self.profile_name + '_extrusion'))
        BOM.set_parameter('description','t_slotted extrusion')
        BOM.set_parameter('dimensions','x: {x:0.3f}, y: {y:0.3f}, z: {z:0.3f}'.format(x=self.parameters['x']*scale[0],y=self.parameters['y']*scale[1],z=self.parameters['z']*scale[2]))
        BOM.set_parameter('vender','?')
        BOM.set_parameter('part number','?')
        self.set_object_parameter('bom',BOM)

    def get_profile_data(self,profile=''):
        if profile in PROFILE_DATA:
            data = PROFILE_DATA[profile]
        else:
            data = ''
        return copy.deepcopy(data)

class LBracket(csg.Difference):
    def __init__(self,x=1,y=1,z=1,extrusion_axis=[0,0,1]):
        super(LBracket, self).__init__()

        if numpy.allclose(extrusion_axis,Z_AXIS):
            dimension_0 = min(abs(x),abs(y))
            dimension_1 = max(abs(x),abs(y))
            l = abs(z)
        elif numpy.allclose(extrusion_axis,Y_AXIS):
            dimension_0 = min(abs(x),abs(z))
            dimension_1 = max(abs(x),abs(z))
            l = abs(y)
        elif numpy.allclose(extrusion_axis,X_AXIS):
            dimension_0 = min(abs(y),abs(z))
            dimension_1 = max(abs(y),abs(z))
            l = abs(x)

        dimension_0 = "{dimension:0.1f}".format(dimension=dimension_0)
        dimension_1 = "{dimension:0.1f}".format(dimension=dimension_1)
        profile = PROFILE_DIMENSION_MAP[dimension_0][dimension_1]
        self.profile_data = self.get_profile_data(profile)

        self.profile_name = profile
        if profile in LBRACKET_DXF:
            self.profile_dxf = LBRACKET_DXF[profile]
        else:
            self.profile_dxf = ''

        if l == 2:
            self.bracket_type = 'double'
        else:
            self.bracket_type = 'single'

        self.__make_bracket()
        self.__make_holes()

        angle0 = math.atan2(1,1)
        if numpy.allclose(extrusion_axis,Z_AXIS):
            x = math.copysign(1,x)
            y = math.copysign(1,y)
            angle = math.atan2(y,x) - angle0
            self.rotate(angle=angle,axis=Z_AXIS)
        elif numpy.allclose(extrusion_axis,Y_AXIS):
            self.rotate(angle=math.pi/2,axis=X_AXIS)
            x = math.copysign(1,x)
            z = math.copysign(1,z)
            angle = math.atan2(x,z) - angle0
            self.rotate(angle=angle,axis=Y_AXIS)
        elif numpy.allclose(extrusion_axis,X_AXIS):
            self.rotate(angle=-math.pi/2,axis=Y_AXIS)
            y = math.copysign(1,y)
            z = math.copysign(1,z)
            angle = math.atan2(z,y) - angle0
            self.rotate(angle=angle,axis=X_AXIS)

        self.__set_bom()
        self.set_color([0.5,0.5,0.5],recursive=True)

    def __make_bracket(self):
        l = self.profile_data['lbracket'][self.bracket_type]['l']
        bracket = fso.Extrusion(profile=self.profile_dxf,l=l)
        self.add_obj(bracket)

    def __make_holes(self):
        hole_r = self.profile_data['lbracket'][self.bracket_type]['hole_r']
        hole_l = self.profile_data['lbracket'][self.bracket_type]['hole_l']
        hole_x = self.profile_data['lbracket'][self.bracket_type]['hole_x']
        hole_y = self.profile_data['lbracket'][self.bracket_type]['hole_y']
        hole_z = self.profile_data['lbracket'][self.bracket_type]['hole_z']
        # hole_list = []
        base_hole = fso.Cylinder(r=hole_r,l=hole_l)
        base_x_hole = base_hole.copy()
        base_x_hole.rotate(angle=math.pi/2,axis=[1,0,0])

        x_holes = po.LinearArray(base_x_hole,x=hole_x,y=[0],z=hole_z)
        self.add_obj(x_holes)
        # for z in hole_z:
        #     for x in hole_x:
        #         hole = base_x_hole.copy()
        #         hole.translate([x,0,z])
        #         hole_list.append(hole)

        base_y_hole = base_hole.copy()
        base_y_hole.rotate(angle=math.pi/2,axis=[0,1,0])
        y_holes = po.LinearArray(base_y_hole,x=[0],y=hole_y,z=hole_z)
        self.add_obj(y_holes)
        # for z in hole_z:
        #     for y in hole_y:
        #         hole = base_y_hole.copy()
        #         hole.translate([0,y,z])
        #         hole_list.append(hole)
        # self.add_obj(hole_list)

    def __set_bom(self):
        scale = self.get_scale()
        BOM = bom.BOMObject()
        BOM.set_parameter('name',(self.profile_name + '_lbracket'))
        BOM.set_parameter('description','t_slotted L bracket')
        BOM.set_parameter('dimensions','x: {x:0.3f}, y: {y:0.3f}, z: {z:0.3f}'.format(x=self.parameters['x']*scale[0],y=self.parameters['y']*scale[1],z=self.parameters['z']*scale[2]))
        BOM.set_parameter('vender','?')
        BOM.set_parameter('part number','?')
        self.set_object_parameter('bom',BOM)

    def get_profile_data(self,profile=''):
        if profile in PROFILE_DATA:
            data = PROFILE_DATA[profile]
        else:
            data = ''
        return copy.deepcopy(data)

if __name__ == "__main__":
    import origin
    o = origin.Origin()

    # beam = Extrusion(x=2,y=1,z=6)
    # beam = Extrusion(x=14,y=2,z=4)
    # beam = beam | o
    # beam.export()

    bracket = LBracket(x=-1,y=2,z=1,extrusion_axis=[0,1,0])
    bracket = bracket | o
    bracket.export()





