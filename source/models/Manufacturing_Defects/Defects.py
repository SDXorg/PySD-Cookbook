
"""
Python model ../../models/Manufacturing_Defects/Defects.py
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
    'INITIAL TIME': 'initial_time',
    'Defect Rate': 'defect_rate',
    'TIME STEP': 'time_step',
    'FINAL TIME': 'final_time',
    'SAVEPER': 'saveper',
    'Fulfillment Rate': 'fulfillment_rate',
    'Time allocated per unit': 'time_allocated_per_unit',
    'Influence of Backlog on Speed': 'influence_of_backlog_on_speed',
    'Length of workday': 'length_of_workday',
    'Backlog': 'backlog',
    'Arrival Rate': 'arrival_rate',
    'Influence of Backlog on Workday': 'influence_of_backlog_on_workday',
    'Number of Employees': 'number_of_employees'}


def _init_backlog():
    """
    Implicit
    --------
    (_init_backlog)
    See docs for backlog
    Provides initial conditions for backlog function
    """
    return 11.7


@cache('run')
def final_time():
    """
    FINAL TIME
    ----------
    (final_time)
    Day
    The final time for the simulation.
    """
    return 50


def influence_of_backlog_on_speed(x):
    """
    Influence of Backlog on Speed
    -----------------------------
    (influence_of_backlog_on_speed)


    """
    return functions.lookup(x, [0, 5, 10, 15, 20, 80], [0.1, 0.1, 0.09, 0.05, 0.04, 0.04])


@cache('step')
def length_of_workday():
    """
    Length of workday
    -----------------
    (length_of_workday)


    """
    return influence_of_backlog_on_workday(backlog())


def influence_of_backlog_on_workday(x):
    """
    Influence of Backlog on Workday
    -------------------------------
    (influence_of_backlog_on_workday)


    """
    return functions.lookup(x, [0, 2.76986, 5.53971, 10.3462, 13.1161, 16.5377, 20.5295, 60], [
                            0.1, 0.128571, 0.188095, 0.347619, 0.416667, 0.452381, 0.469048, 0.5])


@cache('step')
def defect_rate():
    """
    Defect Rate
    -----------
    (defect_rate)


    """
    return 0.01 * length_of_workday() / time_allocated_per_unit()


@cache('run')
def initial_time():
    """
    INITIAL TIME
    ------------
    (initial_time)
    Day
    The initial time for the simulation.
    """
    return 0


@cache('step')
def _dbacklog_dt():
    """
    Implicit
    --------
    (_dbacklog_dt)
    See docs for backlog
    Provides derivative for backlog function
    """
    return arrival_rate() - fulfillment_rate()


@cache('step')
def fulfillment_rate():
    """
    Fulfillment Rate
    ----------------
    (fulfillment_rate)


    """
    return number_of_employees() * length_of_workday() / time_allocated_per_unit() * (1 - defect_rate())


@cache('step')
def arrival_rate():
    """
    Arrival Rate
    ------------
    (arrival_rate)


    """
    return 10 + 12 * functions.pulse(20, 10)


@cache('run')
def time_step():
    """
    TIME STEP
    ---------
    (time_step)
    Day [0,?]
    The time step for the simulation.
    """
    return 0.015625


@cache('run')
def number_of_employees():
    """
    Number of Employees
    -------------------
    (number_of_employees)


    """
    return 2


@cache('step')
def time_allocated_per_unit():
    """
    Time allocated per unit
    -----------------------
    (time_allocated_per_unit)


    """
    return influence_of_backlog_on_speed(backlog())


@cache('step')
def backlog():
    """
    Backlog
    -------
    (backlog)


    """
    return _state['backlog']


@cache('step')
def saveper():
    """
    SAVEPER
    -------
    (saveper)
    Day [0,?]
    The frequency with which output is stored.
    """
    return time_step()


def time():
    return _t
functions.time = time
functions.initial_time = initial_time
