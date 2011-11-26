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
import copy

import cad_object


class Camera(cad_object.CADObject):
    def __init__(self,name='default',projection='perspective',angle=65,position=[0,0,100],look_at=[0,0,0],image_size=[640,480],image_dir=''):
        super(Camera, self).__init__()
        image_ext = '.png'
        image_name = name + image_ext
        self.set_obj_parameter('camera_name',name)
        self.set_obj_parameter('camera_projection',projection)
        self.set_obj_parameter('camera_angle',angle)
        self.set_position(position)
        self.set_obj_parameter('camera_look_at',look_at)
        self.set_obj_parameter('image_size',image_size)
        self.set_obj_parameter('image_ext',image_ext)
        self.set_obj_parameter('image_name',image_name)
        self.set_obj_parameter('image_dir',image_dir)
        self.set_obj_parameter('image_path',os.path.join(image_dir,image_name))


class Light(cad_object.CADObject):
    def __init__(self,position=[0,0,1000],color=[1.0,1.0,1.0,1.0]):
        super(Light, self).__init__()
        self.set_position(position)
        self.set_color(color)

class RenderObject(cad_object.CADObject):
    """Render object wrapper base class."""
    def __init__(self):
        super(RenderObject, self).__init__()
        self.camera_dict = {}
        self.light_list = []
        self.add_camera(name='default')

    def get_light_list(self):
        return copy.deepcopy(self.light_list)

    def set_light_list(self,light_list):
        self.light_list = []
        if type(light_list) == list:
            self.light_list.extend(light_list)
        else:
            self.light_list.append(light_list)

    def add_light(self,position=[0,0,1000],color=[1.0,1.0,1.0,1.0]):
        light = Light(position,color)
        self.light_list.append(light)

    def get_camera_name(self):
        return self.camera.get_obj_parameter('camera_name')

    def get_camera_names(self):
        return copy.deepcopy(self.camera_dict.keys())

    def get_camera_count(self):
        return len(self.camera_dict)

    def clear_cameras(self):
        self.camera_dict = {}

    def add_camera(self,name='',projection='perspective',angle=65,position=[0,0,100],look_at=[0,0,0],image_size=[640,480],image_dir=''):
        if name == '':
            camera_count = self.get_camera_count()
            name = 'camera' + str(camera_count)

        # Replace default if that is the only camera
        camera_count = self.get_camera_count()
        if 0 < camera_count:
            camera_name = self.get_camera_name()
            if (camera_count == 1) and (camera_name == 'default'):
                self.clear_cameras()

        self.camera_dict[name] = Camera(name,projection,angle,position,look_at,image_size,image_dir)
        camera_count = self.get_camera_count()
        if camera_count == 1:
            self.set_camera(name)

    def remove_camera(self,camera_name):
        name = self.camera.get_obj_parameter('camera_name')
        self.camera_dict.pop(camera_name)
        if name == camera_name:
            camera_names = self.get_camera_names()
            self.camera = self.camera_dict[camera_names[0]]

    def set_camera(self,camera_name='default'):
        self.camera = self.camera_dict[camera_name]

    def render(self):
        image_path = self.camera.get_obj_parameter('image_path')
        self.export(image_path)

    def render_all(self):
        camera_name_previous = self.get_camera_name()
        camera_names = self.get_camera_names()
        for camera_name in camera_names:
            self.set_camera(camera_name)
            self.render()
        self.set_camera(camera_name_previous)

if __name__ == "__main__":
    render_object = RenderObject()
    print render_object
