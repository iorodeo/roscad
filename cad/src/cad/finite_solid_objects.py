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

import csg_objects


class _FiniteSolidObject(csg_objects.CSGObject):
    def __init__(self):
        super(_FiniteSolidObject, self).__init__()
        self.dimensions = {}
        self.dimensions_default = {}

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
        return self.dimensions

class Box(_FiniteSolidObject):
    def __init__(self,*args,**kwargs):
        super(Box, self).__init__()
        self.dimensions_default = {'x': 1, 'y': 1, 'z': 1}
        self.set_dimensions_(args,kwargs)
        self.printable = True

class Sphere(_FiniteSolidObject):
    def __init__(self,*args,**kwargs):
        super(Sphere, self).__init__()
        self.dimensions_default = {'radius': 1}
        self.set_dimensions_(args,kwargs)
        self.printable = True

class Cylinder(_FiniteSolidObject):
    def __init__(self,*args,**kwargs):
        super(Cylinder, self).__init__()
        self.dimensions_default = {'z': 1, 'radius': 1}
        self.set_dimensions_(args,kwargs)
        self.printable = True


if __name__ == "__main__":
    fso = _FiniteSolidObject()
    print "fso.printable = " + str(fso.printable)
    box = Box([1,2,3])
    print "box.objlist = " + str(box.objlist)
    print "box.printable = " + str(box.printable)
    print "box.__class__ = " + str(box.__class__)
    print "box dimensions = " + str(box.get_dimensions())
    print "box pose = " + str(box.get_pose())
    print "box.color = " + str(box.color)
    sphere = Sphere()
    print "sphere.objlist = " + str(sphere.objlist)
    print "sphere.printable = " + str(sphere.printable)
    print "sphere.__class__ = " + str(sphere.__class__)
    print "sphere dimensions = " + str(sphere.get_dimensions())
    print "sphere pose = " + str(sphere.get_pose())
    print "sphere.color = " + str(sphere.color)
    diff = box - sphere
    print "diff.objlist = " + str(diff.objlist)
    print "diff.printable = " + str(diff.printable)
    print "diff.__class__ = " + str(diff.__class__)
    print "diff pose = " + str(diff.get_pose())
    print "diff objlist[0] pose = " + str(diff.objlist[0].get_pose())
    print "diff objlist[1] pose = " + str(diff.objlist[1].get_pose())
    print "diff objlist[0] dimensions = " + str(diff.objlist[0].get_dimensions())
    print "diff objlist[1] dimensions = " + str(diff.objlist[1].get_dimensions())
    print "diff objlist[0] color = " + str(diff.objlist[0].color)
    print "diff objlist[1] color = " + str(diff.objlist[1].color)
    print "diff.color = " + str(diff.color)
    box.set_dimensions(5)
    box.color.extend([1,0,0,4])
    sphere.translate([0.5,0,0])
    uni = box | sphere
    print "uni.objlist = " + str(uni.objlist)
    print "uni.printable = " + str(uni.printable)
    print "uni.__class__ = " + str(uni.__class__)
    print "uni pose = " + str(uni.get_pose())
    print "uni objlist[0] pose = " + str(uni.objlist[0].get_pose())
    print "uni objlist[1] pose = " + str(uni.objlist[1].get_pose())
    print "uni objlist[0] dimensions = " + str(uni.objlist[0].get_dimensions())
    print "uni objlist[1] dimensions = " + str(uni.objlist[1].get_dimensions())
    print "uni objlist[0] color = " + str(uni.objlist[0].color)
    print "uni objlist[1] color = " + str(uni.objlist[1].color)
    print "uni.color = " + str(uni.color)

    print "box.objlist = " + str(box.objlist)
    print "box.printable = " + str(box.printable)
    print "box.__class__ = " + str(box.__class__)
    print "box dimensions = " + str(box.get_dimensions())
    print "box pose = " + str(box.get_pose())
    print "box.color = " + str(box.color)
    print "sphere.objlist = " + str(sphere.objlist)
    print "sphere.printable = " + str(sphere.printable)
    print "sphere.__class__ = " + str(sphere.__class__)
    print "sphere dimensions = " + str(sphere.get_dimensions())
    print "sphere pose = " + str(sphere.get_pose())
    print "sphere.color = " + str(sphere.color)
    print "diff.objlist = " + str(diff.objlist)
    print "diff.printable = " + str(diff.printable)
    print "diff.__class__ = " + str(diff.__class__)
    print "diff pose = " + str(diff.get_pose())
    print "diff objlist[0] pose = " + str(diff.objlist[0].get_pose())
    print "diff objlist[1] pose = " + str(diff.objlist[1].get_pose())
    print "diff objlist[0] dimensions = " + str(diff.objlist[0].get_dimensions())
    print "diff objlist[1] dimensions = " + str(diff.objlist[1].get_dimensions())
    print "diff objlist[0] color = " + str(diff.objlist[0].color)
    print "diff objlist[1] color = " + str(diff.objlist[1].color)
    print "diff.color = " + str(diff.color)

    sphere2 = sphere.copy()
    # sphere2.set_pose()
    # sphere2.translate([-5,13,1])
    sphere2.set_position([-5,13,1])
    uni2 = uni | sphere2
    print "uni2.objlist = " + str(uni2.objlist)
    print "uni2.printable = " + str(uni2.printable)
    print "uni2.__class__ = " + str(uni2.__class__)
    print "uni2 pose = " + str(uni2.get_pose())
    print "uni2 objlist[0] pose = " + str(uni2.objlist[0].get_pose())
    print "uni2 objlist[1] pose = " + str(uni2.objlist[1].get_pose())
    print "uni2 objlist[1] dimensions = " + str(uni2.objlist[1].get_dimensions())
    print "uni2 objlist[0] color = " + str(uni2.objlist[0].color)
    print "uni2 objlist[1] color = " + str(uni2.objlist[1].color)
    print "uni2.color = " + str(uni2.color)

    box = Box(4)
    print "box dimensions = " + str(box.get_dimensions())
    box = Box(4,2,3)
    print "box dimensions = " + str(box.get_dimensions())
    box = Box(x=14,y=12,z=13)
    print "box dimensions = " + str(box.get_dimensions())
    box = Box([100])
    print "box dimensions = " + str(box.get_dimensions())
    box = Box([100,200,300])
    print "box dimensions = " + str(box.get_dimensions())
    box = Box({'x': 42, 'y': 52, 'z': 73})
    print "box dimensions = " + str(box.get_dimensions())

    cylinder = Cylinder(1234)
    print "cylinder dimensions = " + str(cylinder.get_dimensions())
    cylinder = Cylinder([1000])
    print "cylinder dimensions = " + str(cylinder.get_dimensions())
    cylinder = Cylinder([100,200])
    print "cylinder dimensions = " + str(cylinder.get_dimensions())
    cylinder = Cylinder(z=22,radius=5000)
    print "cylinder dimensions = " + str(cylinder.get_dimensions())
    cylinder = Cylinder({'z': 42, 'radius': 52})
    print "cylinder dimensions = " + str(cylinder.get_dimensions())

