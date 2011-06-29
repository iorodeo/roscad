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
import numpy
from matplotlib.collections import LineCollection
import pylab
import math
import copy

import shapely.geometry
import shapely.ops

import dxf_reader
import cad_utilities.circle_functions as cf


def get_fragment_count(radius,fn=0,fs=1,fa=12):
    if 0 < fn:
        return int(fn)
    else:
        return int(numpy.ceil(numpy.max([numpy.min([360/fa,radius*numpy.pi/fs]),5])))

def arc_to_lines(arc,fn=0,fs=1,fa=12,decimals=5):
    center = arc.loc
    start_angle = cf.degrees_to_radians(arc.start_angle)
    end_angle = cf.degrees_to_radians(arc.end_angle) + 2*math.pi
    radius = arc.radius
    fragment_count = get_fragment_count(radius,fn,fs,fa)
    angle_inc = ((end_angle - start_angle)%(2*math.pi))/fragment_count
    angle = start_angle
    arc_lines = []
    count = 0
    while count < fragment_count:
        point0 = cf.polar_to_cartesean(center=center,radius=radius,angle=angle,decimals=decimals)
        if len(arc.loc) == 3:
            point0.append(arc.loc[2])
        angle += angle_inc
        point1 = cf.polar_to_cartesean(center=center,radius=radius,angle=angle,decimals=decimals)
        if len(arc.loc) == 3:
            point1.append(arc.loc[2])
        line = [point0,point1]
        arc_lines.append(line)
        count += 1
    return arc_lines

def circle_to_lines(circle,fn=0,fs=1,fa=12,decimals=5):
    center = circle.loc
    start_angle = 0
    end_angle = 2*math.pi
    radius = circle.radius
    fragment_count = get_fragment_count(radius,fn,fs,fa)
    angle_inc = 2*math.pi/fragment_count
    angle = start_angle
    circle_lines = []
    count = 0
    while count < fragment_count:
        point0 = cf.polar_to_cartesean(center=center,radius=radius,angle=angle,decimals=decimals)
        if len(circle.loc) == 3:
            point0.append(circle.loc[2])
        angle += angle_inc
        point1 = cf.polar_to_cartesean(center=center,radius=radius,angle=angle,decimals=decimals)
        if len(circle.loc) == 3:
            point1.append(circle.loc[2])
        line = [point0,point1]
        circle_lines.append(line)
        count += 1
    return circle_lines

def round_numbers_in_lines(lines_original,decimals):
    lines = copy.deepcopy(lines_original)
    for line_index in range(len(lines)):
        line = lines[line_index]
        for point_index in range(len(line)):
            point = line[point_index]
            for number_index in range(len(point)):
                number = point[number_index]
                number = round(number,decimals)
                lines[line_index][point_index][number_index] = number
    return lines

def import_dxf(file,fn=0,fs=1,fa=12,decimals=5,close_gaps=False):
    drawing = dxf_reader.readDXF(file)
    polygonized = False

    while (not polygonized) and (0 <= decimals):
        try:
            lines = []

            for item in drawing.entities.data:
                if item.type == 'line':
                    lines.append(item.points)
                elif item.type == 'arc':
                    arc_lines = arc_to_lines(item,fn,fs,fa,decimals)
                    lines.extend(arc_lines)

            lines_rounded = round_numbers_in_lines(lines,decimals)
            polygon_list_iterator = shapely.ops.polygonize(lines_rounded)
            polygon_list = [polygon for polygon in polygon_list_iterator]
            polygonized = True
        except ValueError:
            decimals -= 1

    # For some reason, it seems that circles need to be done separately
    for item in drawing.entities.data:
        if item.type == 'circle':
            circle_lines = circle_to_lines(item,fn,fs,fa,decimals)
            polygon_list_iterator = shapely.ops.polygonize(circle_lines)
            try:
                circle_polygon = [polygon for polygon in polygon_list_iterator]
                polygon_list.extend(circle_polygon)
            except ValueError:
                pass

    return polygon_list,decimals

if __name__ == "__main__":
    # profile = import_dxf('rectangle.dxf')
    # profile = import_dxf('rectangulartube.dxf')
    # profile = import_dxf('rectangle_rounded.dxf')
    # profile = import_dxf('1010.dxf')
    # profile = import_dxf('i_beam.dxf')
    # profile = import_dxf('twistedup.dxf')
    # profile = import_dxf('curved.dxf')
    profile = import_dxf('most_arc.dxf')
    # profile = import_dxf('upper_left.dxf')
    # profile = import_dxf('lower_left.dxf')
    # profile = import_dxf('upper_right.dxf')
    # profile = import_dxf('lower_right.dxf')
    # profile = import_dxf('box_holes.dxf')
    # print list(profile.geoms)
    # for polygon in profile:
    #     print polygon
