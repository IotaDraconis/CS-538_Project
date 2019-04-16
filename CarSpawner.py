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
traci.start(["sumo-gui", "-c", "sumocfg/freeway-manual.sumo.cfg"])

platoonSize = 7
numCars = 200
numPlatoons = numCars//platoonSize
src = None
dest = None
# Use dir() to get all methods
edgeList = traci.edge.getIDList()
#edgeList = list()

#for id in edgeList_original:
#    if id[:4] == "edge":
#        edgeList.append(id)

#set routes
for i in range(numPlatoons):
    while src == dest:
        src = random.choice(edgeList)
        dest = random.choice(edgeList)
    traci.route.add("route" + str(i), [src, dest])

#add cars
for i in range(platoonSize):
    for j in range(numPlatoons):
        # "route" + str(j)
        car_value = traci.vehicle.add("car" + str(j) + "_" + str(i), "platoon_route", typeID="vtypeauto")
        # print(car_value)
        while(car_value == tc.RTYPE_ERR):
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
