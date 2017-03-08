
"""
Python model Goldstone_Tilly_2001.py
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
    'Repression fractional adjustment': 'repression_fractional_adjustment',
    'Cost of protest C': 'cost_of_protest_c',
    'Making concessions': 'making_concessions',
    'Concessions': 'concessions',
    'Current threat Tc': 'current_threat_tc',
    'TIME STEP': 'time_step',
    'Adjusting concession expectation': 'adjusting_concession_expectation',
    'Gains that would result from success V': 'gains_that_would_result_from_success_v',
    'Threat rate': 'threat_rate',
    'SAVEPER': 'saveper',
    'Concession unit cost': 'concession_unit_cost',
    'INITIAL TIME': 'initial_time',
    'Probability of success O': 'probability_of_success_o',
    'FINAL TIME': 'final_time',
    'Expected net gain from protest G': 'expected_net_gain_from_protest_g',
    'Concession rate': 'concession_rate',
    'Making threats': 'making_threats',
    'Preference for Repression': 'preference_for_repression',
    'Strength of nonstate allies k3': 'strength_of_nonstate_allies_k3',
    'Adjusting repression expectation': 'adjusting_repression_expectation',
    'Regime Survival': 'regime_survival',
    'Expectation of repression needed': 'expectation_of_repression_needed',
    'Initial level of current threat': 'initial_level_of_current_threat',
    'Repressive threat Tr': 'repressive_threat_tr',
    'Expectation of concessions needed': 'expectation_of_concessions_needed',
    'Regime capability': 'regime_capability',
    'Repression unit cost': 'repression_unit_cost',
    'Concession fractional adjustment': 'concession_fractional_adjustment',
    'Total cost': 'total_cost',
    'Popular support k2': 'popular_support_k2',
    'New advantages A': 'new_advantages_a',
    'Protest': 'protest',
    'State weakness k1': 'state_weakness_k1'}


@cache('step')
def current_threat_tc():
    """
    Current threat Tc
    -----------------
    (current_threat_tc)


    """
    return initial_level_of_current_threat() - concessions()


@cache('run')
def strength_of_nonstate_allies_k3():
    """
    Strength of nonstate allies k3
    ------------------------------
    (strength_of_nonstate_allies_k3)


    """
    return 0.1667


@cache('run')
def initial_level_of_current_threat():
    """
    Initial level of current threat
    -------------------------------
    (initial_level_of_current_threat)
    [0,5,0.125]

    """
    return 1


@cache('run')
def final_time():
    """
    FINAL TIME
    ----------
    (final_time)
    Month
    The final time for the simulation.
    """
    return 10


@cache('run')
def repression_fractional_adjustment():
    """
    Repression fractional adjustment
    --------------------------------
    (repression_fractional_adjustment)


    """
    return 1


@cache('run')
def regime_capability():
    """
    Regime capability
    -----------------
    (regime_capability)


    """
    return 10


@cache('run')
def state_weakness_k1():
    """
    State weakness k1
    -----------------
    (state_weakness_k1)

    'The probability of success depends on state weakness (for example, fiscal problems,
                elite divisions, military defeat)' pg 184		'In the short run, the group and the state probably can do little about state
                weakness, which depends on structural conditions or events, such as
                financial weakness, elite divisions, or military defeat.' pg 185				'Weak repression or concessions can increase perceptions of state
                weakness.' pg 189
    """
    return 0.1666


@cache('step')
def expectation_of_concessions_needed():
    """
    Expectation of concessions needed
    ---------------------------------
    (expectation_of_concessions_needed)


    """
    return _state['expectation_of_concessions_needed']


@cache('step')
def protest():
    """
    Protest
    -------
    (protest)


    """
    return functions.if_then_else(expected_net_gain_from_protest_g() > 0, 1, 0)


@cache('run')
def concession_unit_cost():
    """
    Concession unit cost
    --------------------
    (concession_unit_cost)


    """
    return 1


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


@cache('step')
def adjusting_repression_expectation():
    """
    Adjusting repression expectation
    --------------------------------
    (adjusting_repression_expectation)


    """
    return functions.if_then_else(
        protest() > 0,
        repressive_threat_tr() *
        repression_fractional_adjustment() -
        expectation_of_repression_needed(),
        0)


@cache('run')
def concession_fractional_adjustment():
    """
    Concession fractional adjustment
    --------------------------------
    (concession_fractional_adjustment)


    """
    return 1


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
def _dconcessions_dt():
    """
    Implicit
    --------
    (_dconcessions_dt)
    See docs for concessions
    Provides derivative for concessions function
    """
    return making_concessions()


@cache('step')
def preference_for_repression():
    """
    Preference for Repression
    -------------------------
    (preference_for_repression)


    """
    return (expectation_of_concessions_needed() * concession_unit_cost() - expectation_of_repression_needed()
            * repression_unit_cost()) / (expectation_of_repression_needed() * repression_unit_cost())


@cache('run')
def popular_support_k2():
    """
    Popular support k2
    ------------------
    (popular_support_k2)


    """
    return 0.1667


@cache('step')
def cost_of_protest_c():
    """
    Cost of protest C
    -----------------
    (cost_of_protest_c)


    """
    return repressive_threat_tr()


def _init_expectation_of_concessions_needed():
    """
    Implicit
    --------
    (_init_expectation_of_concessions_needed)
    See docs for expectation_of_concessions_needed
    Provides initial conditions for expectation_of_concessions_needed function
    """
    return 1


@cache('run')
def repression_unit_cost():
    """
    Repression unit cost
    --------------------
    (repression_unit_cost)


    """
    return 1


@cache('step')
def total_cost():
    """
    Total cost
    ----------
    (total_cost)


    """
    return concessions() * concession_unit_cost() + repressive_threat_tr() * repression_unit_cost()


@cache('step')
def expected_net_gain_from_protest_g():
    """
    Expected net gain from protest G
    --------------------------------
    (expected_net_gain_from_protest_g)

    Pg 184:		This fonnula involves yet another simplification - that the costs of
                repression do not depend on the chances for success. In some cases, this
                is clearly false - those leading a rebellion are likely to suffer far
                greater costs if the rebellion fails than if it succeeds. However, if we
                focus on the ordinary protestor, say the person who helped defend the
                Russian Parliament in 1991, or the civil rights protestor who risks a
                beating or arrest, for them the eventual result days or weeks later will
                not change whether a bullet finds them on the barricade, or lighten the
                beating, or avoid the arrest. For them, the immediate risks involved with
                the act of protest itself are what counts - which is to say that leaders
                and followers may have a separate calculus of prospective gains and risks,
                with both being much greater for those in charge.
    """
    return (gains_that_would_result_from_success_v()
            * probability_of_success_o()) - cost_of_protest_c()


@cache('step')
def gains_that_would_result_from_success_v():
    """
    Gains that would result from success V
    --------------------------------------
    (gains_that_would_result_from_success_v)

    pg 184		new advantages obtained or current or prospective harms avoided
    """
    return new_advantages_a() + current_threat_tc()


@cache('step')
def regime_survival():
    """
    Regime Survival
    ---------------
    (regime_survival)


    """
    return functions.if_then_else(total_cost() < regime_capability(), 1, 0)


@cache('step')
def repressive_threat_tr():
    """
    Repressive threat Tr
    --------------------
    (repressive_threat_tr)


    """
    return _state['repressive_threat_tr']


@cache('step')
def making_threats():
    """
    Making threats
    --------------
    (making_threats)


    """
    return functions.if_then_else(
        protest() > 0, functions.if_then_else(
            preference_for_repression() >= 0, threat_rate(), 0), 0)


def _init_repressive_threat_tr():
    """
    Implicit
    --------
    (_init_repressive_threat_tr)
    See docs for repressive_threat_tr
    Provides initial conditions for repressive_threat_tr function
    """
    return 1


def _init_concessions():
    """
    Implicit
    --------
    (_init_concessions)
    See docs for concessions
    Provides initial conditions for concessions function
    """
    return 0


@cache('step')
def probability_of_success_o():
    """
    Probability of success O
    ------------------------
    (probability_of_success_o)


    """
    return state_weakness_k1() + popular_support_k2() + strength_of_nonstate_allies_k3()


def _init_expectation_of_repression_needed():
    """
    Implicit
    --------
    (_init_expectation_of_repression_needed)
    See docs for expectation_of_repression_needed
    Provides initial conditions for expectation_of_repression_needed function
    """
    return 1


@cache('step')
def making_concessions():
    """
    Making concessions
    ------------------
    (making_concessions)


    """
    return functions.if_then_else(
        protest() > 0,
        functions.if_then_else(
            preference_for_repression() < 0,
            concession_rate(),
            0),
        0)


@cache('step')
def expectation_of_repression_needed():
    """
    Expectation of repression needed
    --------------------------------
    (expectation_of_repression_needed)


    """
    return _state['expectation_of_repression_needed']


@cache('step')
def _drepressive_threat_tr_dt():
    """
    Implicit
    --------
    (_drepressive_threat_tr_dt)
    See docs for repressive_threat_tr
    Provides derivative for repressive_threat_tr function
    """
    return making_threats()


@cache('run')
def concession_rate():
    """
    Concession rate
    ---------------
    (concession_rate)


    """
    return 1


@cache('run')
def new_advantages_a():
    """
    New advantages A
    ----------------
    (new_advantages_a)
    [0,5,0.125]

    """
    return 1


@cache('step')
def _dexpectation_of_concessions_needed_dt():
    """
    Implicit
    --------
    (_dexpectation_of_concessions_needed_dt)
    See docs for expectation_of_concessions_needed
    Provides derivative for expectation_of_concessions_needed function
    """
    return adjusting_concession_expectation()


@cache('run')
def threat_rate():
    """
    Threat rate
    -----------
    (threat_rate)


    """
    return 1


@cache('step')
def concessions():
    """
    Concessions
    -----------
    (concessions)


    """
    return _state['concessions']


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


@cache('step')
def _dexpectation_of_repression_needed_dt():
    """
    Implicit
    --------
    (_dexpectation_of_repression_needed_dt)
    See docs for expectation_of_repression_needed
    Provides derivative for expectation_of_repression_needed function
    """
    return adjusting_repression_expectation()


@cache('step')
def adjusting_concession_expectation():
    """
    Adjusting concession expectation
    --------------------------------
    (adjusting_concession_expectation)


    """
    return functions.if_then_else(
        protest() > 0,
        concessions() *
        concession_fractional_adjustment() -
        expectation_of_concessions_needed(),
        0)


def time():
    return _t
functions.time = time
functions.initial_time = initial_time
