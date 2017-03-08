
"""
Python model ../../models/Epidemic/SI.py
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
    'TIME STEP': 'time_step',
    'Total Population': 'total_population',
    'FINAL TIME': 'final_time',
    'Contact Frequency': 'contact_frequency',
    'Susceptible': 'susceptible',
    'Susceptible Contacts': 'susceptible_contacts',
    'TIME': 'time',
    'SAVEPER': 'saveper',
    'New Reported Cases': 'new_reported_cases',
    'Infectivity': 'infectivity',
    'Infection Rate': 'infection_rate',
    'Infected': 'infected',
    'Time': 'time',
    'Cumulative Reported Cases': 'cumulative_reported_cases',
    'Probability of Contact with Infected Person': 'probability_of_contact_with_infected_person',
    'Contacts Between Infected and Uninfected Persons': 'contacts_between_infected_and_uninfected_persons',
    'INITIAL TIME': 'initial_time'}


@cache('run')
def final_time():
    """
    FINAL TIME
    ----------
    (final_time)
    Week
    The final time for the simulation.
    """
    return 35


@cache('step')
def cumulative_reported_cases():
    """
    Cumulative Reported Cases
    -------------------------
    (cumulative_reported_cases)
    Persons

    """
    return _state['cumulative_reported_cases']


@cache('run')
def infectivity():
    """
    Infectivity
    -----------
    (infectivity)
    Dmnl [-1,1,0.001]

    """
    return 0.05


@cache('run')
def initial_time():
    """
    INITIAL TIME
    ------------
    (initial_time)
    Week
    The initial time for the simulation.
    """
    return 0


@cache('run')
def time_step():
    """
    TIME STEP
    ---------
    (time_step)
    Week [0,?]
    The time step for the simulation.
    """
    return 0.125


@cache('run')
def total_population():
    """
    Total Population
    ----------------
    (total_population)
    Persons

    """
    return 10000


@cache('step')
def _dinfected_dt():
    """
    Implicit
    --------
    (_dinfected_dt)
    See docs for infected
    Provides derivative for infected function
    """
    return infection_rate()


@cache('run')
def contact_frequency():
    """
    Contact Frequency
    -----------------
    (contact_frequency)
    Persons/Person/Week

    """
    return 7


@cache('step')
def susceptible():
    """
    Susceptible
    -----------
    (susceptible)
    Persons
    The Population Susceptible to Ebola is the equal to the population
                susceptible prior to the onset of the disease less all of those that have
                contracted it. It is initialized to the Total Effective Population.
    """
    return _state['susceptible']


def _init_cumulative_reported_cases():
    """
    Implicit
    --------
    (_init_cumulative_reported_cases)
    See docs for cumulative_reported_cases
    Provides initial conditions for cumulative_reported_cases function
    """
    return 0


@cache('step')
def _dcumulative_reported_cases_dt():
    """
    Implicit
    --------
    (_dcumulative_reported_cases_dt)
    See docs for cumulative_reported_cases
    Provides derivative for cumulative_reported_cases function
    """
    return new_reported_cases()


@cache('step')
def _dsusceptible_dt():
    """
    Implicit
    --------
    (_dsusceptible_dt)
    See docs for susceptible
    Provides derivative for susceptible function
    """
    return -infection_rate()


@cache('step')
def probability_of_contact_with_infected_person():
    """
    Probability of Contact with Infected Person
    -------------------------------------------
    (probability_of_contact_with_infected_person)
    Dmnl

    """
    return infected() / total_population()


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
def contacts_between_infected_and_uninfected_persons():
    """
    Contacts Between Infected and Uninfected Persons
    ------------------------------------------------
    (contacts_between_infected_and_uninfected_persons)
    Persons/Week

    """
    return probability_of_contact_with_infected_person() * susceptible_contacts()


@cache('step')
def new_reported_cases():
    """
    New Reported Cases
    ------------------
    (new_reported_cases)
    Persons/Week

    """
    return infection_rate()


@cache('step')
def susceptible_contacts():
    """
    Susceptible Contacts
    --------------------
    (susceptible_contacts)
    Persons/Week

    """
    return contact_frequency() * susceptible()


def _init_infected():
    """
    Implicit
    --------
    (_init_infected)
    See docs for infected
    Provides initial conditions for infected function
    """
    return 1


@cache('step')
def saveper():
    """
    SAVEPER
    -------
    (saveper)
    Week [0,?]
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
def time():
    """
    TIME
    ----
    (time)
    None
    The time of the model
    """
    return _t


@cache('step')
def infection_rate():
    """
    Infection Rate
    --------------
    (infection_rate)
    Persons/Week
    The infection rate is determined by the total number of contacts between
                infected and uninfected people each week (Contacts Between Infected and
                Uninfected Persons), and the probability that each such contact results in
                transmission from the infected to uninfected person (Infectivity).
    """
    return contacts_between_infected_and_uninfected_persons() * infectivity()


def time():
    return _t
functions.time = time
functions.initial_time = initial_time
