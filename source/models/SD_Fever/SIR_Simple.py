
"""
Python model ../../models/SD_Fever/SIR_Simple.py
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
    'total population': 'total_population',
    'contact infectivity': 'contact_infectivity',
    'susceptible': 'susceptible',
    'infect': 'infect',
    'TIME STEP': 'time_step',
    'SAVEPER': 'saveper',
    'infectious': 'infectious',
    'cumulative cases': 'cumulative_cases',
    'report case': 'report_case',
    'FINAL TIME': 'final_time',
    'recovery period': 'recovery_period',
    'recover': 'recover',
    'INITIAL TIME': 'initial_time',
    'recovered': 'recovered'}


def _init_cumulative_cases():
    """
    Implicit
    --------
    (_init_cumulative_cases)
    See docs for cumulative_cases
    Provides initial conditions for cumulative_cases function
    """
    return 0


@cache('run')
def final_time():
    """
    FINAL TIME
    ----------
    (final_time)
    Day
    The final time for the simulation.
    """
    return 100


@cache('run')
def contact_infectivity():
    """
    contact infectivity
    -------------------
    (contact_infectivity)
    Persons/Persons/Day
    A joint parameter listing both how many people you contact, and how likely
                you are to give them the disease.
    """
    return 0.7


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


@cache('run')
def time_step():
    """
    TIME STEP
    ---------
    (time_step)
    Day [0,?]
    The time step for the simulation.
    """
    return 0.5


@cache('step')
def recover():
    """
    recover
    -------
    (recover)
    Persons/Day

    """
    return infectious() / recovery_period()


def _init_recovered():
    """
    Implicit
    --------
    (_init_recovered)
    See docs for recovered
    Provides initial conditions for recovered function
    """
    return 0


@cache('run')
def total_population():
    """
    total population
    ----------------
    (total_population)
    Persons
    This is just a simplification to make it easer to track how many folks
                there are without having to sum up all the stocks.
    """
    return 1000


@cache('step')
def susceptible():
    """
    susceptible
    -----------
    (susceptible)
    Persons
    The population that has not yet been infected.
    """
    return _state['susceptible']


def _init_infectious():
    """
    Implicit
    --------
    (_init_infectious)
    See docs for infectious
    Provides initial conditions for infectious function
    """
    return 5


@cache('step')
def _dinfectious_dt():
    """
    Implicit
    --------
    (_dinfectious_dt)
    See docs for infectious
    Provides derivative for infectious function
    """
    return infect() - recover()


@cache('step')
def _dcumulative_cases_dt():
    """
    Implicit
    --------
    (_dcumulative_cases_dt)
    See docs for cumulative_cases
    Provides derivative for cumulative_cases function
    """
    return report_case()


@cache('step')
def _dsusceptible_dt():
    """
    Implicit
    --------
    (_dsusceptible_dt)
    See docs for susceptible
    Provides derivative for susceptible function
    """
    return -infect()


@cache('step')
def recovered():
    """
    recovered
    ---------
    (recovered)
    Persons
    These people have recovered from the disease. Yay! Nobody dies in this
                model.
    """
    return _state['recovered']


@cache('step')
def infect():
    """
    infect
    ------
    (infect)
    Persons/Day

    """
    return susceptible() * (infectious() / total_population()) * contact_infectivity()


@cache('step')
def cumulative_cases():
    """
    cumulative cases
    ----------------
    (cumulative_cases)


    """
    return _state['cumulative_cases']


@cache('run')
def recovery_period():
    """
    recovery period
    ---------------
    (recovery_period)
    Days
    How long are you infectious for?
    """
    return 5


@cache('step')
def infectious():
    """
    infectious
    ----------
    (infectious)
    Persons
    The population with the disease, manifesting symptoms, and able to
                transmit it to other people.
    """
    return _state['infectious']


@cache('step')
def _drecovered_dt():
    """
    Implicit
    --------
    (_drecovered_dt)
    See docs for recovered
    Provides derivative for recovered function
    """
    return recover()


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


def _init_susceptible():
    """
    Implicit
    --------
    (_init_susceptible)
    See docs for susceptible
    Provides initial conditions for susceptible function
    """
    return total_population()


@cache('step')
def report_case():
    """
    report case
    -----------
    (report_case)


    """
    return infect()


def time():
    return _t
functions.time = time
functions.initial_time = initial_time
