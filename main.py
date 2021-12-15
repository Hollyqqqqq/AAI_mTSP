from galogic import *
import matplotlib.pyplot as plt
import progressbar
import sys
import time
import os

# read console input
instance = sys.argv[1]
runs = 1 if len(sys.argv) <= 2 else int(sys.argv[2])
method = 'baseline' if len(sys.argv) <= 3 else sys.argv[3].lower()


# read data and add dustbins
with open(f'instances/{instance}.txt','r') as f:
    lines = f.read().splitlines()
    set_numNodes(len(lines) - 1)
    for i in range(1, len(lines)):
        [x, y] = lines[i].split(' ')[1:]
        RouteManager.addDustbin(Dustbin(float(x), float(y)))


min_dis_list = []
for r in range(runs):

    print(f'runs {r}')
    pbar = progressbar.ProgressBar()

    # random.seed(seedValue)
    yaxis = [] # Fittest value (distance)
    xaxis = [] # Generation count

    start = time.process_time()
    
    pop = Population(populationSize, True)
    globalRoute = pop.getFittest()
    init_dis = globalRoute.getDistance()

    # Start evolving
    for i in pbar(range(numGenerations)):
        pop = GA.evolvePopulation(pop, method)
        localRoute = pop.getFittest()
        if globalRoute.getDistance() > localRoute.getDistance():
            globalRoute = localRoute
        yaxis.append(localRoute.getDistance())
        xaxis.append(i)

    end = time.process_time()

    min_dis = globalRoute.getDistance()
    min_dis_list.append(min_dis)
    route_str = globalRoute.toString()
    cpu_time = end - start
    print ('Initial minimum distance: ' + str(init_dis))
    print ('Global minimum distance: ' + str(min_dis))
    print ('Final Route: ' + route_str, end='')
    print (f'CPU Time cost: {cpu_time}s')


    if not os.path.isdir(f'{method}/{instance}/{r}'):
        os.makedirs(f'{method}/{instance}/{r}')

    with open(f'{method}/{instance}/{r}/output.txt','w') as f:
        f.write(f'{init_dis}\n')
        f.write(f'{min_dis}\n')
        f.write(route_str)
        f.write(f'{cpu_time}s')

    fig = plt.figure()
    plt.plot(xaxis, yaxis, 'r-')
    plt.savefig(f'{method}/{instance}/{r}/evolution.jpg')
    # plt.show()
    
with open(f'{method}/min_dis_{instance}.txt','w') as f:
    for d in min_dis_list:
        f.write(f'{d}\n')
