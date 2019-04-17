import os, sys
import random

import sys, os
import random

if 'SUMO_HOME' in os.environ:
    tools = os.path.join(os.environ['SUMO_HOME'], 'tools')
    sys.path.append(tools)
else:
    sys.exit("please declare environment variable 'SUMO_HOME'")

import traci
import traci.constants as tc

import simpla

from deap import base
from deap import creator
from deap import tools

IND_SIZE=1

def run_sumo_iteration(platoon_size):
    traci.start(["sumo", "-c", "sumocfg/freeway.sumo.cfg"])
    num_cars = 100
    num_platoons = num_cars // platoon_size
    src = None
    dest = None
    edge_list = traci.edge.getIDList()
    edges = list()

    for i in range(len(edge_list)):
        if(edge_list[i][:4] == "edge"):
            edges.append(edge_list[i])

    #set routes
    for i in range(num_platoons):
        route_found = False
        #while(route_found == False):
        #    src = random.choice(edges)
        #    dest = random.choice(edges)
        #    if(src != dest):
        #        route_returned = traci.simulation.findRoute(fromEdge=src, toEdge=dest)
        #        # print(route_returned.edges)
        #        if(route_returned.edges != []):
        #            route_found = True
        #            # print("Route was found for a platoon!!!")
        route_returned = traci.simulation.findRoute(fromEdge="edge_0_0", toEdge="edge_2_2")
        traci.route.add("route" + str(i), route_returned.edges)

    total_fuel_used = 0

    #add cars
    for i in range(platoon_size):
        for j in range(num_platoons):
            # "route" + str(j)
            car_return = traci.vehicle.add("car" + str(j) + "_" + str(i), "route" + str(j), typeID="vtypeauto")
            #traci.vehicle.changeTarget()
            # print(car_value)
            while(car_return == tc.RTYPE_ERR):
                for id in traci.vehicle.getIDList():
                    total_fuel_used += traci.vehicle.getFuelConsumption(id)
                
                traci.simulationStep()
    

    #loop till done
    while traci.simulation.getMinExpectedNumber() > 0:
        for id in traci.vehicle.getIDList():
            total_fuel_used += traci.vehicle.getFuelConsumption(id)
        #        getFuelConsumption
        #        getCO2Emission
        #        getCOEmission
        #        getHCEmission
        #        getNOxEmission
        #        getNoiseEmission
        #        getPMxEmission
        traci.simulationStep()
    
    print("\n\n\n\n\n\n\n\n")
    print(total_fuel_used)
    
    traci.close()
    

def evaluate(individual):
    # Run each simulation for an individual here
    # Find individual fitness here
    return fit_value

creator.create("FitnessMax", base.Fitness, weights=(1.0,))
creator.create("Individual", list, fitness=creator.FitnessMax)
toolbox = base.Toolbox()
toolbox.register("attr_float", random.random)
toolbox.register("individual", tools.initRepeat, creator.Individual, toolbox.attr_float, n=IND_SIZE)



run_sumo_iteration(1);

























