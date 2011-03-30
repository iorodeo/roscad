from __future__ import division
import roslib
roslib.load_manifest('cad_library')
import rospy
import cad.finite_solid_objects as fso
import cad.csg_objects as csg
import copy


# RAB air bearing parameters
# Data sheet parameter
RAB4_params = {                            # --------------------
        'slide_width'          : 4.0,      # A
        'slide_height'         : 1.5,      # B
        'carriage_length'      : 5.0,      # C
        'carriage_width'       : 5.5,      # D,E
        'carriage_height'      : 3.0,      # F
        'slide_screw_inset'    : 0.313,    # G
        'slide_screw_dW'       : 3.0,      # H
        'carriage_screw_dW'    : 4.75,     # J
        'carriage_screw_dL'    : 3.25,     # K
        'slide_base_length'    : 6.25,     # L
        'slide_screw_size'     : 0.25,     # M
        'carriage_screw_size'  : 0.25,     # N
        'slide_tolerance'      : 0.005,
        }

# Data sheet parameter
RAB6_params = {                            # --------------------
        'slide_width'          : 6.0,      # A
        'slide_height'         : 1.75,     # B
        'carriage_length'      : 7.0,      # C
        'carriage_width'       : 7.5,      # D,E
        'carriage_height'      : 3.25,     # F
        'slide_screw_inset'    : 0.313,    # G
        'slide_screw_dW'       : 5.0,      # H
        'carriage_screw_dW'    : 6.75,     # J
        'carriage_screw_dL'    : 5.00,     # K
        'slide_base_length'    : 8.25,     # L
        'slide_screw_size'     : 0.25,     # M
        'carriage_screw_size'  : 0.25,     # N
        'slide_tolerance'      : 0.005,
        }

# Data sheet parameter
RAB10_params = {                           # --------------------
        'slide_width'          : 10.0,     # A
        'slide_height'         : 3.0,      # B
        'carriage_length'      : 12.0,     # C
        'carriage_width'       : 12.0,     # D,E
        'carriage_height'      : 5.5,      # F
        'slide_screw_inset'    : 0.313,    # G
        'slide_screw_dW'       : 9.0,      # H
        'carriage_screw_dW'    : 11.0,     # J
        'carriage_screw_dL'    : 9.50,     # K
        'slide_base_length'    : 13.25,    # L
        'slide_screw_size'     : 0.25,     # M
        'carriage_screw_size'  : 0.25,     # N
        'slide_tolerance'      : 0.005,
        }

bearing_params = {
        'RAB4'  : RAB4_params,
        'RAB6'  : RAB6_params,
        'RAB10' : RAB10_params,
        }

class AirBearing(csg.Union):
    """
    Creates a model of the RAB air bearings.
    """

    def __init__(self,bearing_type,slide_travel,slide_color=None,carriage_color=None):
        super(AirBearing, self).__init__()
        self.bearing_type = bearing_type
        self.params = bearing_params[bearing_type]
        self.params['bearing_slide_travel'] = slide_travel
        self.slide_color = slide_color
        self.carriage_color = carriage_color
        self.__make_slide()
        self.__make_carriage()
        self.__make_slide_travel()
        self.set_obj_list([self.slide,self.carriage,self.slide_travel])

    def set_slide_travel(self,val):
        self.params['bearing_slide_travel'] = val
        self.__make_slide()
        self.__make_carriage()
        self.__make_slide_travel()
        self.set_obj_list([self.slide,self.carriage,self.slide_travel])

    def __make_slide(self):
        """
        Creates the slide component of the RAB air bearing.
        """
        # Create base rectangle for slide
        length = self.params['slide_base_length'] + self.params['bearing_slide_travel']
        width = self.params['slide_width']
        height = self.params['slide_height']
        slide = fso.Box(x=length,y=width,z=height)
        # Create the mounting holes
        radius = 0.5*self.params['slide_screw_size']
        base_hole = fso.Cylinder(r=radius, l=2*height)
        hole_list = []
        for i in (-1,1):
            for j in (-1,1):
                xpos = i*(0.5*length - self.params['slide_screw_inset'])
                ypos = j*(0.5*self.params['slide_screw_dW'])
                hole = base_hole.copy()
                hole.translate([xpos,ypos,0])
                hole_list.append(hole)
        # Remove hole material
        slide -= hole_list
        # Add color to slide if available
        if not self.slide_color is None:
            slide.set_color(self.slide_color)
        self.slide = slide

    def __make_carriage(self):
        """
        Creates the carriage component of the RAB air bearing.
        """
        # Create base rectangle
        length = self.params['carriage_length']
        width = self.params['carriage_width']
        height = self.params['carriage_height']
        carriage = fso.Box(x=length, y=width, z=height)

        # Subtract slide from carraige
        slide_width = self.params['slide_width'] + 2*self.params['slide_tolerance']
        slide_height  = self.params['slide_height'] + 2*self.params['slide_tolerance']
        slide_negative = fso.Box(x=2*length, y=slide_width, z=slide_height)
        carriage = carriage - slide_negative

        # Create mounting holes
        radius = 0.5*self.params['carriage_screw_size']
        base_hole = fso.Cylinder(r=radius,l=2*height)
        hole_list = []
        for i in (-1,1):
            for j in (-1,1):
                xpos = i*0.5*self.params['carriage_screw_dL']
                ypos = j*0.5*self.params['carriage_screw_dW']
                hole = base_hole.copy()
                hole.translate([xpos,ypos,0])
                hole_list.append(hole)
        # Remove hole material
        print hole_list
        carriage -= hole_list
        # Add color to carriage is available
        if not self.carriage_color is None:
            carriage.set_color(self.carriage_color)
        self.carriage = carriage

    def __make_slide_travel(self,color=[0,0,1,1]):
        """
        Make a colored region showing the slides travel.
        """
        length = self.params['carriage_width'] + self.params['bearing_slide_travel']
        width = self.params['slide_width'] + self.params['slide_tolerance']
        height = self.params['slide_height'] +  self.params['slide_tolerance']
        slide_travel = fso.Box(x=length,y=width,z=height)
        slide_travel.set_color(color)
        self.slide_travel = slide_travel


# ---------------------------------------------------------------------
if __name__ == '__main__':

    bearing_type = 'RAB6'
    slide_travel = 4

    bearing = AirBearing(bearing_type, slide_travel, slide_color=[0.3,0.3,1,1],carriage_color=[1.0,0.3,0.3,1])
    obj_list = bearing.get_obj_list()
    for obj in obj_list:
        print obj.get_obj_list()
    bearing.export()