from galogic import *
import matplotlib.pyplot as plt
import progressbar
import sys
import time
import os

pbar = progressbar.ProgressBar()

# Add Dustbins
instance = sys.argv[1]
with open(f'instances/{instance}.txt','r') as f:
    lines = f.read().splitlines()
    set_numNodes(len(lines) - 1)
    for i in range(1, len(lines)):
        [x, y] = lines[i].split(' ')[1:]
        RouteManager.addDustbin(Dustbin(float(x), float(y)))

runs = 1 if len(sys.argv) <= 2 else sys.argv[2]
if not os.path.isdir(f'./{instance}'):
    os.mkdir(f'{instance}')
for r in range(runs):
    with open(f'{instance}/{r}.txt','w') as f:
        random.seed(seedValue)
        yaxis = [] # Fittest value (distance)
        xaxis = [] # Generation count

        start = time.process_time()
        
        pop = Population(populationSize, True)
        globalRoute = pop.getFittest()
        init_dis = globalRoute.getDistance()
        print ('Initial minimum distance: ' + str(init_dis))
        f.write(f'{init_dis}\n')

        # Start evolving
        for i in pbar(range(numGenerations)):
            pop = GA.evolvePopulation(pop)
            localRoute = pop.getFittest()
            if globalRoute.getDistance() > localRoute.getDistance():
                globalRoute = localRoute
            yaxis.append(localRoute.getDistance())
            xaxis.append(i)

        end = time.process_time()

        min_dis = globalRoute.getDistance()
        route_str = globalRoute.toString()
        cpu_time = end - start
        print ('Global minimum distance: ' + str(min_dis))
        print ('Final Route: ' + route_str)
        print (f'Time cost: {cpu_time}s')
        f.write(f'{min_dis}\n')
        f.write(route_str)
        f.write(f'{cpu_time}s')

        fig = plt.figure()

        plt.plot(xaxis, yaxis, 'r-')
        plt.savefig(f'{instance}/{r}.jpg')
        # plt.show()
