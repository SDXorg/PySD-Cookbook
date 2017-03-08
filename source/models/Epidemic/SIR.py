
"""
Python model ../../models/Epidemic/SIR.py
Translated using PySD version 0.6.4
"""
from __future__ import division
import numpy as np
from pysd import utils
import xarray as xr

from pysd.functions import cache
from pysd import functions

_subscript_dict = {}

_namespace = {
    'Total Population': 'total_population',
    'Recovery': 'recovery',
    'FINAL TIME': 'final_time',
    'Susceptible': 'susceptible',
    'TIME STEP': 'time_step',
    'TIME': 'time',
    'SAVEPER': 'saveper',
    'Contact Rate': 'contact_rate',
    'Initial Infected': 'initial_infected',
    'Infectivity': 'infectivity',
    'INITIAL TIME': 'initial_time',
    'Initial Susceptible': 'initial_susceptible',
    'Infection': 'infection',
    'Period of Infection': 'period_of_infection',
    'Time': 'time',
    'Infected': 'infected',
    'Recovered': 'recovered'}


@cache('run')
def period_of_infection():
    """
    Period of Infection
    -------------------
    (period_of_infection)
    Days

    """
    return 10


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


@cache('run')
def infectivity():
    """
    Infectivity
    -----------
    (infectivity)
    Persons/Contact

    """
    return 0.02


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
def initial_infected():
    """
    Initial Infected
    ----------------
    (initial_infected)


    """
    return 10


@cache('run')
def time_step():
    """
    TIME STEP
    ---------
    (time_step)
    Day [0,?]
    The time step for the simulation.
    """
    return 0.0625


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
    Total Population
    ----------------
    (total_population)
    Persons

    """
    return 1e+07


@cache('step')
def _dinfected_dt():
    """
    Implicit
    --------
    (_dinfected_dt)
    See docs for infected
    Provides derivative for infected function
    """
    return infection() - recovery()


@cache('run')
def contact_rate():
    """
    Contact Rate
    ------------
    (contact_rate)
    Contacts/Person/Day

    """
    return 25


@cache('step')
def susceptible():
    """
    Susceptible
    -----------
    (susceptible)
    Persons

    """
    return _state['susceptible']


@cache('step')
def initial_susceptible():
    """
    Initial Susceptible
    -------------------
    (initial_susceptible)


    """
    return total_population() - initial_infected()


@cache('step')
def infected():
    """
    Infected
    --------
    (infected)
    Persons

    """
    return _state['infected']


@cache('step')
def _dsusceptible_dt():
    """
    Implicit
    --------
    (_dsusceptible_dt)
    See docs for susceptible
    Provides derivative for susceptible function
    """
    return -infection()


@cache('step')
def recovered():
    """
    Recovered
    ---------
    (recovered)
    Persons

    """
    return _state['recovered']


@cache('step')
def infection():
    """
    Infection
    ---------
    (infection)
    Persons/Day

    """
    return susceptible() * contact_rate() * (infected() / total_population()) * infectivity()


@cache('step')
def recovery():
    """
    Recovery
    --------
    (recovery)
    Persons/Day

    """
    return infected() / period_of_infection()


def _init_infected():
    """
    Implicit
    --------
    (_init_infected)
    See docs for infected
    Provides initial conditions for infected function
    """
    return 10


@cache('step')
def _drecovered_dt():
    """
    Implicit
    --------
    (_drecovered_dt)
    See docs for recovered
    Provides derivative for recovered function
    """
    return recovery()


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
    return initial_susceptible()


@cache('step')
def time():
    """
    TIME
    ----
    (time)
    None
    The time of the model
    """
    return _t


def time():
    return _t
functions.time = time
functions.initial_time = initial_time
