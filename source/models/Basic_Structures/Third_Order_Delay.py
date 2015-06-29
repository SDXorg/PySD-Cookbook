from __future__ import division                                 
import numpy as np                                              
from pysd import functions                                      
from pysd import builder                                        
                                                                
class Components(builder.ComponentClass):                       
                                                                
    def delay(self):
        """Type: Flow or Auxiliary
        """
        return 3 

    def ddelay_buffer_1_dt(self):                       
        return self.input()-self.throughput_1()                           

    def delay_buffer_1_init(self):                      
        return 0                           

    def delay_buffer_1(self):                            
        """ Stock: delay_buffer_1 =                      
                 self.input()-self.throughput_1()                          
                                             
        Initial Value: 0                    
        Do not overwrite this function       
        """                                  
        return self.state["delay_buffer_1"]              
                                             
    def ddelay_buffer_2_dt(self):                       
        return self.throughput_1()-self.throughput_2()                           

    def delay_buffer_2_init(self):                      
        return 0                           

    def delay_buffer_2(self):                            
        """ Stock: delay_buffer_2 =                      
                 self.throughput_1()-self.throughput_2()                          
                                             
        Initial Value: 0                    
        Do not overwrite this function       
        """                                  
        return self.state["delay_buffer_2"]              
                                             
    def ddelay_buffer_3_dt(self):                       
        return self.throughput_2()-self.output()                           

    def delay_buffer_3_init(self):                      
        return 0                           

    def delay_buffer_3(self):                            
        """ Stock: delay_buffer_3 =                      
                 self.throughput_2()-self.output()                          
                                             
        Initial Value: 0                    
        Do not overwrite this function       
        """                                  
        return self.state["delay_buffer_3"]              
                                             
    def delay_part_1(self):
        """Type: Flow or Auxiliary
        """
        return self.delay()/3 

    def delay_part_2(self):
        """Type: Flow or Auxiliary
        """
        return self.delay()/3 

    def delay_part_3(self):
        """Type: Flow or Auxiliary
        """
        return self.delay()/3 

    def input(self):
        """Type: Flow or Auxiliary
        """
        return self.functions.step(1 , 1 ) 

    def output(self):
        """Type: Flow or Auxiliary
        """
        return self.delay_buffer_3()/self.delay_part_3() 

    def throughput_1(self):
        """Type: Flow or Auxiliary
        """
        return self.delay_buffer_1()/self.delay_part_1() 

    def throughput_2(self):
        """Type: Flow or Auxiliary
        """
        return self.delay_buffer_2()/self.delay_part_2() 

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
        return 0.015625 

