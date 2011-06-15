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

# def plot_polygons(polygons):
#     # print lines
#     lines = numpy.array(convert_3D_to_2D(lines))
#     # print lines
#     x = numpy.array(x_from_lines(lines))
#     y = numpy.array(y_from_lines(lines))
#     # print x
#     line_segments = LineCollection(lines)

#     # In order to efficiently plot many lines in a single set of axes,
#     # Matplotlib has the ability to add the lines all at once. Here is a
#     # simple example showing how it is done.

#     # N = 50
#     # x = arange(N)
#     # Here are many sets of y to plot vs x
#     # ys = [x+i for i in x]

#     # We need to set the plot limits, they will not autoscale
#     ax = pylab.axes()
#     ax.set_xlim((1.1*pylab.amin(x),1.1*pylab.amax(x)))
#     ax.set_ylim((1.1*pylab.amin(pylab.amin(y)),1.1*pylab.amax(pylab.amax(y))))

#     # colors is sequence of rgba tuples
#     # linestyle is a string or dash tuple. Legal string values are
#     #          solid|dashed|dashdot|dotted.  The dash tuple is (offset, onoffseq)
#     #          where onoffseq is an even length tuple of on and off ink in points.
#     #          If linestyle is omitted, 'solid' is used
#     # See matplotlib.collections.LineCollection for more information

#     # line_segments = LineCollection([zip(x,y) for y in ys], # Make a sequence of x,y pairs
#     #                                 linewidths    = (0.5,1,1.5,2),
#     #                                 linestyles = 'solid')
#     line_segments.set_array(x)
#     ax.add_collection(line_segments)
#     fig = pylab.gcf()
#     axcb = fig.colorbar(line_segments)
#     axcb.set_label('Line Number')
#     ax.set_title('Line Collection with mapped colors using matplotlib')
#     # sci(line_segments) # This allows interactive changing of the colormap.
#     pylab.axis('equal')
#     pylab.savefig('lineplot')
#     pylab.show()
#     # savefig('matplotlib-153.svg')

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
    end_angle = cf.degrees_to_radians(arc.end_angle) + 2*math.pi
    # start_angle = cf.degrees_to_radians(arc.end_angle)
    # end_angle = cf.degrees_to_radians(arc.start_angle)
    radius = arc.radius
    fragment_count = get_fragment_count(radius,fn,fs,fa)
    # print "fragment_count = " + str(fragment_count)
    # print "start_angle = " + str(start_angle)
    # print "end_angle = " + str(end_angle)
    angle_inc = ((end_angle - start_angle)%(2*math.pi))/fragment_count
    # angle_inc = cf.circle_dist(start_angle,end_angle)/fragment_count
    # print "angle_inc = " + str(angle_inc)
    angle = start_angle
    arc_lines = []
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
        arc_lines.append(line)
        count += 1
    # print angle
    # print arc_lines
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
                # print "original number = " + str(number)
                number = round(number,decimals)
                # print "rounded number = " + str(number)
                lines[line_index][point_index][number_index] = number
    return lines

def import_dxf(file,fn=0,fs=1,fa=12,decimals=5,close_gaps=False):
    drawing = dxf_reader.readDXF(file)
    polygonized = False

    while (not polygonized) and (0 <= decimals):
        try:
            lines = []

            for item in drawing.entities.data:
                # print item
                if item.type == 'line':
                    lines.append(item.points)
                elif item.type == 'arc':
                    arc_lines = arc_to_lines(item,fn,fs,fa,decimals)
                    lines.extend(arc_lines)
                # elif item.type == 'circle':
                #     circle_lines = circle_to_lines(item,fn,fs,fa,decimals)
                #     lines.extend(circle_lines)

            lines_rounded = round_numbers_in_lines(lines,decimals)
            polygons_iterator = shapely.ops.polygonize(lines_rounded)
            polygons = [polygon for polygon in polygons_iterator]
            polygonized = True
        except ValueError:
            # print "Failed, using decimals value: " + str(decimals)
            decimals -= 1
            # print "Trying again using decimals value: " + str(decimals)

    # For some reason, it seems that circles need to be done separately
    for item in drawing.entities.data:
        if item.type == 'circle':
            circle_lines = circle_to_lines(item,fn,fs,fa,decimals)
            polygons_iterator = shapely.ops.polygonize(circle_lines)
            try:
                circle_polygon = [polygon for polygon in polygons_iterator]
                polygons.extend(circle_polygon)
            except ValueError:
                pass

    # plot_lines(lines_rounded)
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
    # print list(profile.geoms)
    # for polygon in profile:
    #     print polygon
