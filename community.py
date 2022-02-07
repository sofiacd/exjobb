from agent import *

class Institution_in_Community: #ONE FOR EVERY COMMUNITY AND EVERY INSTITUTION TYPE 
    # TO BE CREATED AND HANDLED ONLY INSIDE COMMUNITY 
    # different type of institutions in a community. defined by one apex tradition and codependent loci traditions. 
    # descibed by tradition indices refering to the traditionrep of each agent
    def __init__(self, locis:np.array, comm:int):
        self._apex = locis[0]
        self.locis= locis  #a vector of tradition indexes where the first one is the apex
        self.complexity= len(locis) #number of locis represents the complexity 
        self.community = comm
        ######################################
        ### in community comm this institution has the following properties
        self.instances = {} # a dict of vectors each vector is an instance of the institution in this community. 
        self.num_active_instances=0 #counter of instances in this community
        return
    
    def get_instances(self):
        return self.instances
    
    def get_instance(self, keyindex:int):
        return self.instances[keyindex]

    def get_locis(self):
        return self.locis

    def add_instance(self, instance:np.array):
        self.num_active_instances+=1
        self.instances[self.num_active_instances] = instance
        
    def remove_instance(self, index: int): # should not be necessary anymore
        self.instances.pop(index)
        self.num_active_instances=-1

    def reset_instances(self):
        self.instances = {}
        self.num_active_instances=0
        return

    

class Community:
    def __init__(self, keyindex:int, num_traditions:int, institutionlist, SLR:int, Estart:int):
        self.key = f'CO{keyindex}'
        self.keyindex = keyindex
        self.active_agents = 0 #active agents!
        self.agents= {}
        self.instcount= np.zeros(len(institutionlist))
        self.tradagentcount = np.zeros(num_traditions)
        self.tradagents = {} 
        self.num_traditions = num_traditions
        self.institutions = {}
        self._make_institutions(institutionlist)
        self.SLR = SLR # social learning rate , likelihood of developing a traditionn allele when an allele of it is expressed in community
        self.Estart = Estart


    ### GET VARIABLES ######################33
    ####################################################################   
    def _make_institutions(self, institutionlist):
        for i in institutionlist:
            lokis = institutionlist[i]
            self.institutions[i] = Institution_in_Community(lokis,self.keyindex)


    def get_key(self): 
        return self.key
    def get_key_index(self):
        return self.keyindex
    def get_num_active_agents(self):
        return self.active_agents

    def get_agent(self,aindex:int):
        if(aindex in self.get_track()):
            self.agents[aindex]
            return self.agents[aindex]
        else: print(f'agent {aindex} not found active')
            
    def get_track(self):
        return list(self.agents)
   
    ###  AGENT STUFF   #######
    ####################################################################################################
    def add_agent(self,agent:Agent):
        self.active_agents+=1
        agent.set_community(self.keyindex)
        self.agents[agent.get_key]= agent
        return
    
    def add_new_agent(self,akeyindex:int, E:int, num_traditions:int): #birth
        self.active_agents+=1
        self.agents[akeyindex]= Agent(akeyindex,self.keyindex, self.Estart, self.num_traditions)
        return

    def remove_agent(self, aindex:int):
        agent = self.get_agent(aindex)
        if(aindex in self.get_track()):
            self.agents.pop(aindex)
            self.active_agents-=1
        else: print(f'agent {aindex} not found active in {self.get_key}')
        return        
    #################################################################################################
    def get_institution(self, keyindex: int):
        return self.institutions[keyindex]

    def tradition_counts(self): 
        # counts current number of expressions of each tradition in community in vector counts.
        counts = np.zeros(self.num_traditions) 
        tradagents = {}
        for a in self.agents:
            agent = a.get_agent()
            for t in range (self.num_traditions):
                counts[t] += agent.traditionrep[t] # if zero nothing else adds one
        self.tradagentcount = counts
        return counts
    
    def tradition_agents(self): 
        tradagents = {}
        for a in self.agents:
            agent = a.get_agent()
            for i in range (self.num_traditions):
                tradagents[i].append(a)
        self.tradagents = tradagents
        return tradagents

    def find_all_institution_instances(self, ind:int):
        # find one of each tradition in the instituti
        tradagentcount = self.tradition_counts()
        tradagents = self.tradition_agents()

        institution = self.get_institution(ind)
        
        pot_inst = np.zeros(len(tradagentcount)) # zeros until tradition allele is found then becomes the index of the agent
        
        while np.all([tradagentcount>0]): 
            for i,loki in enumerate(institution.get_locis()):
                r = random.random(0,int(tradagentcount[i]-1))
                pot_inst[i] = tradagents[i][r]
            #if loop ends institution is filled with alleles and pot_inst becomes inst
            #remove this agent from current alleles of tradition 
            for i in range(len(institution.get_locis())):
                tradagentcount[i] -= 1
                tradagents[i].pop(r)

            institution.add_instance(pot_inst)
            self.instcount[ind]+=1
        
        return self.instcount
                    

    def harvest(self, R, eps, m, Ecost, Emin):#BIG ONE 
        #NOTE there is a small overlapp in the structure of this function since the apexes first express their alleles and recieve the small payoff 
        #  And then recieve the big payoff of being the apex. 
        #TODO fix this?
