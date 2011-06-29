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
# import shapely.ops
# from shapely.geometry.polygon import LinearRing
import numpy
from matplotlib.collections import LineCollection
import pylab
import time

import geometric_objects
import cad.cad_import.dxf as dxf


class _FinitePatchObject(geometric_objects.FiniteGeometricObject):
    def __init__(self,*args,**kwargs):
        super(_FinitePatchObject, self).__init__()

class Polygon(_FinitePatchObject):
    def __init__(self,*args,**kwargs):
        super(Polygon, self).__init__()
        self.dimensions_default = {'polygon_list': [],'decimals': 5}
        self.set_dimensions_(args,kwargs)
        self.set_exportable(True)
        self.set_primative('polygon')
        # self.bounding_box = Box()

    def get_points(self):
        polygon_list = self.get_dimension('polygon_list')
        points = []
        for polygon in polygon_list:
            coords = polygon.exterior.coords
            coord_list = [list(coord) for coord in coords]
            points.extend(coord_list)
        return points

    def get_paths(self):
        polygon_list = self.get_dimension('polygon_list')
        paths = []
        point_index = 0
        for polygon in polygon_list:
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

    def _point_list_to_polygon(self,point_list):
            point_tuple_list = []
            for point in point_list:
                point_tuple_list.append(tuple(point))
            polygon = shapely.geometry.Polygon(point_tuple_list)
            return polygon

    def set_dimensions_(self,args,kwargs):
        if not kwargs.has_key('polygon_list'):
            if kwargs.has_key('polygon'):
                polygon = kwargs['polygon']
                kwargs['polygon_list'] = [polygon]
            elif kwargs.has_key('point_list'):
                point_list = kwargs['point_list']
                polygon = self._point_list_to_polygon(point_list)
                kwargs['polygon_list'] = [polygon]
            elif kwargs.has_key('x_list') and kwargs.has_key('y_list'):
                x_list = kwargs['x_list']
                y_list = kwargs['y_list']
                point_list = numpy.array([x_list,y_list])
                point_list = point_list.transpose()
                polygon = self._point_list_to_polygon(point_list)
                kwargs['polygon_list'] = [polygon]
            elif kwargs.has_key('dxf_file'):
                dxf_file = kwargs['dxf_file']
                polygon_list,decimals = dxf.import_dxf(dxf_file)
                kwargs['polygon_list'] = polygon_list
                kwargs['decimals'] = decimals
        super(Polygon, self).set_dimensions_(args,kwargs)

    def plot(self):
        points = self.get_points()
        x_list = []
        y_list = []
        for point in points:
            x_list.append(point[0])
            y_list.append(point[1])
        pylab.plot(x_list,y_list)
        pylab.axis('equal')
        pylab.show()
        # pylab.savefig('lineplot')
        # savefig('matplotlib-153.svg')

    def set_color(self,color=[],recursive=False):
        pass

    # def update_bounding_box(self):
    #     dimensions = self.get_dimensions()
    #     super(Polygon, self).update_bounding_box(x=1,y=1,z=0.1)


if __name__ == "__main__":
    pass
