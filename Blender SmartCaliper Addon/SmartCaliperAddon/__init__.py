# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTIBILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

bl_info = {
    "name" : "Smart Caliper",
    "author" : "Jingzhou Liu, Ritvik Singh",
    "description" : "After a part is manufactured, it is common practice to use a caliper to measure the dimensions of that part to determine its tolerance and errors introduced during the manufacturing process. In order to determine the part’s tolerance, it is required to compare the manufactured part with its original 3D CAD model. To make this process faster and more intuitive, our software package includes a functionality that enables the user to input the measured dimensions and make any annotations directly onto the 3D CAD model. The user is able to view the original 3D CAD model in our software, then click on any two vertices/faces of the 3D model to generate a dimension the user wants to comment on. The software then stores any user-inputted comments, computes and logs the intended original dimension, and prompts the user to enter the part’s actual measured dimension. Similar to Part 1, the user simply needs to click one button on the SmartCaliper to transfer the measure dimension into the software without the need to type. The user can make as many of these annotations as they desire and all of that information is saved directly as comments in the 3D CAD model. By doing so, the user can use the software to load the 3D CAD model along with all of the saved annotations if the user wants to edit or append new annotations in the future.",
    "blender" : (2, 80, 0),
    
    "version" : (0, 0, 1),
    "location" : "View3D",
    "warning" : "",
    "category" : "Generic"
}

import bpy
from . Custom_Operators import *
from . Custom_Panels import *


classes = (Add_Engineering_Annotation, 
        Load_Engineering_Annotations, 
        Save_Engineering_Annotation, 
        Measure,
        Eng_Anno_Panel)


register, unregister = bpy.utils.register_classes_factory(classes)



