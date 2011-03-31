from __future__ import division
import roslib
roslib.load_manifest('cad_library')
import rospy
import cad.finite_solid_objects as fso
import cad.csg_objects as csg
import numpy
import copy


class Vector(csg.Union):
    def __init__(self,tail=[0,0,0],head=[1,0,0],color=[1,0,0]):
        super(Vector, self).__init__()
        z_axis = numpy.array([0,0,1])
        tail = numpy.array(tail)
        head = numpy.array(head)
        vector = head - tail
        length = numpy.linalg.norm(vector)

        cone_cylinder_length_ratio = 0.2
        cone_head_tail_ratio = 0.1
        cylinder_radius_length_ratio = 0.02
        cone_tail_cylinder_radius_ratio = 3
        cone_head_cylinder_radius_ratio = 0.1

        cylinder_length = length/(1 + cone_cylinder_length_ratio/2)
        cylinder_radius = cylinder_length*cylinder_radius_length_ratio
        cone_length = cylinder_length*cone_cylinder_length_ratio
        cone_tail_radius = cylinder_radius*cone_tail_cylinder_radius_ratio
        cone_head_radius = cylinder_radius*cone_head_cylinder_radius_ratio

        cylinder = fso.Cylinder(l=cylinder_length,r=cylinder_radius)
        cone = fso.Cone(l=cone_length,r_pos=cone_head_radius,r_neg=cone_tail_radius)
        cone.translate([0,0,cylinder_length/2])

        self.add_obj([cylinder,cone])
        self.translate([0,0,cylinder_length/2])

        rot_axis = numpy.cross(z_axis,vector)
        dot = numpy.dot(z_axis,vector)
        z_axis_modulus = numpy.sqrt((z_axis*z_axis).sum())
        vector_modulus = numpy.sqrt((vector*vector).sum())
        rot_angle = numpy.pi/2 - dot/z_axis_modulus/vector_modulus
        # print "dot = " + str(dot)
        # print "z_axis_modulus = " + str(z_axis_modulus)
        # print "vector_modulus = " + str(vector_modulus)
        # print "angle = " + str(rot_angle)
        # print "axis = " + str(rot_axis)
        self.rotate(angle=rot_angle,axis=rot_axis)
        self.translate(list(tail))
        self.set_color(color,recursive=True)


# ---------------------------------------------------------------------
if __name__ == '__main__':
    vector = Vector()
    vector.export()
