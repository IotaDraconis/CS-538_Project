import sys, os
import random

if 'SUMO_HOME' in os.environ:
    tools = os.path.join(os.environ['SUMO_HOME'], 'tools')
    sys.path.append(tools)
else:
    sys.exit("please declare environment variable 'SUMO_HOME'")

import traci
import traci.constants as tc

for option in dir(traci):
    print(option)
    for option2 in dir(option):
        print(option2)
        print(dir(option2))
        print("\n")
