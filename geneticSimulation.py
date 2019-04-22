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

#from deap import base
#from deap import creator
#from deap import tools

LENGTH=4
gui_mode = True


def remove(vehID, reason):
    traci._sendByteCmd(tc.CMD_SET_VEHICLE_VARIABLE, tc.REMOVE, vehID, reason)

def run_sumo_iteration(speed, platoon_size, distance):
    if gui_mode == True:
        traci.start(["sumo-gui", "-c", "cfg/freeway.sumo.cfg"])
    else:
        traci.start(["sumo", "-c", "cfg/freeway.sumo.cfg"])
    
    plexe = Plexe()
    traci.addStepListener(plexe)
    max_cars = 50
    total_cars = 0
    total_fuel_used = 0
    num_platoons = max_cars // platoon_size
    src = None
    dest = None
    edge_list = traci.edge.getIDList()
    edges_start = list()
    edges_end = list()
    

    for i in range(len(edge_list)):
        if(edge_list[i][:4] == "edge"):
            edges_start.append(edge_list[i])
            edges_end.append(edge_list[i])
            

    for i in range(num_platoons):
        route_returned = traci.simulation.findRoute(fromEdge="edge_0_0", toEdge="absorption_0")
        traci.route.add("route" + str(i), route_returned.edges)
        LEADER = "car0_" + str(i)

        spawn_offset = (num_platoons - i + 1) * 2 * ((platoon_size + 1) * (distance + LENGTH))

        # Add platoon_size cars to a platoon
        for j in range(platoon_size):
            total_cars += 1
            vid = "car" + str(j) + "_" + str(i)
            add_platooning_vehicle(plexe, vid, spawn_offset - j * (distance + LENGTH), 0, speed, distance, False, route="route" + str(i))
            plexe.set_fixed_lane(vid, 0, safe=False)
            traci.vehicle.setSpeedMode(vid, 0)
            if j == 0:
                plexe.set_active_controller(vid, ACC)
                # Disable the ability to change lanes due to cars being dumb and changing lanes to get off on an off-ramps
                plexe.enable_auto_lane_changing(LEADER, False)
                #print("Creating leader of platoon: ", vid)
            else:
                plexe.set_active_controller(vid, CACC)
                plexe.enable_auto_feed(vid, True, leader_id=LEADER, front_id="car" + str(j-1) + "_" + str(i))
                plexe.add_member(LEADER, vid, i)
                #print("Adding member to platoon ", LEADER, " | ", vid)
            if total_cars > max_cars:
                break

    #print(total_cars)

    #first_itteration = True
    #loop till done
    while traci.simulation.getMinExpectedNumber() > 0:
        #if first_itteration == True and gui_mode == True:
             #first_itteration == False
             #traci.gui.trackVehicle("View #0", "car0_0")
             #traci.gui.setZoom("View #0", 3000)
        
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






run_sumo_iteration(36, 25, 1);

























