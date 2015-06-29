from __future__ import division                                 
import numpy as np                                              
from pysd import functions                                      
from pysd import builder                                        
                                                                
class Components(builder.ComponentClass):                       
                                                                
    def prey_births(self):
        """Type: Flow or Auxiliary
        """
        return self.prey_fertility()*self.prey_population() 

    def predation_rate(self):
        """Type: Flow or Auxiliary
        """
        return 0.0001 

    def prey_deaths(self):
        """Type: Flow or Auxiliary
        """
        return self.predation_rate()*self.prey_population()*self.predator_population() 

    def prey_fertility(self):
        """Type: Flow or Auxiliary
        """
        return 2 

    def dprey_population_dt(self):                       
        return self.prey_births()-self.prey_deaths()                           

    def prey_population_init(self):                      
        return 250                           

    def prey_population(self):                            
        """ Stock: prey_population =                      
                 self.prey_births()-self.prey_deaths()                          
                                             
        Initial Value: 250                    
        Do not overwrite this function       
        """                                  
        return self.state["prey_population"]              
                                             
    def predator_births(self):
        """Type: Flow or Auxiliary
        """
        return self.predator_food_driven_fertility()*self.prey_population()*self.predator_population() 

    def predator_deaths(self):
        """Type: Flow or Auxiliary
        """
        return self.predator_mortality()*self.predator_population() 

    def predator_food_driven_fertility(self):
        """Type: Flow or Auxiliary
        """
        return 0.001 

    def predator_mortality(self):
        """Type: Flow or Auxiliary
        """
        return 0.01 

    def dpredator_population_dt(self):                       
        return self.predator_births()-self.predator_deaths()                           

    def predator_population_init(self):                      
        return 100                           

    def predator_population(self):                            
        """ Stock: predator_population =                      
                 self.predator_births()-self.predator_deaths()                          
                                             
        Initial Value: 100                    
        Do not overwrite this function       
        """                                  
        return self.state["predator_population"]              
                                             
    def final_time(self):
        """Type: Flow or Auxiliary
        """
        return 50 

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
        return 0.015625 

