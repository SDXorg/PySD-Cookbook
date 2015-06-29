from __future__ import division                                 
import numpy as np                                              
from pysd import functions                                      
from pysd import builder                                        
                                                                
class Components(builder.ComponentClass):                       
                                                                
    def bday10(self):
        """Type: Flow or Auxiliary
        """
        return self.dec_1()/ 10 

    def bday20(self):
        """Type: Flow or Auxiliary
        """
        return self.dec_2()/ 10 

    def bday30(self):
        """Type: Flow or Auxiliary
        """
        return self.dec_3()/ 10 

    def bday40(self):
        """Type: Flow or Auxiliary
        """
        return self.dec_4()/10 

    def bday50(self):
        """Type: Flow or Auxiliary
        """
        return self.dec_5()/10 

    def bday60(self):
        """Type: Flow or Auxiliary
        """
        return self.dec_6()/ 10 

    def bday70(self):
        """Type: Flow or Auxiliary
        """
        return self.dec_7()/10 

    def bday80(self):
        """Type: Flow or Auxiliary
        """
        return self.dec_8()/10 

    def births(self):
        """Type: Flow or Auxiliary
        """
        return 0 

    def ddec_1_dt(self):                       
        return self.births()-self.bday10()-self.dec_1_loss()                           

    def dec_1_init(self):                      
        return 10                           

    def dec_1(self):                            
        """ Stock: dec_1 =                      
                 self.births()-self.bday10()-self.dec_1_loss()                          
                                             
        Initial Value: 10                    
        Do not overwrite this function       
        """                                  
        return self.state["dec_1"]              
                                             
    def dec_1_loss(self):
        """Type: Flow or Auxiliary
        """
        return self.dec_1()* self.dec_1_loss_rate() 

    def dec_1_loss_rate(self):
        """Type: Flow or Auxiliary
        """
        return 0.05 

    def ddec_2_dt(self):                       
        return self.bday10()-self.bday20()-self.dec_2_loss()                           

    def dec_2_init(self):                      
        return 10                           

    def dec_2(self):                            
        """ Stock: dec_2 =                      
                 self.bday10()-self.bday20()-self.dec_2_loss()                          
                                             
        Initial Value: 10                    
        Do not overwrite this function       
        """                                  
        return self.state["dec_2"]              
                                             
    def dec_2_loss(self):
        """Type: Flow or Auxiliary
        """
        return self.dec_2()* self.dec_2_loss_rate() 

    def dec_2_loss_rate(self):
        """Type: Flow or Auxiliary
        """
        return 0.05 

    def ddec_3_dt(self):                       
        return self.bday20()-self.bday30()-self.dec_3_loss()                           

    def dec_3_init(self):                      
        return 10                           

    def dec_3(self):                            
        """ Stock: dec_3 =                      
                 self.bday20()-self.bday30()-self.dec_3_loss()                          
                                             
        Initial Value: 10                    
        Do not overwrite this function       
        """                                  
        return self.state["dec_3"]              
                                             
    def dec_3_loss(self):
        """Type: Flow or Auxiliary
        """
        return self.dec_3()* self.dec_3_loss_rate() 

    def dec_3_loss_rate(self):
        """Type: Flow or Auxiliary
        """
        return 0.05 

    def ddec_4_dt(self):                       
        return self.bday30()-self.bday40()-self.dec_4_loss()                           

    def dec_4_init(self):                      
        return 10                           

    def dec_4(self):                            
        """ Stock: dec_4 =                      
                 self.bday30()-self.bday40()-self.dec_4_loss()                          
                                             
        Initial Value: 10                    
        Do not overwrite this function       
        """                                  
        return self.state["dec_4"]              
                                             
    def dec_4_loss(self):
        """Type: Flow or Auxiliary
        """
        return self.dec_4()* self.dec_4_loss_rate() 

    def dec_4_loss_rate(self):
        """Type: Flow or Auxiliary
        """
        return 0.05 

    def ddec_5_dt(self):                       
        return self.bday40()-self.bday50()-self.dec_5_loss()                           

    def dec_5_init(self):                      
        return 10                           

    def dec_5(self):                            
        """ Stock: dec_5 =                      
                 self.bday40()-self.bday50()-self.dec_5_loss()                          
                                             
        Initial Value: 10                    
        Do not overwrite this function       
        """                                  
        return self.state["dec_5"]              
                                             
    def dec_5_loss(self):
        """Type: Flow or Auxiliary
        """
        return self.dec_5()* self.dec_5_loss_rate() 

    def dec_5_loss_rate(self):
        """Type: Flow or Auxiliary
        """
        return 0.05 

    def ddec_6_dt(self):                       
        return self.bday50()-self.bday60()-self.dec_6_loss()                           

    def dec_6_init(self):                      
        return 10                           

    def dec_6(self):                            
        """ Stock: dec_6 =                      
                 self.bday50()-self.bday60()-self.dec_6_loss()                          
                                             
        Initial Value: 10                    
        Do not overwrite this function       
        """                                  
        return self.state["dec_6"]              
                                             
    def dec_6_loss(self):
        """Type: Flow or Auxiliary
        """
        return self.dec_6()* self.dec_6_loss_rate() 

    def dec_6_loss_rate(self):
        """Type: Flow or Auxiliary
        """
        return 0.05 

    def ddec_7_dt(self):                       
        return self.bday60()-self.bday70()-self.dec_7_loss()                           

    def dec_7_init(self):                      
        return 10                           

    def dec_7(self):                            
        """ Stock: dec_7 =                      
                 self.bday60()-self.bday70()-self.dec_7_loss()                          
                                             
        Initial Value: 10                    
        Do not overwrite this function       
        """                                  
        return self.state["dec_7"]              
                                             
    def dec_7_loss(self):
        """Type: Flow or Auxiliary
        """
        return self.dec_7()* self.dec_7_loss_rate() 

    def dec_7_loss_rate(self):
        """Type: Flow or Auxiliary
        """
        return 0.05 

    def ddec_8_dt(self):                       
        return self.bday70()-self.bday80()-self.dec_8_loss()                           

    def dec_8_init(self):                      
        return 10                           

    def dec_8(self):                            
        """ Stock: dec_8 =                      
                 self.bday70()-self.bday80()-self.dec_8_loss()                          
                                             
        Initial Value: 10                    
        Do not overwrite this function       
        """                                  
        return self.state["dec_8"]              
                                             
    def dec_8_loss(self):
        """Type: Flow or Auxiliary
        """
        return self.dec_8()* self.dec_8_loss_rate() 

    def dec_8_loss_rate(self):
        """Type: Flow or Auxiliary
        """
        return 0.05 

    def dec_9_loss_rate(self):
        """Type: Flow or Auxiliary
        """
        return 0.05 

    def ddec_9_dt(self):                       
        return self.bday80()-self.dec_9_loss()                           

    def dec_9_init(self):                      
        return 10                           

    def dec_9(self):                            
        """ Stock: dec_9 =                      
                 self.bday80()-self.dec_9_loss()                          
                                             
        Initial Value: 10                    
        Do not overwrite this function       
        """                                  
        return self.state["dec_9"]              
                                             
    def dec_9_loss(self):
        """Type: Flow or Auxiliary
        """
        return self.dec_9()* self.dec_9_loss_rate() 

    def final_time(self):
        """Type: Flow or Auxiliary
        """
        return 2010 

    def initial_time(self):
        """Type: Flow or Auxiliary
        """
        return 2000 

    def saveper(self):
        """Type: Flow or Auxiliary
        """
        return self.time_step() 

    def time_step(self):
        """Type: Flow or Auxiliary
        """
        return 0.125 

