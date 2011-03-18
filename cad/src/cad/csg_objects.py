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
# from __future__ import division
# import roslib
# roslib.load_manifest('cad')
# import rospy

import cad_objects


class CSGObject(cad_objects.CADObject):
    def __init__(self):
        super(CSGObject, self).__init__()
        self.objlist = []

    def add_obj(self, obj):
        if type(obj) == list:
            self.objlist.extend(obj)
        else:
            self.objlist.append(obj)

    def union(self,obj):
        return _Union([self,obj])

    # |
    def __or__(self, obj):
        return self.union(obj)

    def intersection(self,obj):
        return _Intersection([self,obj])

    # &
    def __and__(self, obj):
        return self.intersection(obj)

    def difference(self,obj):
        return _Difference([self,obj])

    # -
    def __sub__(self, obj):
        return self.difference(obj)

    def merge(self,obj):
        return _Merge([self,obj])

    # ^
    def __xor__(self, obj):
        return self.merge(obj)


class _Union(CSGObject):
    def __init__(self,obj):
        super(_Union, self).__init__()
        self.add_obj(obj)
        self.printable = True

class _Intersection(CSGObject):
    def __init__(self,obj):
        super(_Intersection, self).__init__()
        self.add_obj(obj)
        self.printable = True

class _Difference(CSGObject):
    def __init__(self,obj):
        super(_Difference, self).__init__()
        self.add_obj(obj)
        self.printable = True

class _Merge(CSGObject):
    def __init__(self,obj):
        super(_Merge, self).__init__()
        self.add_obj(obj)
        self.printable = True


if __name__ == "__main__":
    a = CSGObject()
    print "a.objlist = " + str(a.objlist)
    print "a.printable = " + str(a.printable)
    print "a.__class__ = " + str(a.__class__)
    b = CSGObject()
    print "b.objlist = " + str(b.objlist)
    print "b.printable = " + str(b.printable)
    print "b.__class__ = " + str(b.__class__)
    c = _Union([a,b])
    print "c.objlist = " + str(c.objlist)
    print "c.printable = " + str(c.printable)
    print "c.__class__ = " + str(c.__class__)
    d = a | b
    print "d.objlist = " + str(d.objlist)
    print "d.printable = " + str(d.printable)
    print "d.__class__ = " + str(d.__class__)

