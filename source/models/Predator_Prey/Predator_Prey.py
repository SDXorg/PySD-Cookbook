
"""
Python model ../../models/Predator_Prey/Predator_Prey.py
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
    'Predator Mortality': 'predator_mortality',
    'TIME STEP': 'time_step',
    'INITIAL TIME': 'initial_time',
    'SAVEPER': 'saveper',
    'FINAL TIME': 'final_time',
    'Prey Fertility': 'prey_fertility',
    'Prey Population': 'prey_population',
    'Predation Rate': 'predation_rate',
    'Predator Population': 'predator_population',
    'Prey Births': 'prey_births',
    'Predator Food Driven Fertility': 'predator_food_driven_fertility',
    'Predator Deaths': 'predator_deaths',
    'Predator Births': 'predator_births',
    'Prey Deaths': 'prey_deaths'}


def _init_predator_population():
    """
    Implicit
    --------
    (_init_predator_population)
    See docs for predator_population
    Provides initial conditions for predator_population function
    """
    return 100


@cache('step')
def prey_population():
    """
    Prey Population
    ---------------
    (prey_population)
    Prey [0,?]

    """
    return _state['prey_population']


@cache('run')
def predator_food_driven_fertility():
    """
    Predator Food Driven Fertility
    ------------------------------
    (predator_food_driven_fertility)
    Predators/Day/Predator/Prey [0,0.0001,1e-06]

    """
    return 0.001


@cache('run')
def prey_fertility():
    """
    Prey Fertility
    --------------
    (prey_fertility)
    Prey/Day/Prey [0,10,0.1]

    """
    return 2


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
def predation_rate():
    """
    Predation Rate
    --------------
    (predation_rate)
    Prey/Day/Prey/Predator [0,0.0001,1e-05]

    """
    return 0.0001


@cache('step')
def predator_deaths():
    """
    Predator Deaths
    ---------------
    (predator_deaths)
    Predator/Day

    """
    return predator_mortality() * predator_population()


@cache('step')
def _dprey_population_dt():
    """
    Implicit
    --------
    (_dprey_population_dt)
    See docs for prey_population
    Provides derivative for prey_population function
    """
    return prey_births() - prey_deaths()


@cache('step')
def prey_deaths():
    """
    Prey Deaths
    -----------
    (prey_deaths)
    Prey/Day

    """
    return predation_rate() * prey_population() * predator_population()


def _init_prey_population():
    """
    Implicit
    --------
    (_init_prey_population)
    See docs for prey_population
    Provides initial conditions for prey_population function
    """
    return 250


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
def predator_births():
    """
    Predator Births
    ---------------
    (predator_births)
    Predator/Day

    """
    return predator_food_driven_fertility() * prey_population() * predator_population()


@cache('step')
def predator_population():
    """
    Predator Population
    -------------------
    (predator_population)
    Predators

    """
    return _state['predator_population']


@cache('step')
def _dpredator_population_dt():
    """
    Implicit
    --------
    (_dpredator_population_dt)
    See docs for predator_population
    Provides derivative for predator_population function
    """
    return predator_births() - predator_deaths()


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


@cache('step')
def prey_births():
    """
    Prey Births
    -----------
    (prey_births)
    Prey/Day

    """
    return prey_fertility() * prey_population()


@cache('run')
def predator_mortality():
    """
    Predator Mortality
    ------------------
    (predator_mortality)
    Predator/Day/Predator [0,1]

    """
    return 0.01


def time():
    return _t
functions.time = time
functions.initial_time = initial_time
