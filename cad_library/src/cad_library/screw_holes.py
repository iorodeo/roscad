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

import os
import sys
import math
import copy
import numpy

import cad.csg_objects as csg
import cad.finite_solid_objects as fso
import cad.pattern_objects as po


SCREW_HOLE_PARAMETERS = {
    '10' : {'tap' : {'course' : {'threads_per_inch' : 24,
                                 '75%' : 0.1495,
                                 '50%' : 0.1610,
                                 },
                     'fine' : {'threads_per_inch': 32,
                               '75%' : 0.1590,
                               '50%' : 0.1695,
                               },
                     },
            'clearance' : {'close' : 0.1960,
                           'free' : 0.201,
                           },
            'counterbore' : {'diameter' : 0.375,
                             'depth' : 0.190,
                             },
            },
    '1/2' : {'tap' : {'course' : {'threads_per_inch' : 20,
                                 '75%' : 0.2010,
                                 '50%' : 0.2188,
                                 },
                     'fine' : {'threads_per_inch': 28,
                               '75%' : 0.2130,
                               '50%' : 0.2280,
                               },
                     },
            'clearance' : {'close' : 0.2570,
                           'free' : 0.2660,
                           },
            'counterbore' : {'diameter' : 0.4375,
                             'depth' : 0.250,
                             },
            }
    }

class Counterbore(csg.Union):
    def __init__(self,*args,**kwargs):
        super(Counterbore,self).__init__()
        self.parameters = SCREW_HOLE_PARAMETERS

        dimensions_default = {'size' : '10',
                              'depth' : 1,
                              'fit' : 'free'}
        self.dimensions = self.fill_variable_with_args(args,kwargs,dimensions_default)
        self.top_clearance = 0.1
        self.__make_hole()
        self.__make_counterbore()

    def __make_hole(self):
        size = self.dimensions['size']
        depth = self.dimensions['depth']
        fit = self.dimensions['fit']
        diameter = self.parameters[size]['clearance'][fit]
        l = depth
        r = diameter/2
        hole = fso.Cylinder(l=l,r=r)
        z_offset = -depth/2
        hole.translate([0,0,z_offset])
        self.add_obj(hole)

    def __make_counterbore(self):
        size = self.dimensions['size']
        diameter = self.parameters[size]['counterbore']['diameter']
        depth = self.parameters[size]['counterbore']['depth']
        l = depth + self.top_clearance
        r = diameter/2
        counterbore = fso.Cylinder(l=l,r=r)
        z_offset = -l/2 + self.top_clearance
        counterbore.translate([0,0,z_offset])
        self.add_obj(counterbore)

class ClearanceHole(fso.Cylinder):
    def __init__(self,*args,**kwargs):
        self.parameters = SCREW_HOLE_PARAMETERS
        dimensions_default = {'size' : '10',
                              'depth' : 1,
                              'fit' : 'free'}
        self.dimensions = self.fill_variable_with_args(args,kwargs,dimensions_default)
        self.top_clearance = 0.1

        size = self.dimensions['size']
        depth = self.dimensions['depth']
        fit = self.dimensions['fit']
        diameter = self.parameters[size]['clearance'][fit]
        l = depth + self.top_clearance
        r = diameter/2

        super(ClearanceHole,self).__init__(r=r,l=l)

        z_offset = -l/2 + self.top_clearance
        self.translate([0,0,z_offset])

class TapHole(fso.Cylinder):
    def __init__(self,*args,**kwargs):
        self.parameters = SCREW_HOLE_PARAMETERS
        dimensions_default = {'size' : '10',
                              'type' : 'course',
                              'percent' : '75%',
                              'depth' : 1}
        self.dimensions = self.fill_variable_with_args(args,kwargs,dimensions_default)
        self.top_clearance = 0.1

        size = self.dimensions['size']
        type = self.dimensions['type']
        percent = self.dimensions['percent']
        depth = self.dimensions['depth']
        diameter = self.parameters[size]['tap'][type][percent]
        l = depth + self.top_clearance
        r = diameter/2

        super(TapHole,self).__init__(r=r,l=l)

        z_offset = -l/2 + self.top_clearance
        self.translate([0,0,z_offset])


if __name__ == "__main__":
    pass
