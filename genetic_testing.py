import os, sys
import random

from deap import base
from deap import creator
from deap import tools

# if 'SUMO_HOME' in os.environ:
#     tools = os.path.join(os.environ['SUMO_HOME'], 'tools')
#     sys.path.append(tools)
# else:
#     sys.exit("please declare environment variable 'SUMO_HOME'")
#
# import traci
# import traci.constants as tc

max_cars = 100
IND_SIZE=1

def evaluate(individual):
    # Run each simulation for an individual here

    # Find individual fitness here
    return fit_value

creator.create("FitnessMax", base.Fitness, weights=(1.0,))
creator.create("Individual", list, fitness=creator.FitnessMax)
toolbox = base.Toolbox()
toolbox.register("attr_float", random.random)
toolbox.register("individual", tools.initRepeat, creator.Individual, toolbox.attr_float, n=IND_SIZE)

