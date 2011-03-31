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
import math
import copy


DATA_PILLOWBLOCK = {
    'x': 4.75,
    'y': 3.5,
    'z': 3.75,
    'profile': 'pillowblock/pillowblock.dxf',
    'color': [1.0,1.0,0.0,1.0],
    'hole_x': (-2.0625,2.0625),
    'hole_z': (-1.25,1.25),
    'hole_r': 0.141,
    'hole_l': 4,
    }

class PillowBlock(csg.Difference):
    def __init__(self):
        super(PillowBlock, self).__init__()
        self.__make_pillowblock()
        # self.__make_holes()
        self.rotate(angle=math.pi/2,axis=[1,0,0])
        self.rotate(angle=math.pi/2,axis=[0,0,1])
        self.set_color([1,1,0],recursive=True)

    def __make_pillowblock(self):
        profile = DATA_PILLOWBLOCK['profile']
        l = DATA_PILLOWBLOCK['z']
        pillowblock = fso.Extrusion(profile=profile,l=l)
        self.add_obj(pillowblock)

    def __make_holes(self):
        hole_r = DATA_PILLOWBLOCK['hole_r']
        hole_l = DATA_PILLOWBLOCK['hole_l']
        hole_x = DATA_PILLOWBLOCK['hole_x']
        hole_z = DATA_PILLOWBLOCK['hole_z']
        hole_list = []
        base_hole = fso.Cylinder(r=hole_r,l=hole_l)
        base_x_hole = base_hole.copy()
        base_x_hole.rotate(angle=-math.pi/2,axis=[1,0,0])
        for z in hole_z:
            for x in hole_x:
                hole = base_x_hole.copy()
                hole.translate([x,0,z])
                hole_list.append(hole)
        self.add_obj(hole_list)


if __name__ == "__main__":
    import arrow
    origin = arrow.Origin()
    pillowblock = PillowBlock()
    pillowblock = pillowblock | origin
    pillowblock.export()





