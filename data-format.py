import numpy as np
from argparse import ArgumentParser
import pandas as pd
import matplotlib.pyplot as plt
import json

parser = ArgumentParser(prog='python data-format.py')
parser.add_argument('infile', help='input csv file for fittting', type=str)
args = parser.parse_args()

Taipei_population = 2,480,681
start_date = '2022-03-20'

if __name__ == '__main__':
    infected_cnt = np.zeros(250)
    df = pd.read_csv(args.infile)
    L = list(df.loc[:, 'Number of Cases'].values)
    nL = L
    for i in range(len(L)-7):
        nL[i] = np.mean(np.array(L[i:i+7]))
    L = nL[79 : 79+250]
    plt.plot(range(250), L)
    plt.show()
    pathname = args.infile[:-4] + ".json"
    with open(pathname, "w") as outfile:
        outfile.write(json.dumps(L))