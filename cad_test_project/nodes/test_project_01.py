#!/usr/bin/env python
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
roslib.load_manifest('cad_test_project')
import rospy

import math

from cad.cad_objects import *
from cad.finite_solid_objects import *




if __name__ == "__main__":
    test_project_01 = CADProject()

    sphere1 = Sphere(radius=3)
    sphere1.translate([0,0,5])

    sphere2 = Sphere(radius=3)
    sphere2.translate([0,0,-5])

    cylinder1 = Cylinder(z=10,radius=0.5)

    dumbbell = sphere1 | sphere2 | cylinder1
    dumbbell.rotate(angle=(math.pi/4),axis=[0,1,0])
    dumbbell.translate([3,0,0])

    test_project_01.add(dumbbell)

    print test_project_01

