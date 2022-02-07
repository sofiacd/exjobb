
from tqdm import tqdm
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import random

class Agent:
    def __init__(self,aindex:int, cindex:int, E:int, num_traditions:int):
        self.key = aindex
        self.age = 0
        self.community = f'CO{cindex}'
        self.energylevel = E #default energy level
        self.traditionrep= np.zeros(num_traditions)
        
    def get_key(self):
        return self.key

    def get_traditionrep(self):
        return self.traditionrep
    


    def make_allele(self, index:int):
        self.traditionrep[index] =1
        return

    def set_community(self, cindex:int):
        #only to be done from community classes
        self.community = f'CO{cindex}'
        return
    
    def reproduce(self, Erep:int):
        self.pay_cost(Erep)
        return
        
    def check_for_death(self,Emin:int):
        return(self.energylevel<Emin)
          
    def check_for_mate(self, comm): # check that there is a mate of reproductiove age in the community, the mate pays no reproducitove costs. 
        comm.get_agents()
        return 
        
    def get_age(self):
        return self.age

    def pay_cost(self,cost:float):
        if(self.energylevel>cost):
            self.energylevel-= cost
            return True
        else: return False
    
    def recieve_payoff(self,bait:float, eps:float, m:float=1):
        self.energylevel+= bait*m*eps
        return
