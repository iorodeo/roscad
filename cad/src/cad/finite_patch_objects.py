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
import shapely.geometry
import shapely.ops
from shapely.geometry.polygon import LinearRing

import geometric_objects
# import cad.cad_import.dxf as dxf


class Polygon(geometric_objects.GeometricObject):
    def __init__(self,*args,**kwargs):
        super(Polygon, self).__init__()
        self.dimensions_default = {'polygons': [],'decimals': 5}
        self.set_dimensions_(args,kwargs)
        self.set_exportable(True)
        self.set_primative('polygon')
        # self.bounding_box = Box()

    def get_points(self):
        polygons = self.get_dimension('polygons')
        points = []
        for polygon in polygons:
            coords = polygon.exterior.coords
            coord_list = [list(coord) for coord in coords]
            points.extend(coord_list)
        return points

    def get_paths(self):
        polygons = self.get_dimension('polygons')
        paths = []
        point_index = 0
        for polygon in polygons:
            coords = polygon.exterior.coords
            coord_list = [list(coord) for coord in coords]
            path = range(len(coord_list))
            path = [point + point_index for point in path]
            paths.append(path)
            point_index = path[-1] + 1
        return paths

    def get_decimals(self):
        decimals = self.get_dimension('decimals')
        return decimals

    def set_dimensions_(self,args,kwargs):
        # if kwargs.has_key('polygons') and ((not kwargs.has_key('points')) or (not kwargs.has_key('paths'))):
        #     polygons = kwargs['polygons']
        #     points,paths = self.get_points_paths_from_polygons(polygons)
        #     kwargs['points'] = points
        #     kwargs['paths'] = paths
        super(Polygon, self).set_dimensions_(args,kwargs)

    # def update_bounding_box(self):
    #     dimensions = self.get_dimensions()
    #     super(Polygon, self).update_bounding_box(x=1,y=1,z=0.1)


if __name__ == "__main__":
    pass
