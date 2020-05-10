 
#define libraries
#from itertools import product
#from sys import stdout as out
#from mip import Model, xsum, minimize, BINARY
import pandas as pd
import pulp as plp
#define input data                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            
data=pd.read_excel(r'Load profiles CHP Office and PV 27-03-20\Load profiles CHP Office and PV 27-03-20.xlsx',sheet_name='data')
N = 5
T = 35040 
set_c = range(1, N+1) #nbr of charging station
set_t = range(0, T) #nbr of set of time
C_pv=40000 #800euro per kwp*50kwp
C_chp=25000 #euro
C_b=600 #euro per kwh
C_cs=24000 #euro
M_pv=800 #euro per year
M_chp= 0.45 #euro per operational hour
N_oph=3886 #operational hours
M_b=5
M_cs=1500 #euro per year
p_ev=3
p_pv=0.092 #ok
p_chp=0.1384 #ok
p_NG=0.0479 #ok
p_NGy=42.27 #natural gas per year
p_el=0.2319 #ok
p_ely=100.98 #price elec per year
LT=1 #years
#eff_b=0,98
C_bmax=100
delta=0.25
 #initial battery capacity
#define objective function
gamma= plp.LpProblem("NPC", plp.LpMinimize)
#define decision variables (power, state of charge)

#PEV= plp.LpVariable.dicts("EV power",[(time) for time in data.index],lowBound=0,upBound=50,cat='continuous')
#PPV= plp.LpVariable.dicts("PV power",((time) for time in data.index),lowBound=0,upBound=50,cat='continuous')
#PL= plp.LpVariable.dicts("load power",((time) for time in data.index),lowBound=0,upBound=6,cat='continuous')
#CHP= plp.LpVariable.dicts("CHP power",((time) for time in data.index),lowBound=0,upBound=9,cat='continuous')

Pg= plp.LpVariable("grid power",[(time) for time in data.index],lowBound=0,upBound=36,
                                     cat='continuous')    #define series of data by tuples

Ncs= plp.LpVariable("number of charging station",lowBound=1,upBound=4,
                                     cat='integer')
Eb= plp.LpVariable("energy of the battery",[(time) for time in data.index],lowBound=0,upBound=C_bmax,
                                     cat='continuous') #define variable as integer
#objective function formula
#gamma+=capital_cost()+maintenance_cost()+fuel_cost()+electricity_cost()-revenues()
gamma +=plp.lpSum([C_pv+C_chp+Nb*C_b+Ncs*C_cs]+[M_pv*LT+M_chp*N_oph+M_b+M_cs*LT]
+[delta*p_NG*data.loc[time,'fuel'] for time in data.index]
+[delta*(p_pv*data.loc[time,'PV']+ p_chp*data.loc[time,'chp']+Ncs*p_ev*data.loc[time,'EV']) for time in data.index]
+[delta*(p_el*data.loc[time,'load']+p_el*data.loc[time,'EV'])+p_ely for time in data.index]
        )
#constraints
for time in data.index:
    gamma += [Ncs*data[time,'power']+ data[time,'load'] == data[time,'chp'] +data[time,'pv']+Pb[time,'Pb']+Pg[time]
    #gamma += Eb[time]== Eb[time-1]-(0.25*Pb[time,'Pb'])
# Solve our problem
gamma.solve()
# Print our decision variable values
for time in data.index:
    Eb_value=Eb[time].varValue
    print "the optimum battery capacity is".format(Eb_value)      

Ncs_value=Ncs.varValue
print "the optimum number of charging station is".format(Ncs_value)
Nb_value=Nb.varValue
print "the optimum number of charging station is".format(Nb_value)


# Print our objective function value
net_present_cost=plp.value(cost.objective)
print "the optimum optimum net present value is".format(net_present_cost)



