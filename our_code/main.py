from galogic import *
import matplotlib.pyplot as plt
import progressbar
import sys
import time
import os

# read console input
instance = sys.argv[1]
runs = 1 if len(sys.argv) <= 2 else int(sys.argv[2])


# read data and add dustbins
with open(f'instances/{instance}.txt','r') as f:
    lines = f.read().splitlines()
    set_numNodes(len(lines) - 1)
    for i in range(1, len(lines)):
        [x, y] = lines[i].split(' ')[1:]
        DustbinManager.addDustbin(Dustbin(float(x), float(y)))


min_dis_list = []
cpu_time_list = []
for r in range(runs):

    print(f'runs {r}')
    pbar = progressbar.ProgressBar()

    random.seed(time.time())
    yaxis = [] # Fittest value (distance)
    xaxis = [] # Generation count

    start = time.process_time()
    
    pop = Population(populationSize, True)
    globalRoute = pop.getKFittest(1)
    init_dis = globalRoute.getDistance()
    global_dis = init_dis

    # Start evolving
    for i in pbar(range(numGenerations)):
        pop = GA.evolvePopulation(pop)
        localRoute = pop.getKFittest(1)
        local_dis = localRoute.getDistance()
        if local_dis < global_dis:
            globalRoute = localRoute
            global_dis = local_dis
        yaxis.append(local_dis)
        xaxis.append(i)

    end = time.process_time()

    min_dis_list.append(global_dis)
    route_str = globalRoute.toString()
    cpu_time = end - start
    cpu_time_list.append(cpu_time)
    print ('Initial minimum distance: ' + str(init_dis))
    print ('Global minimum distance: ' + str(global_dis))
    print ('Final Route: ' + route_str, end='')
    print (f'CPU Time cost: {cpu_time}s')


    if not os.path.isdir(f'{instance}/{r}'):
        os.makedirs(f'{instance}/{r}')

    with open(f'{instance}/{r}/output.txt','w') as f:
        f.write(f'{init_dis}\n')
        f.write(f'{global_dis}\n')
        f.write(route_str)
        f.write(f'{cpu_time}s')

    fig = plt.figure()
    plt.plot(xaxis, yaxis, 'r-')
    plt.savefig(f'{instance}/{r}/evolution.jpg')
    # plt.show()
    
with open(f'min_dis_{instance}.txt','w') as f:
    for d in min_dis_list:
        f.write(f'{d}\n')

print(f'best solution for {r} runs: {min(min_dis_list)}')
print(f'worst solution for {r} runs: {max(min_dis_list)}')
print(f'average solution for {r} runs: {sum(min_dis_list)/len(min_dis_list)}')
print(f'average cpu time for {r} runs: {sum(cpu_time_list)/len(cpu_time_list)}')
with open(f'stat_{instance}.txt','w') as f:
    f.write(f'{min(min_dis_list)}\n')
    f.write(f'{max(min_dis_list)}\n')
    f.write(f'{sum(min_dis_list)/len(min_dis_list)}\n')
    f.write(f'{sum(cpu_time_list)/len(cpu_time_list)}\n')
