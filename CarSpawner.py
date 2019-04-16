import sys, os
import random

if 'SUMO_HOME' in os.environ:
    tools = os.path.join(os.environ['SUMO_HOME'], 'tools')
    sys.path.append(tools)
else:
    sys.exit("please declare environment variable 'SUMO_HOME'")

import traci
import traci.constants as tc

# can also use sumo-gui for GUI demo
# Change the .cfg based on the model being used
traci.start(["sumo", "-c", "sumocfg/freeway.sumo.cfg", "--device.rerouting.probability", "1"])

platoonSize = 7
numCars = 200
numPlatoons = numCars//platoonSize
src = None
dest = None
# Use dir() to get all methods
edgeList = traci.edge.getIDList()
edges = list()

for i in range(len(edgeList)):
    if(edgeList[i][:4] == "edge"):
        edges.append(edgeList[i])

#set routes
for i in range(numPlatoons):
    while src == dest:
        src = random.choice(edges)
        dest = random.choice(edges)
    #route_returned = traci._simulation.SimulationDomain.findRoute(self=???, fromEdge=src, toEdge=dest)
    #print(route_returned)
    traci.route.add("route" + str(i), [src, dest])

#add cars
for i in range(platoonSize):
    for j in range(numPlatoons):
        # "route" + str(j)
        car_return = traci.vehicle.add("car" + str(j) + "_" + str(i), "platoon", typeID="vtypeauto")
        #traci.vehicle.changeTarget()
        # print(car_value)
        while(car_return == tc.RTYPE_ERR):
            traci.simulationStep()

#loop till done
while traci.simulation.getMinExpectedNumber() > 0:
    traci.simulationStep()


#add route
#traci.route.add("trip", ["startEdge", "endEdge"])
#vID, vTypeID, RouteID, laneID, insertPos, insSpeed

#add vehicle
#traci.vehicle.add("newVeh", "trip", typeID="reroutingType")

traci.close()
