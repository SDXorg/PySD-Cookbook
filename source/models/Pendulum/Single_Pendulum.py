
from __future__ import division
import numpy as np
from pysd import functions

def time():
    return _t

# Share the `time` function with the module for `step`, `pulse`, etc.
functions.__builtins__.update({'time':time})


def acceleration_due_to_gravity():
    """
    
    """
    loc_dimension_dir = 0 
    output = -9.8

    return output

def angular_component_of_gravity():
    """
    
    """
    loc_dimension_dir = 0 
    output = force_of_gravity()*np.sin(angular_position())

    return output

def angular_position():
    return _state['angular_position']

def _angular_position_init():
    try:
        loc_dimension_dir = angular_position.dimension_dir
    except:
        loc_dimension_dir = 0
    return 1

def _dangular_position_dt():
    try:
        loc_dimension_dir = angular_position.dimension_dir
    except:
        loc_dimension_dir = 0
    return change_in_angular_position()

def angular_velocity():
    return _state['angular_velocity']

def _angular_velocity_init():
    try:
        loc_dimension_dir = angular_velocity.dimension_dir
    except:
        loc_dimension_dir = 0
    return 0

def _dangular_velocity_dt():
    try:
        loc_dimension_dir = angular_velocity.dimension_dir
    except:
        loc_dimension_dir = 0
    return change_in_angular_velocity()

def change_in_angular_position():
    """
    
    """
    loc_dimension_dir = 0 
    output = angular_velocity()

    return output

def change_in_angular_velocity():
    """
    
    """
    loc_dimension_dir = 0 
    output = torque()/pendulum_moment_of_inertia()

    return output

def force_of_gravity():
    """
    
    """
    loc_dimension_dir = 0 
    output = acceleration_due_to_gravity()*mass_of_pendulum()

    return output

def length_of_pendulum():
    """
    
    """
    loc_dimension_dir = 0 
    output = 10

    return output

def mass_of_pendulum():
    """
    
    """
    loc_dimension_dir = 0 
    output = 10

    return output

def pendulum_moment_of_inertia():
    """
    
    """
    loc_dimension_dir = 0 
    output = mass_of_pendulum()*length_of_pendulum()**2

    return output

def torque():
    """
    
    """
    loc_dimension_dir = 0 
    output = angular_component_of_gravity()*length_of_pendulum()

    return output

def final_time():
    """
    
    """
    loc_dimension_dir = 0 
    output = 100

    return output

def initial_time():
    """
    
    """
    loc_dimension_dir = 0 
    output = 0

    return output

def saveper():
    """
    
    """
    loc_dimension_dir = 0 
    output = 0.1

    return output

def time_step():
    """
    
    """
    loc_dimension_dir = 0 
    output = 0.0078125

    return output
