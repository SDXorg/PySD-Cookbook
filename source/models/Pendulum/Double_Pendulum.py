
"""
Python model ../../models/Pendulum/Double_Pendulum.py
Translated using PySD version 0.6.1
"""
from __future__ import division
import numpy as np
from pysd import utils
import xarray as xr

from pysd.functions import cache
from pysd import functions

_subscript_dict = {}

_namespace = {
    'Mass of Pendulum2': 'mass_of_pendulum2', 'INITIAL TIME': 'initial_time',
    'FINAL TIME': 'final_time', 'Angular Position2': 'angular_position2',
    'Angular Position': 'angular_position', 'TIME STEP': 'time_step',
    'Angular Velocity': 'angular_velocity',
    'Change in Angular Position': 'change_in_angular_position',
    'Change in Angular Velocity': 'change_in_angular_velocity',
    'Change in Angular Position2': 'change_in_angular_position2',
    'Angular Velocity2': 'angular_velocity2', 'SAVEPER': 'saveper',
    'Length of Pendulum2': 'length_of_pendulum2',
    'Change in Angular Velocity2': 'change_in_angular_velocity2',
    'Mass of Pendulum': 'mass_of_pendulum',
    'Acceleration due to Gravity': 'acceleration_due_to_gravity',
    'Length of Pendulum': 'length_of_pendulum'}


@cache('run')
def final_time():
    """
    FINAL TIME
    ----------
    (final_time)
    Second
    The final time for the simulation.
    """
    return 100


@cache('run')
def initial_time():
    """
    INITIAL TIME
    ------------
    (initial_time)
    Second
    The initial time for the simulation.
    """
    return 0


@cache('run')
def time_step():
    """
    TIME STEP
    ---------
    (time_step)
    Second [0,?]
    The time step for the simulation.
    """
    return 0.0078125


@cache('step')
def _dangular_velocity2_dt():
    """
    Implicit
    --------
    (_dangular_velocity2_dt)
    See docs for angular_velocity2
    Provides derivative for angular_velocity2 function
    """
    return change_in_angular_velocity2()


@cache('step')
def change_in_angular_position():
    """
    Change in Angular Position
    --------------------------
    (change_in_angular_position)


    """
    return angular_velocity()


@cache('step')
def angular_position():
    """
    Angular Position
    ----------------
    (angular_position)
    radians
    Angle between the pendulum and vertical
    """
    return _state['angular_position']


@cache('run')
def length_of_pendulum():
    """
    Length of Pendulum
    ------------------
    (length_of_pendulum)
    Meter

    """
    return 10


def _init_angular_velocity():
    """
    Implicit
    --------
    (_init_angular_velocity)
    See docs for angular_velocity
    Provides initial conditions for angular_velocity function
    """
    return 0


@cache('step')
def angular_velocity2():
    """
    Angular Velocity2
    -----------------
    (angular_velocity2)


    """
    return _state['angular_velocity2']


@cache('step')
def change_in_angular_velocity2():
    """
    Change in Angular Velocity2
    ---------------------------
    (change_in_angular_velocity2)


    """
    return (2 * np.sin(angular_position() - angular_position2()) * (angular_velocity()**2 * length_of_pendulum() * (mass_of_pendulum() + mass_of_pendulum2()) + acceleration_due_to_gravity() * (mass_of_pendulum() + mass_of_pendulum2()) * np.cos(angular_position()) + angular_velocity2()
                                                                    ** 2 * length_of_pendulum2() * mass_of_pendulum2() * np.cos(angular_position() - angular_position2()))) / (length_of_pendulum2() * (2 * mass_of_pendulum() + mass_of_pendulum2() - mass_of_pendulum2() * np.cos(2 * angular_position() - 2 * angular_position2())))


@cache('run')
def acceleration_due_to_gravity():
    """
    Acceleration due to Gravity
    ---------------------------
    (acceleration_due_to_gravity)
    Meters/Second/Second

    """
    return -9.8


@cache('step')
def angular_position2():
    """
    Angular Position2
    -----------------
    (angular_position2)
    radians
    http://www.myphysicslab.com/dbl_pendulum.html
    """
    return _state['angular_position2']


def _init_angular_velocity2():
    """
    Implicit
    --------
    (_init_angular_velocity2)
    See docs for angular_velocity2
    Provides initial conditions for angular_velocity2 function
    """
    return 0


@cache('step')
def angular_velocity():
    """
    Angular Velocity
    ----------------
    (angular_velocity)


    """
    return _state['angular_velocity']


@cache('step')
def _dangular_position2_dt():
    """
    Implicit
    --------
    (_dangular_position2_dt)
    See docs for angular_position2
    Provides derivative for angular_position2 function
    """
    return change_in_angular_position2()


@cache('run')
def mass_of_pendulum2():
    """
    Mass of Pendulum2
    -----------------
    (mass_of_pendulum2)
    Kilogram

    """
    return 10


def _init_angular_position2():
    """
    Implicit
    --------
    (_init_angular_position2)
    See docs for angular_position2
    Provides initial conditions for angular_position2 function
    """
    return 1


@cache('step')
def change_in_angular_velocity():
    """
    Change in Angular Velocity
    --------------------------
    (change_in_angular_velocity)

    If anything is worth doing, it's worth doing well.		This is not worth doing well.
    """
    return (
        acceleration_due_to_gravity() * (
            2 * mass_of_pendulum() + mass_of_pendulum2()) * np.sin(
            angular_position()) - mass_of_pendulum2() * acceleration_due_to_gravity() * np.sin(
                angular_position() - 2 * angular_position2()) - 2 * np.sin(
                    angular_position() - angular_position2()) * mass_of_pendulum2() * (
                        angular_velocity2()**2 * length_of_pendulum2() + angular_velocity()**2 * length_of_pendulum() * np.cos(
                            angular_position() - angular_position2()))) / (
                                length_of_pendulum() * (
                                    2 * mass_of_pendulum() + mass_of_pendulum2() - mass_of_pendulum2() * np.cos(
                                        2 * angular_position() - 2 * angular_position2())))


@cache('step')
def _dangular_position_dt():
    """
    Implicit
    --------
    (_dangular_position_dt)
    See docs for angular_position
    Provides derivative for angular_position function
    """
    return change_in_angular_position()


def _init_angular_position():
    """
    Implicit
    --------
    (_init_angular_position)
    See docs for angular_position
    Provides initial conditions for angular_position function
    """
    return 1


@cache('run')
def length_of_pendulum2():
    """
    Length of Pendulum2
    -------------------
    (length_of_pendulum2)
    Meter

    """
    return 10


@cache('run')
def saveper():
    """
    SAVEPER
    -------
    (saveper)
    Second [0,?]
    The frequency with which output is stored.
    """
    return 0.1


@cache('run')
def mass_of_pendulum():
    """
    Mass of Pendulum
    ----------------
    (mass_of_pendulum)
    Kilogram

    """
    return 10


@cache('step')
def _dangular_velocity_dt():
    """
    Implicit
    --------
    (_dangular_velocity_dt)
    See docs for angular_velocity
    Provides derivative for angular_velocity function
    """
    return change_in_angular_velocity()


@cache('step')
def change_in_angular_position2():
    """
    Change in Angular Position2
    ---------------------------
    (change_in_angular_position2)


    """
    return angular_velocity2()


def time():
    return _t
functions.time = time
functions.initial_time = initial_time