# __________________________________________________________
        # bait is the available resource per agent per community R/N_c
        bait = R/self.active_agents
        # eps is the effectivity of alleles when extracting energy, without institutions
        # m is the monopolizability of the resource extractable by institution apex 

        # first express all alleles individually, pay cost and recieve harvest and apply SLR
        #  
        # Find all institution instances 
        # express all tradition alleles within and without institutions
        # for each allele expression, 
        #   pay the cost of expression (if possible)
        #   recieve the harvest 
        count = self.tradition_counts()
        agents = self.tradition_agents()

        #EXPRESS ALL ALLELELS in community 
        for t in range(self.num_traditions):
            for allele in range(count[t]): 
                agent= self.get_agent(agents[allele])
                if agent.pay_cost(Ecost): # if agent can pay cost 
                    agent.recieve_payoff(bait, eps) # recieve payoff for out of institution work
                #self.spread_allele(t, agents) # need energy for this 


        # CHECK HOW MANY INSTITUTIONS WHERE PRESENT IN THIS MOMENT OF HARVEST 
        # let them recieve payoff and distribute to rest.
        #constuct as many institutions as is posssible . (per institutions it will be min(tradagentcount) i e the smallest number of tradition alleles)
        for ind in self.institutions:
            institution = self.get_institution(ind)
            self.find_all_institution_instances(ind)
            instances = institution.get_instances()
            for i in instances: 
                instance = instances[i] #a np.array of agent keys containing this institution 
                apex = self.get_agent(instance[0]) # the apex agent
                apex.recieve_payoff(bait, 1,m)
                self.distribute_to_rest(apex,bait,m)
                
        return

    def socially_learn(self):
        count = self.tradition_counts()
        agents = self.tradition_agents()
        for t in range(self.num_traditions):
            for allele in range(count[t]):
                self.spread_allele(t, agents)
        return


    def check_for_deaths(self,E_min):
        for a in self.agents: 
            agent = self.get_agent(a)
            if (agent.check_for_death(E_min)):
                self.remove_agent(a)
        return 


    def check_for_births(self,E_rep, repage):
        for a in self.agents: 
            agent = self.get_agent(a)
            if (agent.get_age()>=repage):
                if (agent.check_for_mate(E_rep)):
                    agent.reproduce(E_rep)
                    newagent= self.add_new_agent()
        return 

    def spread_allele(self, tind:int, agents): # for each non able agent an allele tind is created with prob SLR
        for aind in agents: 
            pot_learner = self.get_agent[aind] # a potential learner 
            if pot_learner.get_traditionrep()[tind]==0:
                if random.random()<self.SLR: # this is a temporally normalized learning rate
                    pot_learner.make_allele(tind) # tradition learned
    


    def distribute_to_rest(self,apexind:int,bait:float, m:float): # after an institutionexpession
        available_bait =bait*(1-m)/(self.active_agents-1) # not for the apex
        for aind in self.agents:
            if (aind!=apexind):
                agent= self.get_agent(aind)
                agent.recieve_payoff(available_bait,1,1) #recieve available bait fully
    


