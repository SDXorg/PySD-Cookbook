"""
Python model 'Goldstone_Tilly_2001.py'
Translated using PySD
"""

from pathlib import Path
import numpy as np

from pysd.py_backend.functions import if_then_else
from pysd.py_backend.statefuls import Integ
from pysd import Component

__pysd_version__ = "3.7.0"

__data = {"scope": None, "time": lambda: 0}

_root = Path(__file__).parent


component = Component()

#######################################################################
#                          CONTROL VARIABLES                          #
#######################################################################

_control_vars = {
    "initial_time": lambda: 0,
    "final_time": lambda: 10,
    "time_step": lambda: 0.03125,
    "saveper": lambda: time_step(),
}


def _init_outer_references(data):
    for key in data:
        __data[key] = data[key]


@component.add(name="Time")
def time():
    """
    Current time of the model.
    """
    return __data["time"]()


@component.add(
    name="FINAL TIME", units="Month", comp_type="Constant", comp_subtype="Normal"
)
def final_time():
    """
    The final time for the simulation.
    """
    return __data["time"].final_time()


@component.add(
    name="INITIAL TIME", units="Month", comp_type="Constant", comp_subtype="Normal"
)
def initial_time():
    """
    The initial time for the simulation.
    """
    return __data["time"].initial_time()


@component.add(
    name="SAVEPER",
    units="Month",
    limits=(0.0, np.nan),
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"time_step": 1},
)
def saveper():
    """
    The frequency with which output is stored.
    """
    return __data["time"].saveper()


@component.add(
    name="TIME STEP",
    units="Month",
    limits=(0.0, np.nan),
    comp_type="Constant",
    comp_subtype="Normal",
)
def time_step():
    """
    The time step for the simulation.
    """
    return __data["time"].time_step()


#######################################################################
#                           MODEL VARIABLES                           #
#######################################################################


@component.add(
    name="Regime Survival",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"total_cost": 1, "regime_capability": 1},
)
def regime_survival():
    return if_then_else(total_cost() < regime_capability(), lambda: 1, lambda: 0)


@component.add(name="Regime capability", comp_type="Constant", comp_subtype="Normal")
def regime_capability():
    return 10


@component.add(
    name="Total cost",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "concessions": 1,
        "concession_unit_cost": 1,
        "repression_unit_cost": 1,
        "repressive_threat_tr": 1,
    },
)
def total_cost():
    return (
        concessions() * concession_unit_cost()
        + repressive_threat_tr() * repression_unit_cost()
    )


@component.add(
    name="Adjusting concession expectation",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "protest": 1,
        "expectation_of_concessions_needed": 1,
        "concession_fractional_adjustment": 1,
        "concessions": 1,
    },
)
def adjusting_concession_expectation():
    return if_then_else(
        protest() > 0,
        lambda: concessions() * concession_fractional_adjustment()
        - expectation_of_concessions_needed(),
        lambda: 0,
    )


@component.add(
    name="Adjusting repression expectation",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "protest": 1,
        "repression_fractional_adjustment": 1,
        "expectation_of_repression_needed": 1,
        "repressive_threat_tr": 1,
    },
)
def adjusting_repression_expectation():
    return if_then_else(
        protest() > 0,
        lambda: repressive_threat_tr() * repression_fractional_adjustment()
        - expectation_of_repression_needed(),
        lambda: 0,
    )


@component.add(
    name="Concession fractional adjustment", comp_type="Constant", comp_subtype="Normal"
)
def concession_fractional_adjustment():
    return 1


@component.add(name="Concession rate", comp_type="Constant", comp_subtype="Normal")
def concession_rate():
    return 1


@component.add(name="Concession unit cost", comp_type="Constant", comp_subtype="Normal")
def concession_unit_cost():
    return 1


@component.add(
    name="Concessions",
    comp_type="Stateful",
    comp_subtype="Integ",
    depends_on={"_integ_concessions": 1},
    other_deps={
        "_integ_concessions": {"initial": {}, "step": {"making_concessions": 1}}
    },
)
def concessions():
    return _integ_concessions()


_integ_concessions = Integ(
    lambda: making_concessions(), lambda: 0, "_integ_concessions"
)


@component.add(
    name="Expectation of concessions needed",
    comp_type="Stateful",
    comp_subtype="Integ",
    depends_on={"_integ_expectation_of_concessions_needed": 1},
    other_deps={
        "_integ_expectation_of_concessions_needed": {
            "initial": {},
            "step": {"adjusting_concession_expectation": 1},
        }
    },
)
def expectation_of_concessions_needed():
    return _integ_expectation_of_concessions_needed()


_integ_expectation_of_concessions_needed = Integ(
    lambda: adjusting_concession_expectation(),
    lambda: 1,
    "_integ_expectation_of_concessions_needed",
)


@component.add(
    name="Expectation of repression needed",
    comp_type="Stateful",
    comp_subtype="Integ",
    depends_on={"_integ_expectation_of_repression_needed": 1},
    other_deps={
        "_integ_expectation_of_repression_needed": {
            "initial": {},
            "step": {"adjusting_repression_expectation": 1},
        }
    },
)
def expectation_of_repression_needed():
    return _integ_expectation_of_repression_needed()


_integ_expectation_of_repression_needed = Integ(
    lambda: adjusting_repression_expectation(),
    lambda: 1,
    "_integ_expectation_of_repression_needed",
)


