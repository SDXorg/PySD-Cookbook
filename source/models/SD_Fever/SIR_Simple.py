from __future__ import division                                 
import numpy as np                                              
from pysd import functions                                      
from pysd import builder                                        
                                                                
class Components(builder.ComponentClass):                       
                                                                
    def dcumulative_cases_dt(self):                       
        return self.report_case()                           

    def cumulative_cases_init(self):                      
        return 0                           

    def cumulative_cases(self):                            
        """ Stock: cumulative_cases =                      
                 self.report_case()                          
                                             
        Initial Value: 0                    
        Do not overwrite this function       
        """                                  
        return self.state["cumulative_cases"]              
                                             
    def report_case(self):
        """Type: Flow or Auxiliary
        """
        return self.infect() 

    def infect(self):
        """Type: Flow or Auxiliary
        """
        return self.susceptible()*(self.infectious()/self.total_population()) * self.contact_infectivity() 

    def contact_infectivity(self):
        """Type: Flow or Auxiliary
        """
        return 0.7 

    def recovery_period(self):
        """Type: Flow or Auxiliary
        """
        return 5 

    def dinfectious_dt(self):                       
        return self.infect()-self.recover()                           

    def infectious_init(self):                      
        return 5                           

    def infectious(self):                            
        """ Stock: infectious =                      
                 self.infect()-self.recover()                          
                                             
        Initial Value: 5                    
        Do not overwrite this function       
        """                                  
        return self.state["infectious"]              
                                             
    def drecovered_dt(self):                       
        return self.recover()                           

    def recovered_init(self):                      
        return 0                           

    def recovered(self):                            
        """ Stock: recovered =                      
                 self.recover()                          
                                             
        Initial Value: 0                    
        Do not overwrite this function       
        """                                  
        return self.state["recovered"]              
                                             
    def recover(self):
        """Type: Flow or Auxiliary
        """
        return self.infectious()/self.recovery_period() 

    def dsusceptible_dt(self):                       
        return -self.infect()                           

    def susceptible_init(self):                      
        return self.total_population()                           

    def susceptible(self):                            
        """ Stock: susceptible =                      
                 -self.infect()                          
                                             
        Initial Value: self.total_population()                    
        Do not overwrite this function       
        """                                  
        return self.state["susceptible"]              
                                             
    def total_population(self):
        """Type: Flow or Auxiliary
        """
        return 1000 

    def final_time(self):
        """Type: Flow or Auxiliary
        """
        return 100 

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
        return 0.5 

