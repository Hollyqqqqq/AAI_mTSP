import random
import math
'''
Contains all global variables specific to simulation
'''
# problem size var
numNodes = 200
numTrucks = 5

# GA size var
populationSize = 100
numGenerations = 200

# initial var
KMeansSize = 20

# crossover var
elitism = True
elitismSize = 5
tournamentSize = 10

# mutation var
mutationRate = 0.03
crossMutateRate = 0.5


def random_range(n, total):
    """Return a randomly chosen list of n positive integers summing to total.
    Each such list is equally likely to occur."""

    dividers = sorted(random.sample(range(1, total), n - 1))
    return [a - b for a, b in zip(dividers + [total], [0] + dividers)]

# Randomly distribute number of dustbins to subroutes
# Maximum and minimum values are maintained to reach optimal result
def route_lengths():
    upper = (numNodes + numTrucks - 1)
    fa = upper/numTrucks*1.6 # max route length
    fb = upper/numTrucks*0.6 # min route length
    a = random_range(numTrucks, upper)
    while 1:
        if all( i < fa and i > fb  for i in a):
                break
        else:
                a = random_range(numTrucks, upper)
    return a
    # a = []
    # length = math.floor(numNodes/numTrucks)
    # last = numNodes - length*(numTrucks-1)
    # for i in range(numTrucks-1):
    #     a.append(length)
    # a.append(last)
    # return a

# change numNodes
def set_numNodes(num):
    global numNodes
    numNodes = num

# get numNodes
def get_numNodes():
    return numNodes