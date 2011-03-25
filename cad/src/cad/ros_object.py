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
import os
import numpy
import cad_object

# Check to see if ROS is installed
try:
    ros_root = os.environ['ROS_ROOT']
except:
    ros_root = ""


if ros_root == "":
    class ROSObject(cad_object.CADObject):
        """ROS object wrapper base class."""
        def __init__(self, position=[0,0,0], orientation=[0,0,0,1], scale=1, exportable=False, modifiers={}):
            super(ROSObject, self).__init__(position,orientation,scale,exportable,modifiers)

else:
    import roslib
    roslib.load_manifest('cad')
    import rospy
    import tf
    import geometry_msgs

    import copy

    class ROSObject(cad_object.CADObject):
        """ROS object wrapper base class."""
        def __init__(self):
            super(ROSObject, self).__init__()

        def rotate(self,angle=0,axis=[1,0,0]):
            axis = copy.deepcopy(axis)
            if type(axis) == type(geometry_msgs.msg.Vector3()):
                axis_vector = axis
                axis = [axis_vector.x,axis_vector.y,axis_vector.z]
            q_previous = self.get_orientation()
            q_rotation = tf.transformations.quaternion_about_axis(angle, axis)
            R = tf.transformations.quaternion_matrix(q_rotation)
            p_previous = self.get_position()
            p_previous.append(1)
            p_new = numpy.dot(R,p_previous)
            p_new = list(p_new[0:-1])
            q_new = tf.transformations.quaternion_multiply(q_rotation, q_previous)
            self.set_orientation(q_new)
            self.set_position(p_new)

        def set_rotation(self,angle=0,axis=[1,0,0]):
            axis = copy.deepcopy(axis)
            if type(axis) == type(geometry_msgs.msg.Vector3()):
                axis_vector = axis
                axis = [axis_vector.x,axis_vector.y,axis_vector.z]
            q_previous = self.get_orientation()
            q_rotation = tf.transformations.quaternion_about_axis(angle, axis)
            q_new = tf.transformations.quaternion_multiply(q_previous, q_rotation)
            self.set_orientation(q_new)

        def get_rotation(self):
            q = self.get_orientation()
            rotation = tf.transformations.euler_from_quaternion(q,'sxyz')
            return rotation

        def get_obj_str(self,depth=0):
            obj_str_header = super(ROSObject, self).get_obj_str(depth)
            obj_str = '{indent}rotation = \n{indent}{rotation:s}\n'
            obj_str = obj_str.format(indent = self.get_export_parameter('indent_str')*depth,
                                     rotation = str(self.get_rotation()))
            obj_str = obj_str_header + obj_str
            return obj_str


if __name__ == "__main__":
    ros_object = ROSObject()
    print ros_object
