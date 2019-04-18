import sys, os
import random

if 'SUMO_HOME' in os.environ:
    tools = os.path.join(os.environ['SUMO_HOME'], 'tools')
    sys.path.append(tools)
else:
    sys.exit("please declare environment variable 'SUMO_HOME'")

import traci
import traci.constants as tc

from plexe import Plexe, ACC, CACC
sys.path.append(os.path.abspath("/home/user/Documents/plexe-pyapi/examples"))
from utils import add_platooning_vehicle

from deap import base
from deap import creator
from deap import tools

IND_SIZE=1
LENGTH=4
DISTANCE=5  # Possible tuing parameter for the GA
SPEED = 25


def run_sumo_iteration(platoon_size):
    traci.start(["sumo-gui", "-c", "sumocfg/freeway.sumo.cfg"])
    plexe = Plexe()
    traci.addStepListener(plexe)
    num_cars = 100
    total_fuel_used = 0
    num_platoons = num_cars // platoon_size
    src = None
    dest = None
    edge_list = traci.edge.getIDList()
    edges = list()

    for i in range(len(edge_list)):
        if(edge_list[i][:4] == "edge"):
            edges.append(edge_list[i])

    for i in range(num_platoons):
        # Find a route for each platoon
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
        
        LEADER = "car0_" + str(i)
        
        # Add platoon_size cars to a platoon
        for j in range(platoon_size):
            vid = "car" + str(j) + "_" + str(i)
            add_platooning_vehicle(plexe, vid, 140 - j * (DISTANCE + LENGTH), 0, SPEED, DISTANCE, False)
            plexe.set_fixed_lane(vid, 0, safe=False)
            traci.vehicle.setSpeedMode(vid, 0)
            if i == 0:
                plexe.set_active_controller(vid, ACC)
                plexe.enable_auto_lane_changing(LEADER, True)
            else:
                plexe.set_active_controller(vid, CACC)
                plexe.enable_auto_feed(vid, True, LEADER, vid)
                plexe.add_member(LEADER, vid, i)


    #first_itteration = True
    #loop till done
    while traci.simulation.getMinExpectedNumber() > 0:
        #if first_itteration == True:
            #first_itteration == False
            #traci.gui.trackVehicle("View #0", "car0_0")
    
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

























