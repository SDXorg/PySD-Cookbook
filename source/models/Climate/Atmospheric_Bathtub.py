"""
Python model 'Atmospheric_Bathtub.py'
Translated using PySD
"""

from pathlib import Path
import numpy as np

from pysd.py_backend.statefuls import Integ
from pysd import Component

__pysd_version__ = "3.6.0"

__data = {"scope": None, "time": lambda: 0}

_root = Path(__file__).parent


component = Component()

#######################################################################
#                          CONTROL VARIABLES                          #
#######################################################################

_control_vars = {
    "initial_time": lambda: 0,
    "final_time": lambda: 100,
    "time_step": lambda: 1,
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


@component.add(name="Emissions", comp_type="Constant", comp_subtype="Normal")
def emissions():
    return 0


@component.add(
    name="Excess Atmospheric Carbon",
    comp_type="Stateful",
    comp_subtype="Integ",
    depends_on={"_integ_excess_atmospheric_carbon": 1},
    other_deps={
        "_integ_excess_atmospheric_carbon": {
            "initial": {},
            "step": {"emissions": 1, "natural_removal": 1},
        }
    },
)
def excess_atmospheric_carbon():
    return _integ_excess_atmospheric_carbon()


_integ_excess_atmospheric_carbon = Integ(
    lambda: emissions() - natural_removal(),
    lambda: 0,
    "_integ_excess_atmospheric_carbon",
)


@component.add(
    name="Natural Removal",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"excess_atmospheric_carbon": 1, "removal_constant": 1},
)
def natural_removal():
    return excess_atmospheric_carbon() * removal_constant()


@component.add(name="Removal Constant", comp_type="Constant", comp_subtype="Normal")
def removal_constant():
    return 0.01
