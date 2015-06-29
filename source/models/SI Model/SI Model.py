from __future__ import division                                 
import numpy as np                                              
from pysd import functions                                      
from pysd import builder                                        
                                                                
class Components(builder.ComponentClass):                       
                                                                
    def new_reported_cases(self):
        """Type: Flow or Auxiliary
        """
        return self.infection_rate() 

    def dpopulation_infected_with_ebola_dt(self):                       
        return self.infection_rate()                           

    def population_infected_with_ebola_init(self):                      
        return 1                           

    def population_infected_with_ebola(self):                            
        """ Stock: population_infected_with_ebola =                      
                 self.infection_rate()                          
                                             
        Initial Value: 1                    
        Do not overwrite this function       
        """                                  
        return self.state["population_infected_with_ebola"]              
                                             
    def dpopulation_susceptible_to_ebola_dt(self):                       
        return -self.infection_rate()                           

    def population_susceptible_to_ebola_init(self):                      
        return self.total_population()                           

    def population_susceptible_to_ebola(self):                            
        """ Stock: population_susceptible_to_ebola =                      
                 -self.infection_rate()                          
                                             
        Initial Value: self.total_population()                    
        Do not overwrite this function       
        """                                  
        return self.state["population_susceptible_to_ebola"]              
                                             
    def contact_frequency(self):
        """Type: Flow or Auxiliary
        """
        return 7 

    def contacts_between_infected_and_uninfected_persons(self):
        """Type: Flow or Auxiliary
        """
        return self.probability_of_contact_with_infected_person()* self.susceptible_contacts() 

    def dcumulative_reported_cases_dt(self):                       
        return self.new_reported_cases()                           

    def cumulative_reported_cases_init(self):                      
        return 0                           

    def cumulative_reported_cases(self):                            
        """ Stock: cumulative_reported_cases =                      
                 self.new_reported_cases()                          
                                             
        Initial Value: 0                    
        Do not overwrite this function       
        """                                  
        return self.state["cumulative_reported_cases"]              
                                             
    def infection_rate(self):
        """Type: Flow or Auxiliary
        """
        return self.contacts_between_infected_and_uninfected_persons()* self.infectivity() 

    def infectivity(self):
        """Type: Flow or Auxiliary
        """
        return 0.05 

    def probability_of_contact_with_infected_person(self):
        """Type: Flow or Auxiliary
        """
        return self.population_infected_with_ebola()/ self.total_population() 

    def susceptible_contacts(self):
        """Type: Flow or Auxiliary
        """
        return self.contact_frequency()* self.population_susceptible_to_ebola() 

    def total_population(self):
        """Type: Flow or Auxiliary
        """
        return 7150 

    def final_time(self):
        """Type: Flow or Auxiliary
        """
        return 35 

    def initial_time(self):
        """Type: Flow or Auxiliary
        """
        return 0 

    def saveper(self):
        """Type: Flow or Auxiliary
        """
        return self.time_step() 

    def time_step(self):
        """Type: Flow or Auxiliary
        """
        return 0.125 

