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

from shapely.geometry import *
from shapely.ops import *

import dxf_reader
import cad_utilities.circle_functions as cf


def convert_3D_to_2D(lines3d):
    lines2d = []
    for line3d in lines3d:
        [point3d0,point3d1] = line3d
        point2d0 = [point3d0[0],point3d0[1]]
        point2d1 = [point3d1[0],point3d1[1]]
        line2d = [point2d0,point2d1]
        lines2d.append(line2d)
    return lines2d

def x_from_lines(lines):
    x = []
    for line in lines:
        for point in line:
            x.append(point[0])
    return x

def y_from_lines(lines):
    y = []
    for line in lines:
        for point in line:
            y.append(point[1])
    return y

def plot_lines(lines):
    # print lines
    lines = numpy.array(convert_3D_to_2D(lines))
    # print lines
    x = numpy.array(x_from_lines(lines))
    y = numpy.array(y_from_lines(lines))
    # print x
    line_segments = LineCollection(lines)

    # In order to efficiently plot many lines in a single set of axes,
    # Matplotlib has the ability to add the lines all at once. Here is a
    # simple example showing how it is done.

    # N = 50
    # x = arange(N)
    # Here are many sets of y to plot vs x
    # ys = [x+i for i in x]

    # We need to set the plot limits, they will not autoscale
    ax = pylab.axes()
    ax.set_xlim((1.1*pylab.amin(x),1.1*pylab.amax(x)))
    ax.set_ylim((1.1*pylab.amin(pylab.amin(y)),1.1*pylab.amax(pylab.amax(y))))

    # colors is sequence of rgba tuples
    # linestyle is a string or dash tuple. Legal string values are
    #          solid|dashed|dashdot|dotted.  The dash tuple is (offset, onoffseq)
    #          where onoffseq is an even length tuple of on and off ink in points.
    #          If linestyle is omitted, 'solid' is used
    # See matplotlib.collections.LineCollection for more information

    # line_segments = LineCollection([zip(x,y) for y in ys], # Make a sequence of x,y pairs
    #                                 linewidths    = (0.5,1,1.5,2),
    #                                 linestyles = 'solid')
    line_segments.set_array(x)
    ax.add_collection(line_segments)
    fig = pylab.gcf()
    axcb = fig.colorbar(line_segments)
    axcb.set_label('Line Number')
    ax.set_title('Line Collection with mapped colors using matplotlib')
    # sci(line_segments) # This allows interactive changing of the colormap.
    pylab.axis('equal')
    pylab.savefig('lineplot')
    pylab.show()
    # savefig('matplotlib-153.svg')



# int get_fragments_from_r(double r, double fn, double fs, double fa)
# {
#       if (fn > 0.0)
#               return (int)fn;
#       return (int)ceil(fmax(fmin(360.0 / fa, r*M_PI / fs), 5));
# }


# def order_lines(lines):
#     line = lines.pop(0)
#     lines_ordered = [line]
#     start_point = line[0]
#     next_point = line[1]
#     while 0 < len(lines):
#         # print lines
#         index = 0
#         while not numpy.allclose(next_point,lines[index][0]):
#             index += 1
#         line = lines.pop(index)
#         lines_ordered.append(line)
#         next_point = line[1]
#     return lines_ordered

def get_fragment_count(radius,fn=0,fs=1,fa=12):
    if 0 < fn:
        return int(fn)
    else:
        return int(numpy.ceil(numpy.max([numpy.min([360/fa,radius*numpy.pi/fs]),5])))

def arc_to_lines(arc,fn=0,fs=1,fa=12,decimals=5):
    center = arc.loc
    start_angle = cf.degrees_to_radians(arc.start_angle)
    end_angle = cf.degrees_to_radians(arc.end_angle)
    radius = arc.radius
    fragment_count = get_fragment_count(radius,fn,fs,fa)
    print "fragment_count = " + str(fragment_count)
    print "start_angle = " + str(start_angle)
    print "end_angle = " + str(end_angle)
    angle_inc = cf.circle_dist(start_angle,end_angle)/fragment_count
    # print "angle_inc = " + str(angle_inc)
    angle = start_angle
    lines = []
    count = 0
    while count < fragment_count:
        # print angle
        point0 = cf.polar_to_cartesean(center=center,radius=radius,angle=angle,decimals=decimals)
        if len(arc.loc) == 3:
            point0.append(arc.loc[2])
        angle += angle_inc
        point1 = cf.polar_to_cartesean(center=center,radius=radius,angle=angle,decimals=decimals)
        if len(arc.loc) == 3:
            point1.append(arc.loc[2])
        line = [point0,point1]
        lines.append(line)
        count += 1
    # print angle
    # print lines
    return lines

def import_dxf(filename):
    drawing = dxf_reader.readDXF(filename)
    lines = []

    for item in drawing.entities.data:
        # print item
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
    # print lines
    # print '**************************************'
    # lines_ordered = order_lines(lines)
    # print lines_ordered
    plot_lines(lines)
    polygons = polygonize(lines)
    return polygons

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
    for polygon in profile:
        print polygon
