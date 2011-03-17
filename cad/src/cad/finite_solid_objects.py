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
roslib.load_manifest('cad')
import rospy
import geometry_msgs

import cad_objects


class FiniteSolidObject(cad_objects.CADObject):
    def __init__(self):
        pass

class Box(FiniteSolidObject):
    def __init__(self,size=1):
        self.size = geometry_msgs.msg.Vector3()
        self.set_size(size)

    def set_size(self,size=1):
        if type(size) == type(geometry_msgs.msg.Vector3()):
            self.size = size
        elif ((type(size) == list) or (type(size) == tuple)):
            self.size.x = size[0]
            self.size.y = size[1]
            self.size.z = size[2]
        else:
            self.size.x = size
            self.size.y = size
            self.size.z = size

    def get_size(self):
        return self.size

class Sphere(FiniteSolidObject):
    def __init__(self,radius=1):
        self.set_radius(radius)

    def set_radius(self,radius=1):
        self.radius = radius

    def get_size(self):
        return self.radius
