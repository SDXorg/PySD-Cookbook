
"""
Python model ../../models/Capability_Trap/Capability Trap.py
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
    'Investment in Capability': 'investment_in_capability',
    'Stretch': 'stretch',
    'Pressure to Improve Capability': 'pressure_to_improve_capability',
    'TIME STEP': 'time_step',
    'Normal Time Spent Working': 'normal_time_spent_working',
    'SAVEPER': 'saveper',
    'Improve Capability Adjustment Time': 'improve_capability_adjustment_time',
    'Influence of Capability Pressure on Improvement Time': 'influence_of_capability_pressure_on_improvement_time',
    'Actual Performance': 'actual_performance',
    'Erosion Timescale': 'erosion_timescale',
    'Change in Pressure to Do Work': 'change_in_pressure_to_do_work',
    'INITIAL TIME': 'initial_time',
    'FINAL TIME': 'final_time',
    'Capability improvement per investment': 'capability_improvement_per_investment',
    'Time Spent Working': 'time_spent_working',
    'Pressure Step': 'pressure_step',
    'Time Spend on Improvement': 'time_spend_on_improvement',
    'Work Harder Adjustment Time': 'work_harder_adjustment_time',
    'Capability Erosion': 'capability_erosion',
    'Influence of Work Pressure on Improvement Time': 'influence_of_work_pressure_on_improvement_time',
    'Change in Pressure to Improve Capability': 'change_in_pressure_to_improve_capability',
    'Capability': 'capability',
    'Pressure to Do Work': 'pressure_to_do_work',
    'Exogenous Capability Pressure': 'exogenous_capability_pressure',
    'Desired Performance': 'desired_performance',
    'Maximum Work Time': 'maximum_work_time',
    'Influence of Pressure on Work Time': 'influence_of_pressure_on_work_time',
    'Performance Step': 'performance_step',
    'Normal Time Spent on Improvement': 'normal_time_spent_on_improvement'}


def influence_of_work_pressure_on_improvement_time(x):
    """
    Influence of Work Pressure on Improvement Time
    ----------------------------------------------
    (influence_of_work_pressure_on_improvement_time)
    Dmnl

    """
    return functions.lookup(x, [0, 1, 1.5, 2, 5], [1, 1, 0.75, 0.25, 0])


@cache('step')
def time_spent_working():
    """
    Time Spent Working
    ------------------
    (time_spent_working)
    Person Hours/Week
    This formulation not quite correct, need to de-conflate the pressure to
                work from the time spent on improvement...
    """
    return np.minimum(
        normal_time_spent_working() *
        influence_of_pressure_on_work_time(
            pressure_to_do_work()),
        maximum_work_time() -
        time_spend_on_improvement())


@cache('step')
def change_in_pressure_to_do_work():
    """
    Change in Pressure to Do Work
    -----------------------------
    (change_in_pressure_to_do_work)
    1/Weeks

    """
    return (stretch() - pressure_to_do_work()) / work_harder_adjustment_time()


@cache('run')
def final_time():
    """
    FINAL TIME
    ----------
    (final_time)
    Week
    The final time for the simulation.
    """
    return 100


@cache('step')
def desired_performance():
    """
    Desired Performance
    -------------------
    (desired_performance)
    Widgets/Week

    """
    return 3000 + functions.step(performance_step(), 10)


def _init_pressure_to_improve_capability():
    """
    Implicit
    --------
    (_init_pressure_to_improve_capability)
    See docs for pressure_to_improve_capability
    Provides initial conditions for pressure_to_improve_capability function
    """
    return 1


@cache('step')
def exogenous_capability_pressure():
    """
    Exogenous Capability Pressure
    -----------------------------
    (exogenous_capability_pressure)


    """
    return functions.step(pressure_step(), 10)


@cache('step')
def change_in_pressure_to_improve_capability():
    """
    Change in Pressure to Improve Capability
    ----------------------------------------
    (change_in_pressure_to_improve_capability)
    1/Weeks

    """
    return (stretch() - pressure_to_improve_capability()
            ) / improve_capability_adjustment_time() + exogenous_capability_pressure()


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
def capability_improvement_per_investment():
    """
    Capability improvement per investment
    -------------------------------------
    (capability_improvement_per_investment)
    Widgets/Person Hour/Person Hour [0,5,0.25]

    """
    return 0.5


@cache('run')
def time_step():
    """
    TIME STEP
    ---------
    (time_step)
    Week [0,?]
    The time step for the simulation.
    """
    return 0.0625


@cache('run')
def maximum_work_time():
    """
    Maximum Work Time
    -----------------
    (maximum_work_time)
    Person Hours/Week [0,100,5]

    """
    return 40


@cache('step')
def stretch():
    """
    Stretch
    -------
    (stretch)
    Dmnl

    """
    return desired_performance() / actual_performance()


@cache('step')
def capability():
    """
    Capability
    ----------
    (capability)
    Widgets/Person Hour

    """
    return _state['capability']


@cache('run')
def performance_step():
    """
    Performance Step
    ----------------
    (performance_step)
    Widgets/Week [0,1000,50]

    """
    return 0


@cache('step')
def pressure_to_improve_capability():
    """
    Pressure to Improve Capability
    ------------------------------
    (pressure_to_improve_capability)
    Dmnl

    """
    return _state['pressure_to_improve_capability']


@cache('step')
def pressure_to_do_work():
    """
    Pressure to Do Work
    -------------------
    (pressure_to_do_work)
    Dmnl

    """
    return _state['pressure_to_do_work']


@cache('step')
def capability_erosion():
    """
    Capability Erosion
    ------------------
    (capability_erosion)
    Widgets/Person Hour/Week

    """
    return capability() / erosion_timescale()


def influence_of_pressure_on_work_time(x):
    """
    Influence of Pressure on Work Time
    ----------------------------------
    (influence_of_pressure_on_work_time)
    Dmnl

    """
    return functions.lookup(x, [0, 0.75, 1, 1.25, 2, 10], [0.75, 0.75, 1, 1.25, 1.5, 1.5])


def influence_of_capability_pressure_on_improvement_time(x):
    """
    Influence of Capability Pressure on Improvement Time
    ----------------------------------------------------
    (influence_of_capability_pressure_on_improvement_time)
    Dmnl

    """
    return functions.lookup(x, [0, 0.5, 0.75, 1, 2, 5], [0, 0, 0.5, 1, 1.5, 1.5])


@cache('run')
def normal_time_spent_working():
    """
    Normal Time Spent Working
    -------------------------
    (normal_time_spent_working)
    Person Hours/Week

    """
    return 30


def _init_capability():
    """
    Implicit
    --------
    (_init_capability)
    See docs for capability
    Provides initial conditions for capability function
    """
    return 100


@cache('run')
def work_harder_adjustment_time():
    """
    Work Harder Adjustment Time
    ---------------------------
    (work_harder_adjustment_time)
    Weeks

    """
    return 3


@cache('run')
def improve_capability_adjustment_time():
    """
    Improve Capability Adjustment Time
    ----------------------------------
    (improve_capability_adjustment_time)
    Weeks [0,50,1]

    """
    return 9


def _init_pressure_to_do_work():
    """
    Implicit
    --------
    (_init_pressure_to_do_work)
    See docs for pressure_to_do_work
    Provides initial conditions for pressure_to_do_work function
    """
    return 1


@cache('step')
def actual_performance():
    """
    Actual Performance
    ------------------
    (actual_performance)
    Widgets/Week

    """
    return capability() * time_spent_working()


@cache('step')
def _dcapability_dt():
    """
    Implicit
    --------
    (_dcapability_dt)
    See docs for capability
    Provides derivative for capability function
    """
    return investment_in_capability() - capability_erosion()


@cache('step')
def _dpressure_to_do_work_dt():
    """
    Implicit
    --------
    (_dpressure_to_do_work_dt)
    See docs for pressure_to_do_work
    Provides derivative for pressure_to_do_work function
    """
    return change_in_pressure_to_do_work()


@cache('step')
def _dpressure_to_improve_capability_dt():
    """
    Implicit
    --------
    (_dpressure_to_improve_capability_dt)
    See docs for pressure_to_improve_capability
    Provides derivative for pressure_to_improve_capability function
    """
    return change_in_pressure_to_improve_capability()


@cache('run')
def normal_time_spent_on_improvement():
    """
    Normal Time Spent on Improvement
    --------------------------------
    (normal_time_spent_on_improvement)
    Person Hours/Week

    """
    return 10


@cache('run')
def erosion_timescale():
    """
    Erosion Timescale
    -----------------
    (erosion_timescale)
    Weeks [0,50,1]

    """
    return 20


@cache('step')
def investment_in_capability():
    """
    Investment in Capability
    ------------------------
    (investment_in_capability)
    Widgets/Person Hour/Week

    """
    return time_spend_on_improvement() * capability_improvement_per_investment()


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


@cache('run')
def pressure_step():
    """
    Pressure Step
    -------------
    (pressure_step)
    [-0.05,0.1,0.01]

    """
    return 0


@cache('step')
def time_spend_on_improvement():
    """
    Time Spend on Improvement
    -------------------------
    (time_spend_on_improvement)
    Person Hours/Week

    """
    return normal_time_spent_on_improvement() * influence_of_capability_pressure_on_improvement_time(
        pressure_to_improve_capability()) * influence_of_work_pressure_on_improvement_time(pressure_to_do_work())


def time():
    return _t
functions.time = time
functions.initial_time = initial_time
