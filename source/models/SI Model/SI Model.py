
from __future__ import division
import numpy as np
from pysd import functions

def time():
    return _t

# Share the `time` function with the module for `step`, `pulse`, etc.
functions.__builtins__.update({'time':time})


def new_reported_cases():
    """
    
    """
    loc_dimension_dir = 0 
    output = infection_rate()

    return output

def population_infected_with_ebola():
    return _state['population_infected_with_ebola']

def _population_infected_with_ebola_init():
    try:
        loc_dimension_dir = population_infected_with_ebola.dimension_dir
    except:
        loc_dimension_dir = 0
    return 1

def _dpopulation_infected_with_ebola_dt():
    try:
        loc_dimension_dir = population_infected_with_ebola.dimension_dir
    except:
        loc_dimension_dir = 0
    return infection_rate()

def population_susceptible_to_ebola():
    return _state['population_susceptible_to_ebola']

def _population_susceptible_to_ebola_init():
    try:
        loc_dimension_dir = population_susceptible_to_ebola.dimension_dir
    except:
        loc_dimension_dir = 0
    return total_population()

def _dpopulation_susceptible_to_ebola_dt():
    try:
        loc_dimension_dir = population_susceptible_to_ebola.dimension_dir
    except:
        loc_dimension_dir = 0
    return -infection_rate()

def contact_frequency():
    """
    
    """
    loc_dimension_dir = 0 
    output = 7

    return output

def contacts_between_infected_and_uninfected_persons():
    """
    
    """
    loc_dimension_dir = 0 
    output = probability_of_contact_with_infected_person()*susceptible_contacts()

    return output

def cumulative_reported_cases():
    return _state['cumulative_reported_cases']

def _cumulative_reported_cases_init():
    try:
        loc_dimension_dir = cumulative_reported_cases.dimension_dir
    except:
        loc_dimension_dir = 0
    return 0

def _dcumulative_reported_cases_dt():
    try:
        loc_dimension_dir = cumulative_reported_cases.dimension_dir
    except:
        loc_dimension_dir = 0
    return new_reported_cases()

def infection_rate():
    """
    
    """
    loc_dimension_dir = 0 
    output = contacts_between_infected_and_uninfected_persons()*infectivity()

    return output

def infectivity():
    """
    
    """
    loc_dimension_dir = 0 
    output = 0.05

    return output

def probability_of_contact_with_infected_person():
    """
    
    """
    loc_dimension_dir = 0 
    output = population_infected_with_ebola()/total_population()

    return output

def susceptible_contacts():
    """
    
    """
    loc_dimension_dir = 0 
    output = contact_frequency()*population_susceptible_to_ebola()

    return output

def total_population():
    """
    
    """
    loc_dimension_dir = 0 
    output = 7150

    return output

def final_time():
    """
    
    """
    loc_dimension_dir = 0 
    output = 35

    return output

def initial_time():
    """
    
    """
    loc_dimension_dir = 0 
    output = 0

    return output

def saveper():
    """
    
    """
    loc_dimension_dir = 0 
    output = time_step()

    return output

def time_step():
    """
    
    """
    loc_dimension_dir = 0 
    output = 0.125

    return output
