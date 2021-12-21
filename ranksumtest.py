from scipy.stats import ranksums
instances = ['mtsp51', 'mtsp100', 'mtsp150', 'Pr76', 'Pr152', 'Pr226']
for instance in instances:
    with open(f'baseline_code/min_dis_{instance}.txt', 'r') as f:
        sample1 = list(map(float, f.read().splitlines()))
    with open(f'our_code/min_dis_{instance}.txt', 'r') as f:
        sample2 = list(map(float, f.read().splitlines()))
    print(f'rank result for {instance}: {ranksums(sample1, sample2).pvalue}')