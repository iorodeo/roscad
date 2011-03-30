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
import cad.finite_solid_objects as fso
import copy


# Data for profiles
PROFILE_TO_DXF = {
    '1010'            : 'profiles/1010.dxf',
    '1020'            : 'profiles/1020.dxf',
    '1030'            : 'profiles/1030.dxf',
    '2040'            : 'profiles/2040.dxf',
    '1545'            : 'profiles/1545.dxf',
    '3030'            : 'profiles/3030.dxf',
    '3060'            : 'profiles/3060.dxf',
    'pillowblock'     : 'profiles/pillowblock.dxf',
    'rectangulartube' : 'profiles/rectangulartube.dxf',
    }

DATA_1010 = {
    'dx' : 1.0,
    'dy' : 1.0,
    'slot_xpos' : (0.0,),
    'slot_ypos' : (0.0,),
    }

DATA_1020 = {
    'dx' : 1.0,
    'dy' : 2.0,
    'slot_xpos' : (0.0,),
    'slot_ypos' : (-0.5,0.5),
    }

DATA_1030 = {
    'dx' : 1.0,
    'dy' : 3.0,
    'slot_xpos' : (0.0,),
    'slot_ypos' : (-1.0, 0.0, 1.0),
    }

DATA_2040 = {
    'dx' : 2.0,
    'dy' : 4.0,
    'slot_xpos' : (-0.5, 0.5),
    'slot_ypos' : (-1.5, -0.5, 0.5, 1.5),
    }

DATA_1545 = {
    'dx' : 1.5,
    'dy' : 4.5,
    'slot_xpos' : (0,),
    'slot_ypos' : (-1.5, 0.0, 1.5),
    }

DATA_3030 = {
    'dx' : 3.0,
    'dy' : 3.0,
    'slot_xpos' : (-0.75, 0.75),
    'slot_ypos' : (-0.75, 0.75),
    }

DATA_3060 = {
    'dx' : 3.0,
    'dy' : 6.0,
    'slot_xpos' : (-0.75, 0.75),
    'slot_ypos' : (-2.25, -0.75, 0.75, 2.25),
    }

DATA_PILLOWBLOCK = {
    'dx' : 4.75,
    'dy' : 2.3,
    }

DATA_RECTANGULARTUBE = {
    'dx' : 2.0,
    'dy' : 5.0,
    }

PROFILE_DATA = {
    '1010'            : DATA_1010,
    '1020'            : DATA_1020,
    '1030'            : DATA_1030,
    '2040'            : DATA_2040,
    '1545'            : DATA_1545,
    '3030'            : DATA_3030,
    '3060'            : DATA_3060,
    'pillowblock'     : DATA_PILLOWBLOCK,
    'rectangulartube' : DATA_RECTANGULARTUBE,
    }

class Extrusion(fso.Extrusion):
    def __init__(self,profile='1010',l=24):
        if profile in PROFILE_TO_DXF:
            profile_dxf = PROFILE_TO_DXF[profile]
        else:
            profile_dxf = ''
        super(Extrusion, self).__init__(profile=profile_dxf,l=l)
        self.set_color([0.5,0.5,0.5])

    def get_profile_data(self,profile=''):
        if profile in profile_data:
            data = PROFILE_DATA[profile]
        else:
            data = ''
        return copy.deepcopy(data)

if __name__ == "__main__":
    beam = Extrusion(profile='1020',l=20)
    beam.export()






