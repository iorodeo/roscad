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
import scad
import povray
import bom
import matplotlib
import subprocess

export_maps = {'scad': scad.SCADExportMap,
               'povray': povray.POVRAYExportMap,
               'bom': bom.BOMExportMap,
               }


def get_export_map_filename_and_postprocess_filename(obj,filename,filetype):
    postprocess_filename_extension = ""
    filename = os.path.expanduser(filename)
    filename_base, filename_extension = os.path.splitext(filename)
    if (filetype != None):
        if type(filetype) != str:
            filetype = str(filetype)
        filetype = filetype.lower()
        if (filetype == 'scad') or (filetype == 's'):
            filename_extension = '.scad'
        elif (filetype == 'povray') or (filetype == 'pov') or (filetype == 'p'):
            filename_extension = '.pov'
        elif (filetype == 'bom') or (filetype == 'b'):
            filename_extension = '.txt'
        elif (filetype == 'image') or (filetype == 'i') or (filetype == 'png'):
            filename_extension = '.pov'
            postprocess_filename_extension = '.png'
    elif filename_extension == '':
        filename_extension = '.scad'

    filename_extension = filename_extension.lower()
    if filename_extension == '.pov':
        filetype = 'povray'
    elif filename_extension == '.txt':
        filetype = 'bom'
    elif filename_extension == '.png':
        filetype = 'povray'
        filename_extension = '.pov'
        postprocess_filename_extension = '.png'
    else:
        filename_extension = '.scad'
        filetype = 'scad'

    if filetype == 'scad':
        export_map = export_maps['scad'](obj)
    elif filetype == 'povray':
        export_map = export_maps['povray'](obj)
    elif filetype == 'bom':
        export_map = export_maps['bom'](obj)

    filename = filename_base + filename_extension

    postprocess_filename = ""
    if postprocess_filename_extension != "":
        postprocess_filename = filename_base + postprocess_filename_extension

    return export_map,filename,postprocess_filename

def write_export_file(obj,filename,filetype):
    export_map,filename,postprocess_filename = get_export_map_filename_and_postprocess_filename(obj,filename,filetype)
    file_header_str = export_map.get_file_header_str(obj,filename)
    objects_str = export_map.get_objects_str(obj)
    dirname = os.path.dirname(filename)
    if dirname != '':
        if not os.path.exists(dirname):
            os.mkdir(dirname)
    fid = open(filename,'w')
    fid.write(file_header_str)
    fid.write(objects_str)
    fid.close()
    if postprocess_filename != "":
        command_str = "povray +I" + filename + " -O" + postprocess_filename
        try:
            image_size = obj.get_obj_parameter('image_size')
            image_width = image_size[0]
            image_height = image_size[1]
            command_str += " +W" + str(int(image_width)) + " +H" + str(int(image_height))
        except KeyError:
            command_str += " +W640 +H480"
        command_str += " +A"
        try:
            display_render = obj.get_obj_parameter('display_render')
            if not display_render:
                command_str += " -D"
        except KeyError:
            command_str += " -D"
        subprocess.check_call(command_str, shell=True)


if __name__ == "__main__":
    scad_export_map = maps['scad']()
