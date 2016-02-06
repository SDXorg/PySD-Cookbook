from __future__ import division                                 
import numpy as np                                              
from pysd import functions                                      
from pysd import builder                                        
                                                                
class Components(builder.ComponentClass):                       
                                                                
    def total_emails(self):
        """Type: Flow or Auxiliary
        """
        return 1000 

    def easy_email_volume(self):
        """Type: Flow or Auxiliary
        """
        return self.total_emails()* self.easy_fraction() 

    def easy_fraction(self):
        """Type: Flow or Auxiliary
        """
        return 0.5 

    def easy_arrival_delay_easy_reply_time_flow_1_of_2(self):
        """Type: Flow or Auxiliary
        """
        return self.easy_arrival() 

    def easy_arrival_delay_easy_reply_time_flow_2_of_2(self):
        """Type: Flow or Auxiliary
        """
        return self.easy_arrival_delay_easy_reply_time_stock_1_of_1()/(1.*self.easy_reply_time()/1) 

    def deasy_arrival_delay_easy_reply_time_stock_1_of_1_dt(self):                       
        return self.easy_arrival_delay_easy_reply_time_flow_1_of_2() - self.easy_arrival_delay_easy_reply_time_flow_2_of_2()                           

    def easy_arrival_delay_easy_reply_time_stock_1_of_1_init(self):                      
        return 0 * (self.easy_reply_time() / 1)                           

    def easy_arrival_delay_easy_reply_time_stock_1_of_1(self):                            
        """ Stock: easy_arrival_delay_easy_reply_time_stock_1_of_1 =                      
                 self.easy_arrival_delay_easy_reply_time_flow_1_of_2() - self.easy_arrival_delay_easy_reply_time_flow_2_of_2()                          
                                             
        Initial Value: 0 * (self.easy_reply_time() / 1)                    
        Do not overwrite this function       
        """                                  
        return self.state["easy_arrival_delay_easy_reply_time_stock_1_of_1"]              
                                             
    def easy_reply(self):
        """Type: Flow or Auxiliary
        """
        return self.easy_arrival_delay_easy_reply_time_flow_2_of_2() 

    def hard_email_volume(self):
        """Type: Flow or Auxiliary
        """
        return self.total_emails()* (1 - self.easy_fraction()) 

    def net_email_output(self):
        """Type: Flow or Auxiliary
        """
        return self.easy_reply()+ self.hard_reply() 

    def easy_reply_time(self):
        """Type: Flow or Auxiliary
        """
        return 1 

    def hard_arrival_delay_hard_reply_time_flow_1_of_4(self):
        """Type: Flow or Auxiliary
        """
        return self.hard_arrival() 

    def hard_arrival_delay_hard_reply_time_flow_2_of_4(self):
        """Type: Flow or Auxiliary
        """
        return self.hard_arrival_delay_hard_reply_time_stock_1_of_3()/(1.*self.hard_reply_time()/3) 

    def hard_arrival_delay_hard_reply_time_flow_3_of_4(self):
        """Type: Flow or Auxiliary
        """
        return self.hard_arrival_delay_hard_reply_time_stock_2_of_3()/(1.*self.hard_reply_time()/3) 

    def hard_arrival_delay_hard_reply_time_flow_4_of_4(self):
        """Type: Flow or Auxiliary
        """
        return self.hard_arrival_delay_hard_reply_time_stock_3_of_3()/(1.*self.hard_reply_time()/3) 

    def dhard_arrival_delay_hard_reply_time_stock_1_of_3_dt(self):                       
        return self.hard_arrival_delay_hard_reply_time_flow_1_of_4() - self.hard_arrival_delay_hard_reply_time_flow_2_of_4()                           

    def hard_arrival_delay_hard_reply_time_stock_1_of_3_init(self):                      
        return 0 * (self.hard_reply_time() / 3)                           

    def hard_arrival_delay_hard_reply_time_stock_1_of_3(self):                            
        """ Stock: hard_arrival_delay_hard_reply_time_stock_1_of_3 =                      
                 self.hard_arrival_delay_hard_reply_time_flow_1_of_4() - self.hard_arrival_delay_hard_reply_time_flow_2_of_4()                          
                                             
        Initial Value: 0 * (self.hard_reply_time() / 3)                    
        Do not overwrite this function       
        """                                  
        return self.state["hard_arrival_delay_hard_reply_time_stock_1_of_3"]              
                                             
    def dhard_arrival_delay_hard_reply_time_stock_2_of_3_dt(self):                       
        return self.hard_arrival_delay_hard_reply_time_flow_2_of_4() - self.hard_arrival_delay_hard_reply_time_flow_3_of_4()                           

    def hard_arrival_delay_hard_reply_time_stock_2_of_3_init(self):                      
        return 0 * (self.hard_reply_time() / 3)                           

    def hard_arrival_delay_hard_reply_time_stock_2_of_3(self):                            
        """ Stock: hard_arrival_delay_hard_reply_time_stock_2_of_3 =                      
                 self.hard_arrival_delay_hard_reply_time_flow_2_of_4() - self.hard_arrival_delay_hard_reply_time_flow_3_of_4()                          
                                             
        Initial Value: 0 * (self.hard_reply_time() / 3)                    
        Do not overwrite this function       
        """                                  
        return self.state["hard_arrival_delay_hard_reply_time_stock_2_of_3"]              
                                             
    def dhard_arrival_delay_hard_reply_time_stock_3_of_3_dt(self):                       
        return self.hard_arrival_delay_hard_reply_time_flow_3_of_4() - self.hard_arrival_delay_hard_reply_time_flow_4_of_4()                           

    def hard_arrival_delay_hard_reply_time_stock_3_of_3_init(self):                      
        return 0 * (self.hard_reply_time() / 3)                           

    def hard_arrival_delay_hard_reply_time_stock_3_of_3(self):                            
        """ Stock: hard_arrival_delay_hard_reply_time_stock_3_of_3 =                      
                 self.hard_arrival_delay_hard_reply_time_flow_3_of_4() - self.hard_arrival_delay_hard_reply_time_flow_4_of_4()                          
                                             
        Initial Value: 0 * (self.hard_reply_time() / 3)                    
        Do not overwrite this function       
        """                                  
        return self.state["hard_arrival_delay_hard_reply_time_stock_3_of_3"]              
                                             
    def hard_reply(self):
        """Type: Flow or Auxiliary
        """
        return self.hard_arrival_delay_hard_reply_time_flow_4_of_4() 

    def hard_reply_time(self):
        """Type: Flow or Auxiliary
        """
        return 4 

    def easy_arrival(self):
        """Type: Flow or Auxiliary
        """
        return self.easy_email_volume()/ self.time_step()* self.functions.pulse(0, self.time_step()) 

    def hard_arrival(self):
        """Type: Flow or Auxiliary
        """
        return self.hard_email_volume()/ self.time_step()* self.functions.pulse(0, self.time_step()) 

    def deasy_emails_dt(self):                       
        return self.easy_arrival()-self.easy_reply()                           

    def easy_emails_init(self):                      
        return 0                           

    def easy_emails(self):                            
        """ Stock: easy_emails =                      
                 self.easy_arrival()-self.easy_reply()                          
                                             
        Initial Value: 0                    
        Do not overwrite this function       
        """                                  
        return self.state["easy_emails"]              
                                             
    def dhard_emails_dt(self):                       
        return self.hard_arrival()-self.hard_reply()                           

    def hard_emails_init(self):                      
        return 0                           

    def hard_emails(self):                            
        """ Stock: hard_emails =                      
                 self.hard_arrival()-self.hard_reply()                          
                                             
        Initial Value: 0                    
        Do not overwrite this function       
        """                                  
        return self.state["hard_emails"]              
                                             
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
        return 0.0625 

