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
traci.start(["sumo", "-c", "sumocfg/freeway-manual.sumo.cfg"])

platoonSize = 7
numCars = 200
numPlatoons = numCars//platoonSize
src = None
dest = None
# Use dir() to get all methods
edgeList_original = traci.edge.getIDList()
edgeList = list()

print(edgeList_original)

for id in edgeList_original:
    if id[:4] == "edge":
        edgeList.append(id)

print(edgeList)

#set routes
for i in range(numPlatoons):
    while src == dest:
        src = random.choice(edgeList)
        dest = random.choice(edgeList)
    traci.route.add("route" + str(i), [src, dest])

#add cars
for i in range(platoonSize):
    for j in range(numPlatoons):
        while(traci.vehicle.add("car" + str(j) + "_" + str(i), "route" + str(j), typeID="vtypeauto") == traci.RTYPE_ERR):
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
