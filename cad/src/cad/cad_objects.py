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
import rospy
import tf
import geometry_msgs


class CADProject(object):
    """Wrapper for a CAD project."""

    def __init__(self):
        self.objlist = []

    def add(self, obj):
        """Add a CAD object to this project container."""
        if type(obj) == list:
            self.objlist.extend(obj)
        else:
            self.objlist.append(obj)

class CADObject(object):
    """CAD object wrapper base class."""

    def __init__(self, pose_stamped=geometry_msgs.msg.PoseStamped(), scale=1):
        self.pose_stamped = geometry_msgs.msg.PoseStamped()
        self.set_pose_stamped(pose_stamped)

        self.scale = geometry_msgs.msg.Vector3()
        self.set_scale(scale)

    def set_pose_stamped(self,pose_stamped=geometry_msgs.msg.PoseStamped()):
        if type(pose_stamped) == type(geometry_msgs.msg.PoseStamped()):
            self.pose_stamped = pose_stamped

    def get_pose_stamped(self):
        return self.pose_stamped

    def set_frame_id(self,frame_id=""):
        if type(frame_id) == str:
            self.pose_stamped.header.frame_id = frame_id

    def get_frame_id(self):
        return self.pose_stamped.header.frame_id

    def set_pose(self,pose=geometry_msgs.msg.Pose()):
        if type(pose) == type(geometry_msgs.msg.Pose()):
            self.pose_stamped.pose = pose

    def get_pose(self):
        return self.pose_stamped.pose

    def set_position(self,position=geometry_msgs.msg.Point()):
        if type(position) == type(geometry_msgs.msg.Point()):
            self.pose_stamped.pose.position = position
        else:
            self.pose_stamped.pose.position.x = position[0]
            self.pose_stamped.pose.position.y = position[1]
            self.pose_stamped.pose.position.z = position[2]

    def get_position(self):
        return self.pose_stamped.pose.position

    def set_orientation(self,orientation=geometry_msgs.Quaternion()):
        if type(orientation) == type(geometry_msgs.Quaternion()):
            self.pose_stamped.pose.orientation = orientation
        else:
            self.pose_stamped.pose.orientation.x = orientation[0]
            self.pose_stamped.pose.orientation.y = orientation[1]
            self.pose_stamped.pose.orientation.z = orientation[2]
            self.pose_stamped.pose.orientation.w = orientation[3]

    def get_orientation(self):
        return self.pose_stamped.pose.orientation

    def translate(self,translation=[0,0,0]):
        if type(translation) == type(geometry_msgs.msg.Vector3()):
            self.pose_stamped.pose.position.x += translation.x
            self.pose_stamped.pose.position.y += translation.y
            self.pose_stamped.pose.position.z += translation.z
        else:
            self.pose_stamped.pose.position.x += translation[0]
            self.pose_stamped.pose.position.y += translation[1]
            self.pose_stamped.pose.position.z += translation[2]

    def rotate(self,angle=0,axis=[1,0,0]):
        if type(axis) == type(geometry_msgs.msg.Vector3()):
            axis_vector = axis
            axis = [axis_vector.x,axis_vector.y,axis_vector.z]
        q_previous = self.pose_stamped.pose.orientation
        q_rotation = tf.transformations.quaternion_about_axis(angle, axis)
        self.pose_stamped.pose.orientation = tf.transformations.quaternion_multiply(q_previous, q_rotation)

    def get_rotation(self):
        q = self.pose_stamped.pose.orientation
        rotation = tf.transformations.euler_from_quaternion(q,'sxyz')
        return rotation

    def set_scale(self,scale=1):
        if type(scale) == type(geometry_msgs.msg.Vector3()):
            self.scale = scale
        elif (type(scale) == list) or (type(scale) == tuple):
            self.scale.x = scale[0]
            self.scale.y = scale[1]
            self.scale.z = scale[2]
        else:
            self.scale.x = scale
            self.scale.y = scale
            self.scale.z = scale

    def get_scale(self):
        return self.scale