@component.add(
    name="Initial level of current threat",
    limits=(0.0, 5.0, 0.125),
    comp_type="Constant",
    comp_subtype="Normal",
)
def initial_level_of_current_threat():
    return 1


@component.add(
    name="Making concessions",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"protest": 1, "preference_for_repression": 1, "concession_rate": 1},
)
def making_concessions():
    return if_then_else(
        protest() > 0,
        lambda: if_then_else(
            preference_for_repression() < 0, lambda: concession_rate(), lambda: 0
        ),
        lambda: 0,
    )


@component.add(
    name="Making threats",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"protest": 1, "preference_for_repression": 1, "threat_rate": 1},
)
def making_threats():
    return if_then_else(
        protest() > 0,
        lambda: if_then_else(
            preference_for_repression() >= 0, lambda: threat_rate(), lambda: 0
        ),
        lambda: 0,
    )


@component.add(
    name="Preference for Repression",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "expectation_of_concessions_needed": 1,
        "concession_unit_cost": 1,
        "expectation_of_repression_needed": 2,
        "repression_unit_cost": 2,
    },
)
def preference_for_repression():
    return (
        expectation_of_concessions_needed() * concession_unit_cost()
        - expectation_of_repression_needed() * repression_unit_cost()
    ) / (expectation_of_repression_needed() * repression_unit_cost())


@component.add(
    name="Protest",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"expected_net_gain_from_protest_g": 1},
)
def protest():
    return if_then_else(expected_net_gain_from_protest_g() > 0, lambda: 1, lambda: 0)


@component.add(
    name="Repression fractional adjustment", comp_type="Constant", comp_subtype="Normal"
)
def repression_fractional_adjustment():
    return 1


@component.add(name="Repression unit cost", comp_type="Constant", comp_subtype="Normal")
def repression_unit_cost():
    return 1


@component.add(
    name="Repressive threat Tr",
    comp_type="Stateful",
    comp_subtype="Integ",
    depends_on={"_integ_repressive_threat_tr": 1},
    other_deps={
        "_integ_repressive_threat_tr": {"initial": {}, "step": {"making_threats": 1}}
    },
)
def repressive_threat_tr():
    return _integ_repressive_threat_tr()


_integ_repressive_threat_tr = Integ(
    lambda: making_threats(), lambda: 1, "_integ_repressive_threat_tr"
)


@component.add(name="Threat rate", comp_type="Constant", comp_subtype="Normal")
def threat_rate():
    return 1


@component.add(
    name="Cost of protest C",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"repressive_threat_tr": 1},
)
def cost_of_protest_c():
    return repressive_threat_tr()


@component.add(
    name="Current threat Tc",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"initial_level_of_current_threat": 1, "concessions": 1},
)
def current_threat_tc():
    return initial_level_of_current_threat() - concessions()


@component.add(
    name="Gains that would result from success V",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"new_advantages_a": 1, "current_threat_tc": 1},
)
def gains_that_would_result_from_success_v():
    """
    pg 184 new advantages obtained or current or prospective harms avoided
    """
    return new_advantages_a() + current_threat_tc()


@component.add(
    name="New advantages A",
    limits=(0.0, 5.0, 0.125),
    comp_type="Constant",
    comp_subtype="Normal",
)
def new_advantages_a():
    return 1


@component.add(name="Popular support k2", comp_type="Constant", comp_subtype="Normal")
def popular_support_k2():
    return 0.1667


@component.add(
    name="Probability of success O",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "state_weakness_k1": 1,
        "popular_support_k2": 1,
        "strength_of_nonstate_allies_k3": 1,
    },
)
def probability_of_success_o():
    return state_weakness_k1() + popular_support_k2() + strength_of_nonstate_allies_k3()


@component.add(
    name="Strength of nonstate allies k3", comp_type="Constant", comp_subtype="Normal"
)
def strength_of_nonstate_allies_k3():
    return 0.1667


@component.add(name="State weakness k1", comp_type="Constant", comp_subtype="Normal")
def state_weakness_k1():
    """
    'The probability of success depends on state weakness (for example, fiscal problems, elite divisions, military defeat)' pg 184 'In the short run, the group and the state probably can do little about state weakness, which depends on structural conditions or events, such as financial weakness, elite divisions, or military defeat.' pg 185 'Weak repression or concessions can increase perceptions of state weakness.' pg 189
    """
    return 0.1666


@component.add(
    name="Expected net gain from protest G",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "gains_that_would_result_from_success_v": 1,
        "probability_of_success_o": 1,
        "cost_of_protest_c": 1,
    },
)
def expected_net_gain_from_protest_g():
    """
    Pg 184: This fonnula involves yet another simplification - that the costs of repression do not depend on the chances for success. In some cases, this is clearly false - those leading a rebellion are likely to suffer far greater costs if the rebellion fails than if it succeeds. However, if we focus on the ordinary protestor, say the person who helped defend the Russian Parliament in 1991, or the civil rights protestor who risks a beating or arrest, for them the eventual result days or weeks later will not change whether a bullet finds them on the barricade, or lighten the beating, or avoid the arrest. For them, the immediate risks involved with the act of protest itself are what counts - which is to say that leaders and followers may have a separate calculus of prospective gains and risks, with both being much greater for those in charge.
    """
    return (
        gains_that_would_result_from_success_v() * probability_of_success_o()
        - cost_of_protest_c()
    )
