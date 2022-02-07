from globe import *
u = 1 #energy unit so that scaling is possible

# MODEL TIME UNIT
updates_per_year = 50 #times we check for events and let events happen per "year"


## -----------------

num_traditions = 10
institutionlist = {}
institutionlist[0] = [i for i in range(num_traditions)] # create an institution containing all community traditions
reproductive_age = 8 #"years"

globals = {} # CURRENT ORDER: [updates_per_year, num_traditions, insitutionlist, reproductive_age]
i =0
globals[i] = updates_per_year
i+=1
globals[i] = num_traditions
i+=1
globals[i] = institutionlist
i+=1
globals[i] = reproductive_age
i+=1
# right now the model thus contains only one institution.

Nmin= 2 #community death threshhold 
Nmax = 50 # community splitting threshold 
community_thresholds = np.array(Nmin,Nmax) # minimun population, maximum population 
#________________________________________________________________________________


Cost_existance = 3*u # (per time unit)
Cost_rep = 10*u #  
Cost_allele = 5 *u
Cost_trad = 2*u # cost of possessing a tradition allele
#Cost_learning ? 


agent_costs = np.array (Cost_rep, Cost_allele, Cost_existance, Cost_trad)


Emin = 10 *u
Erep = Cost_rep + Emin

agent_thresholds = np.array(Emin, Erep) #



# Harvesting parameters ___________________________________________________________________
R = 100*u # energy rate of the available community resource
epsilon = 0.1 # effectivity. the rate with which an agent can access its correspoinding part of the community resource. without the support of an insitutition
m = 0.5 # monopolizability. the rate with which an agent who is at the apex of an institution can access a corresponding part of the resource. 
#NOTE the agents corresponding part of the community resource (R/N_c) will decrease as the community grows. 
# is it reasonable that the monopolizability and effectivity is applied in constant rate on this decreasing quantity?

harvesting = np.array(R, epsilon, m)


# social parameters__________________________________________ 
SLR = 0.2 # rate of learners in community per time unit
socializing = np.array(SLR)
#_________________________________________


globe = Global(globals, community_thresholds,agent_thresholds, agent_costs,harvesting,socializing)


