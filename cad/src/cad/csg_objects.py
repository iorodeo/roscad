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
import ros_object


class CSGObject(ros_object.ROSObject):
    def __init__(self):
        super(CSGObject, self).__init__()

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
        self.set_exportable(True)

class _Intersection(CSGObject):
    def __init__(self,obj):
        super(_Intersection, self).__init__()
        self.add_obj(obj)
        self.set_exportable(True)

class _Difference(CSGObject):
    def __init__(self,obj):
        super(_Difference, self).__init__()
        self.add_obj(obj)
        self.set_exportable(True)

class _Merge(CSGObject):
    def __init__(self,obj):
        super(_Merge, self).__init__()
        self.add_obj(obj)
        self.set_exportable(True)


if __name__ == "__main__":
    a = CSGObject()
    print a
    b = CSGObject()
    print b
    c = _Union([a,b])
    print c
    d = a | b
    print d
