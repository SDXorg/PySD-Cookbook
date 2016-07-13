
"""
Python model ../../models/Climate/Atmospheric_Bathtub.py
Translated using PySD version 0.6.3
"""
from __future__ import division
import numpy as np
from pysd import utils
import xarray as xr

from pysd.functions import cache
from pysd import functions

_subscript_dict = {}

_namespace = {
    'INITIAL TIME': 'initial_time',
    'Removal Constant': 'removal_constant',
    'Natural Removal': 'natural_removal',
    'TIME STEP': 'time_step',
    'FINAL TIME': 'final_time',
    'SAVEPER': 'saveper',
    'Excess Atmospheric Carbon': 'excess_atmospheric_carbon',
    'Emissions': 'emissions'}


@cache('step')
def natural_removal():
    """
    Natural Removal
    ---------------
    (natural_removal)


    """
    return excess_atmospheric_carbon() * removal_constant()


@cache('step')
def _dexcess_atmospheric_carbon_dt():
    """
    Implicit
    --------
    (_dexcess_atmospheric_carbon_dt)
    See docs for excess_atmospheric_carbon
    Provides derivative for excess_atmospheric_carbon function
    """
    return emissions() - natural_removal()


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


@cache('run')
def removal_constant():
    """
    Removal Constant
    ----------------
    (removal_constant)


    """
    return 0.01


@cache('step')
def excess_atmospheric_carbon():
    """
    Excess Atmospheric Carbon
    -------------------------
    (excess_atmospheric_carbon)


    """
    return _state['excess_atmospheric_carbon']


def _init_excess_atmospheric_carbon():
    """
    Implicit
    --------
    (_init_excess_atmospheric_carbon)
    See docs for excess_atmospheric_carbon
    Provides initial conditions for excess_atmospheric_carbon function
    """
    return 0


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
def emissions():
    """
    Emissions
    ---------
    (emissions)


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
    return 1


def time():
    return _t
functions.time = time
functions.initial_time = initial_time
