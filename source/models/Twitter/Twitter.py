from __future__ import division                                 
import numpy as np                                              
from pysd import functions                                      
from pysd import builder                                        
                                                                
class Components(builder.ComponentClass):                       
                                                                
    def displacement(self):
        """Type: Flow or Auxiliary
        """
        return self.posts_on_timeline()/self.displacement_timescale() 

    def displacement_timescale(self):
        """Type: Flow or Auxiliary
        """
        return 3600 

    def dposts_on_timeline_dt(self):                       
        return self.tweeting()-self.displacement()                           

    def posts_on_timeline_init(self):                      
        return 0                           

    def posts_on_timeline(self):                            
        """ Stock: posts_on_timeline =                      
                 self.tweeting()-self.displacement()                          
                                             
        Initial Value: 0                    
        Do not overwrite this function       
        """                                  
        return self.state["posts_on_timeline"]              
                                             
    def tweeting(self):
        """Type: Flow or Auxiliary
        """
        return 4 

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
        return 1 

