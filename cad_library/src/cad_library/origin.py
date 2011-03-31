from __future__ import division
import roslib
roslib.load_manifest('cad_library')
import rospy
import cad.finite_solid_objects as fso
import cad.csg_objects as csg
import numpy
import copy

import vector

class Origin(csg.Union):
    def __init__(self,mag=10):
        super(Origin,self).__init__()
        x_vector = vector.Vector(tail=[0,0,0],head=[mag,0,0],color=[1,0,0])
        y_vector = vector.Vector(tail=[0,0,0],head=[0,mag,0],color=[0,1,0])
        z_vector = vector.Vector(tail=[0,0,0],head=[0,0,mag],color=[0,0,1])
        origin_point = fso.Sphere(r=mag/20)
        origin_point.set_color([1,1,0])
        self.add_obj([origin_point,x_vector,y_vector,z_vector])

# ---------------------------------------------------------------------
if __name__ == '__main__':
    origin = Origin(100)
    origin.export()
