
"""
Python model ../../models/Roessler_Chaos/roessler_chaos.py
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
    'a': 'a',
    'dydt': 'dydt',
    'c': 'c',
    'b': 'b',
    'FINAL TIME': 'final_time',
    'TIME STEP': 'time_step',
    'SAVEPER': 'saveper',
    'dzdt': 'dzdt',
    'y': 'y',
    'INITIAL TIME': 'initial_time',
    'dxdt': 'dxdt',
    'x': 'x',
    'z': 'z'}


@cache('run')
def a():
    """
    a
    -
    (a)


    """
    return 0.2


@cache('step')
def dydt():
    """
    dydt
    ----
    (dydt)


    """
    return x() + a() * y()


@cache('run')
def c():
    """
    c
    -
    (c)


    """
    return 5.7


@cache('run')
def b():
    """
    b
    -
    (b)


    """
    return 0.2


@cache('step')
def _dy_dt():
    """
    Implicit
    --------
    (_dy_dt)
    See docs for y
    Provides derivative for y function
    """
    return dydt()


@cache('run')
def final_time():
    """
    FINAL TIME
    ----------
    (final_time)
    Month
    The final time for the simulation.
    """
    return 100


def _init_z():
    """
    Implicit
    --------
    (_init_z)
    See docs for z
    Provides initial conditions for z function
    """
    return 0.4


@cache('step')
def _dz_dt():
    """
    Implicit
    --------
    (_dz_dt)
    See docs for z
    Provides derivative for z function
    """
    return dzdt()


@cache('step')
def dzdt():
    """
    dzdt
    ----
    (dzdt)


    """
    return b() + z() * (x() - c())


def _init_x():
    """
    Implicit
    --------
    (_init_x)
    See docs for x
    Provides initial conditions for x function
    """
    return 0.5


@cache('step')
def _dx_dt():
    """
    Implicit
    --------
    (_dx_dt)
    See docs for x
    Provides derivative for x function
    """
    return dxdt()


@cache('step')
def y():
    """
    y
    -
    (y)


    """
    return _state['y']


def _init_y():
    """
    Implicit
    --------
    (_init_y)
    See docs for y
    Provides initial conditions for y function
    """
    return 0.5


@cache('step')
def saveper():
    """
    SAVEPER
    -------
    (saveper)
    Month [0,?]
    The frequency with which output is stored.
    """
    return time_step()


@cache('run')
def initial_time():
    """
    INITIAL TIME
    ------------
    (initial_time)
    Month
    The initial time for the simulation.
    """
    return 0


@cache('run')
def time_step():
    """
    TIME STEP
    ---------
    (time_step)
    Month [0,?]
    The time step for the simulation.
    """
    return 0.03125


@cache('step')
def dxdt():
    """
    dxdt
    ----
    (dxdt)


    """
    return -y() - z()


@cache('step')
def x():
    """
    x
    -
    (x)


    """
    return _state['x']


@cache('step')
def z():
    """
    z
    -
    (z)


    """
    return _state['z']


def time():
    return _t
functions.time = time
functions.initial_time = initial_time
