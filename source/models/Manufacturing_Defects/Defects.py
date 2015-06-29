from __future__ import division                                 
import numpy as np                                              
from pysd import functions                                      
from pysd import builder                                        
                                                                
class Components(builder.ComponentClass):                       
                                                                
    def influence_of_backlog_on_speed(self, x):                                      
        return self.functions.lookup(x,                   
                                     self.influence_of_backlog_on_speed.xs,          
                                     self.influence_of_backlog_on_speed.ys)          
                                                          
    influence_of_backlog_on_speed.xs = [0.0, 5.0, 10.0, 15.0, 20.0, 80.0]                                            
    influence_of_backlog_on_speed.ys = [0.1, 0.1, 0.09, 0.05, 0.04, 0.04]                                            
                                                          
    def influence_of_backlog_on_workday(self, x):                                      
        return self.functions.lookup(x,                   
                                     self.influence_of_backlog_on_workday.xs,          
                                     self.influence_of_backlog_on_workday.ys)          
                                                          
    influence_of_backlog_on_workday.xs = [0.0, 2.76986, 5.53971, 10.3462, 13.1161, 16.5377, 20.5295, 60.0]                                            
    influence_of_backlog_on_workday.ys = [0.1, 0.128571, 0.188095, 0.347619, 0.416667, 0.452381, 0.469048, 0.5]                                            
                                                          
    def length_of_workday(self):
        """Type: Flow or Auxiliary
        """
        return self.influence_of_backlog_on_workday(self.backlog()) 

    def fulfillment_rate(self):
        """Type: Flow or Auxiliary
        """
        return self.number_of_employees()* self.length_of_workday()/ self.time_allocated_per_unit()* (1-self.defect_rate()) 

    def time_allocated_per_unit(self):
        """Type: Flow or Auxiliary
        """
        return self.influence_of_backlog_on_speed(self.backlog()) 

    def number_of_employees(self):
        """Type: Flow or Auxiliary
        """
        return 2 

    def arrival_rate(self):
        """Type: Flow or Auxiliary
        """
        return 10 + 12 * self.functions.pulse(20 , 10 ) 

    def dbacklog_dt(self):                       
        return self.arrival_rate()-self.fulfillment_rate()                           

    def backlog_init(self):                      
        return 11.7                           

    def backlog(self):                            
        """ Stock: backlog =                      
                 self.arrival_rate()-self.fulfillment_rate()                          
                                             
        Initial Value: 11.7                    
        Do not overwrite this function       
        """                                  
        return self.state["backlog"]              
                                             
    def defect_rate(self):
        """Type: Flow or Auxiliary
        """
        return 0.01 * self.length_of_workday()/ self.time_allocated_per_unit() 

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

