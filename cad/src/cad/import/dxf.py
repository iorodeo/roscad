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
import numpy
from shapely.geometry import *
from shapely.ops import *

# angles have units of degrees

import dxfReader


# int get_fragments_from_r(double r, double fn, double fs, double fa)
# {
#       if (fn > 0.0)
#               return (int)fn;
#       return (int)ceil(fmax(fmin(360.0 / fa, r*M_PI / fs), 5));
# }


def order_lines(lines):
    line = lines.pop(0)
    lines_ordered = [line]
    start_point = line[0]
    next_point = line[1]
    while 0 < len(lines):
        # print lines
        index = 0
        while not numpy.allclose(next_point,lines[index][0]):
            index += 1
        line = lines.pop(index)
        lines_ordered.append(line)
        next_point = line[1]
    return lines_ordered

def get_fragment_count(radius,fn=0,fs=1,fa=12):
    if 0 < fn:
        return int(fn)
    else:
        return int(numpy.ceil(numpy.max(numpy.min([360/fa,radius*numpy.pi/fs]),5)))

def arc_to_lines(arc,fn=0,fs=1,fa=12,decimals=5):
    center = arc.loc
    start_angle = arc.start_angle
    end_angle = arc.end_angle
    radius = arc.radius
    fragment_count = get_fragment_count(radius,fn,fs,fa)
    # print fragment_count
    # print start_angle
    # print end_angle
    angle_inc = (start_angle - end_angle)/fragment_count
    angle = end_angle
    lines = []
    count = 0
    while count < fragment_count:
        x0 = center[0] + radius*numpy.cos(angle*numpy.pi/180)
        y0 = center[1] + radius*numpy.sin(angle*numpy.pi/180)
        point0 = [numpy.round(x0,decimals=decimals),numpy.round(y0,decimals=decimals)]
        if len(arc.loc) == 3:
            point0.append(arc.loc[2])
        angle += angle_inc
        x1 = center[0] + radius*numpy.cos(angle*numpy.pi/180)
        y1 = center[1] + radius*numpy.sin(angle*numpy.pi/180)
        point1 = [numpy.round(x1,decimals=decimals),numpy.round(y1,decimals=decimals)]
        if len(arc.loc) == 3:
            point1.append(arc.loc[2])
        line = [point0,point1]
        lines.append(line)
        count += 1
    return lines

def import_dxf(filename):
    drawing = dxfReader.readDXF(filename)
    lines = []

    for item in drawing.entities.data:
        if item.type == 'line':
            lines.append(item.points)
        elif item.type == 'arc':
            arc_lines = arc_to_lines(item)
            lines.extend(arc_lines)
    # for arc in drawing.entities.get_type('arc'):
    #     arc_lines = arc_to_lines(arc)
    #     lines.extend(arc_lines)
    # for line in drawing.entities.get_type('line'):
    #     lines.append(line.points)
    print lines
    # print '**************************************'
    # lines_ordered = order_lines(lines)
    # print lines_ordered
    result = polygonize(lines)
    for polygon in result:
        print polygon

if __name__ == "__main__":
    # profile = import_dxf('rectangle.dxf')
    # profile = import_dxf('rectangulartube.dxf')
    # profile = import_dxf('rectangle_rounded.dxf')
    # profile = import_dxf('1010.dxf')
    # profile = import_dxf('upper_left.dxf')
    # profile = import_dxf('lower_left.dxf')
    # profile = import_dxf('upper_right.dxf')
    # profile = import_dxf('lower_right.dxf')
    profile = import_dxf('box_holes.dxf')
