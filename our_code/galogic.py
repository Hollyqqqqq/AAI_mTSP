'''
The main helper class for Genetic Algorithm to perform
crossover, mutation on populations to evolve them
'''
import numpy as np
from population import *
import warnings
warnings.filterwarnings("ignore", category=Warning)

class GA:

    @classmethod
    # Evolve pop
    def evolvePopulation(cls, pop):

        newPopulation = Population(pop.populationSize, False)

        elitismOffset = 0

        # Performs tournament selection followed by crossover to generate child
        # If fittest chromosome has to be passed directly to next generation
        if elitism:
            kFittest = pop.getKFittest(elitismSize)

        for i in range(elitismOffset, newPopulation.populationSize):
            parent1 = cls.tournamentSelection(pop)
            parent2 = cls.tournamentSelection(pop)
            child = cls.crossover(parent1, parent2)
            # Adds child to next generation
            newPopulation.saveRoute(i, child)

        # Performs Mutation
        for i in range(elitismOffset, newPopulation.populationSize):
            cls.mutate(newPopulation.getRoute(i))
        
        pop.dropKWorst(kFittest)

        return newPopulation

    
    # Function to implement TCX crossover operation
    @classmethod
    def crossover(cls, parent1, parent2):

        child = Route()
        for i in range(numTrucks):
            child.route[i].append(DustbinManager.getDustbin(0)) # add same first node for each route
        

        # cut some genes from parent1 to child
        select_genes = []
        for i in range(numTrucks):
            routeLen = parent1.routeLengths[i]
            if routeLen > 1:
                cut1 = random.randint(1, routeLen-1)
                cut2 = random.randint(cut1+1, routeLen)
                cut_genes = parent1.route[i][cut1:cut2]
                child.route[i].extend(cut_genes)
                select_genes.extend(cut_genes)
        

        # add rest genes from parent2 to child
        rest_genes = []
        for i in range(numTrucks):
            for j in range(parent2.routeLengths[i]-1):
                if parent2.route[i][j+1] not in select_genes:
                    rest_genes.append(parent2.route[i][j+1])

        s_index = 0
        for i in range(numTrucks-1):
            e_index = random.randint(s_index, len(rest_genes))
            child.route[i].extend(rest_genes[s_index:e_index])
            s_index = e_index
        child.route[i].extend(rest_genes[s_index:])

        
        # update child routeLengths
        for i in range(numTrucks):
            child.routeLengths[i] = len(child.route[i])
        

        return child

    # Mutation operation
    @classmethod
    def mutate (cls, route):
        if random.uniform(0, 1) > mutationRate:
            return
        if random.uniform(0, 1) <= crossMutateRate:
            cls.mutate_crossRoute(route)
        else:
            cls.interior_mutate(route)


    @classmethod
    def mutate_crossRoute(cls, route):
        index1 = 0
        index2 = 0
        while index1 == index2:
            index1 = random.randint(0, numTrucks - 1)
            index2 = random.randint(0, numTrucks - 1)
        #print ('Indexes selected: ' + str(index1) + ',' + str(index2))

        #generate replacement range for 1
        route1startPos = 0
        route1lastPos = 0
        if route.routeLengths[index1] > 1:
            route1startPos = random.randint(1, route.routeLengths[index1]-1)
            route1lastPos = random.randint(route1startPos, route.routeLengths[index1]-1)

        #generate replacement range for 2
        route2startPos = 0
        route2lastPos = 0
        if route.routeLengths[index2] > 1:
            route2startPos = random.randint(1, route.routeLengths[index2]-1)
            route2lastPos = random.randint(route2startPos, route.routeLengths[index2]-1)

        swap1 = [] # values from 1
        swap2 = [] # values from 2

        
        # pop all the values to be replaced
        for i in range(route1startPos, route1lastPos + 1):
            swap1.append(route.route[index1].pop(route1startPos))

        for i in range(route2startPos, route2lastPos + 1):
            swap2.append(route.route[index2].pop(route2startPos))

        # add to new location by pushing
        route.route[index1][route1startPos:route1startPos] = swap2
        route.route[index2][route2startPos:route2startPos] = swap1

        route.routeLengths[index1] = len(route.route[index1])
        route.routeLengths[index2] = len(route.route[index2])

    @classmethod
    # modified
    # mutate in one salesman's route by swapping two part in the route
    def interior_mutate(cls, route):
        # select a salesman randomly for mutation
        index = random.randint(0, numTrucks - 1)
        while len(route.route[index]) < 3:#the length of the route must be at least 3
            index = random.randint(0, numTrucks - 1)
        # print ('Indexes selected: ' + str(index))

        cut_point = random.sample(range(1, len(route.route[index])), 2)
        cut_point.sort()

        cut_point += random.sample(range(cut_point[0], cut_point[1]), 1)
        cut_point += random.sample(range(cut_point[1], len(route.route[index])), 1)

        swap1 = []  # cut_point[0]~cut_point[2]
        swap2 = []  # cut_point[1]~cut_point[3]

        for i in range(cut_point[1], cut_point[3] + 1):
            swap2.append(route.route[index].pop(cut_point[1]))

        for i in range(cut_point[0], cut_point[2] + 1):
            swap1.append(route.route[index].pop(cut_point[0]))

        route.route[index][cut_point[1] - len(swap1):cut_point[1] - len(swap1)] = swap1
        route.route[index][cut_point[0]:cut_point[0]] = swap2


    # Tournament Selection: choose a random set of chromosomes and find the fittest among them 
    @classmethod
    def tournamentSelection (cls, pop):
        tournament = Population(tournamentSize, False)

        for i in range(tournamentSize):
            randomInt = random.randint(0, pop.populationSize-1)
            tournament.saveRoute(i, pop.getRoute(randomInt))

        fittest = tournament.getKFittest(1)
        return fittest
