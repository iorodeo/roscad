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
        def __init__(self, position=[0,0,0], orientation=[0,0,0,1], scale=1, exportable=False, modifiers={}):
            super(ROSObject, self).__init__(position,orientation,scale,exportable,modifiers)

        def rotate(self,angle=0,axis=[1,0,0]):
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
            obj_str = obj_str.format(indent = self.indent_str*depth,
                                     rotation = str(self.get_rotation()))
            obj_str = obj_str_header + obj_str
            return obj_str

        # def __str__(self,depth=0):
        #     rtn_str_header = super(ROSObject, self).__str__()
        #     rtn_str = 'rotation = \n{rotation:s}\n'
        #     rtn_str = rtn_str.format(rotation = str(self.get_rotation()))
        #     rtn_str = rtn_str_header + rtn_str
        #     return rtn_str


        # def __init__(self, pose_stamped=geometry_msgs.msg.PoseStamped(), scale=1):
        #     self.comment_syntax = '// '
        #     self.comment = ''
        #     self.pose_stamped = geometry_msgs.msg.PoseStamped()
        #     self.set_pose_stamped(pose_stamped)

        #     self.scale = geometry_msgs.msg.Vector3()
        #     self.set_scale(scale)

        #     self.printable = False
        #     self.color = []

        # def __str__(self):
        #     return ""

        # def copy(self):
        #     return copy.deepcopy(self)

        # def set_pose_stamped(self,pose_stamped=geometry_msgs.msg.PoseStamped()):
        #     if type(pose_stamped) == type(geometry_msgs.msg.PoseStamped()):
        #         self.pose_stamped = pose_stamped
        #         if self.pose_stamped.pose.orientation.w == 0:
        #             self.pose_stamped.pose.orientation.w = 1

        # def get_pose_stamped(self):
        #     return self.pose_stamped

        # def set_frame_id(self,frame_id=""):
        #     self.pose_stamped = copy.deepcopy(self.pose_stamped)
        #     if type(frame_id) == str:
        #         self.pose_stamped.header.frame_id = frame_id

        # def get_frame_id(self):
        #     return copy.deepcopy(self.pose_stamped.header.frame_id)

        # def set_pose(self,pose=geometry_msgs.msg.Pose()):
        #     self.pose_stamped = copy.deepcopy(self.pose_stamped)
        #     if type(pose) == type(geometry_msgs.msg.Pose()):
        #         self.pose_stamped.pose = pose
        #         if self.pose_stamped.pose.orientation.w == 0:
        #             self.pose_stamped.pose.orientation.w = 1

        # def get_pose(self):
        #     return copy.deepcopy(self.pose_stamped.pose)

        # def set_position(self,position=geometry_msgs.msg.Point()):
        #     self.pose_stamped = copy.deepcopy(self.pose_stamped)
        #     if type(position) == type(geometry_msgs.msg.Point()):
        #         self.pose_stamped.pose.position = position
        #     else:
        #         self.pose_stamped.pose.position.x = position[0]
        #         self.pose_stamped.pose.position.y = position[1]
        #         self.pose_stamped.pose.position.z = position[2]

        # def get_position(self):
        #     return copy.deepcopy(self.pose_stamped.pose.position)

        # def get_position_list(self):
        #     p = copy.deepcopy(self.pose_stamped.pose.position)
        #     return [p.x,p.y,p.z]

        # def set_orientation(self,orientation=geometry_msgs.msg.Quaternion()):
        #     self.pose_stamped = copy.deepcopy(self.pose_stamped)
        #     if type(orientation) == type(geometry_msgs.msg.Quaternion()):
        #         self.pose_stamped.pose.orientation = orientation
        #     else:
        #         self.pose_stamped.pose.orientation.x = orientation[0]
        #         self.pose_stamped.pose.orientation.y = orientation[1]
        #         self.pose_stamped.pose.orientation.z = orientation[2]
        #         self.pose_stamped.pose.orientation.w = orientation[3]
        #     if self.pose_stamped.pose.orientation.w == 0:
        #         self.pose_stamped.pose.orientation.w = 1

        # def get_orientation(self):
        #     return copy.deepcopy(self.pose_stamped.pose.orientation)

        # def get_orientation_list(self):
        #     o = copy.deepcopy(self.pose_stamped.pose.orientation)
        #     return [o.x,o.y,o.z,o.w]

        # def translate(self,translation=[0,0,0]):
        #     position = self.get_position()
        #     if type(translation) == type(geometry_msgs.msg.Vector3()):
        #         position.x += translation.x
        #         position.y += translation.y
        #         position.z += translation.z
        #     else:
        #         position.x += translation[0]
        #         position.y += translation[1]
        #         position.z += translation[2]
        #     self.set_position(position)

        # def rotate(self,angle=0,axis=[1,0,0]):
        #     if type(axis) == type(geometry_msgs.msg.Vector3()):
        #         axis_vector = axis
        #         axis = [axis_vector.x,axis_vector.y,axis_vector.z]
        #     q_previous = self.get_orientation_list()
        #     q_rotation = tf.transformations.quaternion_about_axis(angle, axis)
        #     q_new = tf.transformations.quaternion_multiply(q_previous, q_rotation)
        #     self.set_orientation(q_new)

        # def get_rotation(self):
        #     q = self.get_orientation_list()
        #     rotation = tf.transformations.euler_from_quaternion(q,'sxyz')
        #     return rotation

        # def set_scale(self,scale=1):
        #     self.scale = copy.deepcopy(self.scale)
        #     if type(scale) == type(geometry_msgs.msg.Vector3()):
        #         self.scale = scale
        #     elif (type(scale) == list) or (type(scale) == tuple):
        #         self.scale.x = scale[0]
        #         self.scale.y = scale[1]
        #         self.scale.z = scale[2]
        #     else:
        #         self.scale.x = scale
        #         self.scale.y = scale
        #         self.scale.z = scale

        # def get_scale(self):
        #     return copy.deepcopy(self.scale)

        # def cmd_str(self,tab_level=0):
        #     return 'CADObect'

        # def __str__(self):
        #     rtn_str_header = '\nCADObject\n'
        #     rtn_str = rtn_str_header + 'class = \n{class_:s}\npose_stamped = \n{pose_stamped:s}\nscale = \n{scale:s}\nprintable = \n{printable:s}\n'
        #     rtn_str = rtn_str.format(class_ = str(self.__class__),
        #                              pose_stamped = str(self.get_pose_stamped()),
        #                              scale = str(self.get_scale()),
        #                              printable = str(self.printable))

        #     # rtn_str = '%s%s\n\n'%(rtn_str,obj)

        #     try:
        #         for obj in self.objlist:
        #             rtn_str = '%s%s'%(rtn_str,obj)
        #             # print obj
        #     except:
        #         pass

        #     return rtn_str

        # def __str__(self,tab_level=0):
        #     tab_str = ' '*TAB_WIDTH*tab_level
        #     comment = tab_str + self.comment_syntax + self.comment + '\n'
        #     rtn_str = 'class = \n{class_:s}\npose_stamped = \n{pose_stamped:s}\nscale = \n{scale:s}\nprintable = \n{printable:s}\n'
        #     rtn_str = rtn_str.format(class_ = str(self.__class__),
        #                              pose_stamped = str(self.get_pose_stamped()),
        #                              scale = str(self.get_scale()),
        #                              printable = str(self.printable))
        #     try:
        #         for obj in self.objlist:
        #             rtn_str = '{0}{1}{2}{3}'.format(tab_str,
        #                                             rtn_str,
        #                                             self.cmd_str(tab_level=tab_level),
        #                                             obj)
        #     except:
        #         pass

        #     return comment + rtn_str


if __name__ == "__main__":
    ros_object = ROSObject()
    print ros_object
