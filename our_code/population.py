'''
Collection of routes (chrmosomes)
'''
import numpy as np
from route import *
from sklearn.cluster import KMeans

class Population:
    routes = []
    # Good old contructor
    def __init__ (self, populationSize, initialise):
        self.populationSize = populationSize
        if initialise:
            self.routes.clear()
            self.generateRoutes()

    # Saves the route passed as argument at index
    def saveRoute (self, index, route):
        self.routes[index] = route

    # Returns route at index
    def getRoute (self, index):
        return self.routes[index]

    # Returns k routes with first k fitnesses value
    def getKFittest(self, k):
        kFittest = []
        kFittest.extend(self.routes[:k])
        kFitness = []
        for j in range(k):
            kFitness.append(kFittest[j].getFitness())
        for i in range(1, self.populationSize):
            curr_fitness = self.getRoute(i).getFitness()
            if kFitness[j%k] < curr_fitness:
                kFittest[j%k] = self.getRoute(i)
                kFitness[j%k] = curr_fitness
                j += 1
        if k == 1:
            return kFittest[0]
        return kFittest


    def dropKWorst(self, elitisms):
        k = len(elitisms)
        kWorst = []
        kWorst.extend(self.routes[:k])
        kFitness = []
        kIndex = []
        for j in range(k):
            kFitness.append(kWorst[j].getFitness())
            kIndex.append(j)
        for i in range(1, self.populationSize):
            curr_fitness = self.getRoute(i).getFitness()
            if kFitness[j%k] > curr_fitness:
                kWorst[j%k] = self.getRoute(i)
                kFitness[j%k] = curr_fitness
                kIndex[j%k] = i
                j += 1
        for i in range(k):
            self.saveRoute(kIndex[i], elitisms[i])


    def generateRoutes(self):
        # kmeans initial
        kmeans = KMeans(n_clusters=numTrucks).fit(DustbinManager.getAllDustbinsPos()[1:])
        for i in range(KMeansSize):
            newRoute = Route()
            newRoute.generateIndividualKmeans(kmeans.labels_)
            self.routes.append(newRoute)
        # random initial
        for i in range(populationSize-KMeansSize):
            newRoute = Route() # Create empty route
            newRoute.generateIndividual() # Add route sequences
            self.routes.append(newRoute) # Add route to the population
