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
import ros_object

class BoundingBox(ros_object.ROSObject):
    def __init__(self):
        super(BoundingBox, self).__init__()
        self.dimensions_default = {'x': 1,
                                   'y': 1,
                                   'z': 1}
        self.dimensions = copy.deepcopy(self.dimensions_default)
        self.set_dimensions()

    def set_dimensions(self,*args,**kwargs):
        self.set_dimensions_(args,kwargs)

    def set_dimensions_(self,args,kwargs):
        self.dimensions = self.fill_variable_with_args(args,kwargs,self.get_dimensions())

    def get_dimensions(self):
        return copy.deepcopy(self.dimensions)

class CSGObject(ros_object.ROSObject):
    def __init__(self):
        super(CSGObject, self).__init__()
        self.bounding_box = BoundingBox()

    def update_bounding_box(self,*args,**kwargs):
        self.bounding_box.set_dimensions(args,kwargs)
        self.bounding_box.set_transformations(self.get_transformations)

    def get_bounding_box(self):
        return copy.deepcopy(self.bounding_box)

    def union(self,obj):
        union = Union(self)
        union.add_obj(obj)
        return union
        # return Union([self,obj])

    # |
    def __or__(self, obj):
        return self.union(obj)

    def intersection(self,obj):
        intersection = Intersection(self)
        intersection.add_obj(obj)
        return intersection
        # return Intersection([self,obj])

    # &
    def __and__(self, obj):
        return self.intersection(obj)

    def difference(self,obj):
        difference = Difference(self)
        difference.add_obj(obj)
        return difference
        # return Difference([self,obj])

    # -
    def __sub__(self, obj):
        return self.difference(obj)

    def merge(self,obj):
        merge = Merge(self)
        merge.add_obj(obj)
        return merge
        # return Merge([self,obj])

    # ^
    def __xor__(self, obj):
        return self.merge(obj)


class Union(CSGObject):
    def __init__(self,obj=[]):
        super(Union, self).__init__()
        self.add_obj(obj)
        self.set_exportable(True)
        self.set_primative('union')

class Intersection(CSGObject):
    def __init__(self,obj=[]):
        super(Intersection, self).__init__()
        self.add_obj(obj)
        self.set_exportable(True)
        self.set_primative('intersection')

class Difference(CSGObject):
    def __init__(self,obj=[]):
        super(Difference, self).__init__()
        self.add_obj(obj)
        self.set_exportable(True)
        self.set_primative('difference')

class Merge(CSGObject):
    def __init__(self,obj=[]):
        super(Merge, self).__init__()
        self.add_obj(obj)
        self.set_exportable(True)
        self.set_primative('merge')


if __name__ == "__main__":
    a = CSGObject()
    print a
    b = CSGObject()
    print b
    c = Union([a,b])
    print c
    d = a | b
    print d
