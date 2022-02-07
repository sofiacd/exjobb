from community import *

class Global:
    def __init__(self, globals,community_thresholds:np.array, agent_thresholds:np.array, agent_costs:np.array, harvesting:np.array, socializing:np.array):
        # CURRENT ORDERs: 
        # globals = {updates_per_year, num_traditions, insitutionlist, reproductive_age} (dict)
        # community_thresholds = [Nmin,Nmax] (np.array)
        # agent_thresholds = [Emin, Erep]
        # agent_costs = [Cost_rep, Cost_allele, Cost_existance, Cost_trad] (np.array)
        # harvesting = [R, epsilon, m]
        # socializing = [SLR]

        self._globals = globals 
        self._community_thresholds = community_thresholds
        self._agent_threshold = agent_thresholds
        self._agent_costs =agent_costs
        self._harvesting = harvesting 
        self._socializing = socializing 

        self._communities = {}
        self._communitycount =0 # of all time
        self._active_communities = 0
        self._agentcount=0 #all agnts in all comunitiez (incl dead)
        #plocka isär parametergrupperna 
        #globals 
        self._timeunit= globals[0]
        self._num_traditions = globals[1]
        self._institutionlist = globals[2]
        self._rep_age = globals[3]
        #community thresholds 
        self._N_min = community_thresholds[0]
        self._N_max = community_thresholds[1]

        #agent_thresholds 
        self._Emin = agent_thresholds[0]
        self._Erep = agent_thresholds[1]
    
        #agent costs 
        self._cost_rep = agent_costs[0]
        self._cost_allele = agent_costs[1]
        self._cost_existance = agent_costs[2]
        self._cost_trad = agent_costs[3]

        #harvesting 
        self._R = harvesting[0]
        self._epsilon = harvesting[1]
        self._m = harvesting[2]

        #socializing
        self._SLR = socializing[0]
        
        c = self.new_community()
        self.__add_new_agent(c)
        self.__add_new_agent(c)

    def __get_community(self,ckey):
        if isinstance(ckey,int):
            return self._communities[f'CO{ckey}']

        return self._communities[ckey]

    def get_num_traditions(self):
        return self._num_traditions

    def get_monopolizability(self):
        return self._monopolizabilty

    def get_institutionlist(self):
        return self._institutionlist
    
    def get_agentcount(self):
        return self._agentcount
    
    def get_epsilon(self):
        return self._epsilon
    
    def get_E(self):
        return self._E
    
    def get_SLR(self):
        return self._SLR

    def get_communitycount(self):
        return self._communitycount
    #def get_communities(self):
    #    return self._communities
    
    #def get_community_keyindex(community:Community):
     #   return community.get_key_index()
    
    def __add_new_agent(self, cindex:int): # birth
        comm = self.__get_community(cindex)
        self._agentcount+=1
        comm.add_new_agent(self._agentcount, self._E, self._num_traditions)

    def __move_agent(self, aindex:int, c1index:int, c2index:int):
        #agent count unchanged
        c1 = self.__get_community(c1index)
        c2 = self.__get_community(c2index)
        #move agent from com1 to com2
        c2.add_agent(c1.get_agent(aindex))
        c1.remove_agent(aindex)
        

    def new_community(self):
        self._communitycount =+1
        self._active_communities =+1 
        newindex = self._communitycount
        newcom = Community(newindex, self._num_traditions, self._institutionlist, self._SLR, self._E,self)
        self._communities[f'CO{newindex}'] = newcom
        return newindex
    
    def __split_community(self, cindex:int):
        c = self.__get_community(cindex)
        c2 = self.__new_community()
        c2index = c2.get_key_index()
        num_active = c.get_num_active_agents()
        track = c.get_track()
        if(num_active!=len(track)): 
            print('error somewhere in community')
            print('aborted split')
            return
        n = round(num_active/2)
        sample= random.sample(track, n)
        for aindex in sample: 
            self.__move_agent(aindex,cindex,c2index)

    #PUBLIC
    def print_communitites(self):
        for c in self._communities:
            com= self.__get_community(c)
            print (f'{c}      --      {com.get_track()}')
        return    
    

    def harvest(self): ## for each community #cosecho
        for c in self.__communities:
            com=self.__get_community(c)
            com.harvest()
        # in each community 
        return

    def check_for_deaths(self):
        for c in self._communities:
            com = self.__get_community()
            com.check_for_deaths()
        return

    def check_for_births(self):
        for c in self._communities:
            com = self.__get_community()
            com.check_for_births()
        return


for 