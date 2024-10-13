import numpy as np
import scipy
import matplotlib.pyplot as plt
from argparse import ArgumentParser

parser = ArgumentParser(prog = 'python cellsim.py')
parser.add_argument('-s', '--seed', help = 'set seed for deterministic output', type = int)
args = parser.parse_args()

# global variables

LANDSIZE = 20       # size for the landscape
timestep = 0.01     # time step for each update
pInfected = 0.01    # probability of a cell initially being infected
virusInit = 0.5     # amount of virus of initially infected cells
rVV = 0.5           # change rate of virus depending on amount of virus
rVA = 4             # change rate of virus depending on amount of antibodies
rAV = 2             # change rate of antibodies depending on amoung of virus
AbDecay = 0.0       # natural decay for antibodies

THInfected = 0.5    # threshold amount of virus for a cell to be infected
THRecovered = 0.5   # threshold amount of antibody for a cell to be recovered

rng = np.random.default_rng()   # generates random float distributed uniformly over [0,1)

spreadWeight = [[0.3, 0.3, 0.3, 0.3, 0.3],
                [0.3, 0.6, 0.6, 0.6, 0.3],
                [0.3, 0.6, 1.0, 0.6, 0.3],
                [0.3, 0.6, 0.6, 0.6, 0.3],
                [0.3, 0.3, 0.3, 0.3, 0.3]]  # weight for dependency of the change of rate of virus on neighbor cells


class cell:
    def __init__(self, type = None):
        if type == 'infected':
            self.virus_val = virusInit
            self.antibody_val = 0
        elif type == 'recovered':
            self.virus_val = 0
            self.antibody_val = 1
        else:
            if rng.random() < pInfected:
                self.virus_val = virusInit
            else:
                self.virus_val = 0
            self.antibody_val = 0
    
    def updateVal(self, exposure = 0):
        V, A = self.virus_val, self.antibody_val

        # update virus_val according to exposure and A
        self.virus_val = min(1.0, V + timestep*(rVV*exposure - rVA*A))
        self.virus_val = max(0.0, self.virus_val)

        # update antibody_val according to V and A
        self.antibody_val = min(1.0, A + timestep*(rAV*V - AbDecay*A))
        self.virus_val = max(0.0, self.virus_val)
    

class landscape:
    def __init__(self, size):
        self.size = size
        self.cells = []
        for i in range(size):
            self.cells.append([cell() for j in range(size)])

    def step(self):
        virusAmount = []
        for row in self.cells:
            virusAmount.append([c.virus_val for c in row])
        virusWeight = scipy.signal.convolve2d(virusAmount, spreadWeight, 'same')
        for i in range(self.size):
            for j in range(self.size):
                self.cells[i][j].updateVal(exposure = virusWeight[i][j])
    
    def populationCount(self):
        cnt = {
            'susceptible': 0, 'infected': 0, 'recovered': 0
        }
        for row in self.cells:
            for c in row:
                if c.virus_val >= THInfected:
                    cnt['infected'] += 1
                elif c.antibody_val >= THRecovered:
                    cnt['recovered'] += 1
                else:
                    cnt['susceptible'] += 1
        return cnt

if __name__ == '__main__':
    if type(args.seed) == int:
        rng = np.random.default_rng(seed = args.seed)

    L = landscape(LANDSIZE)
    for d in range(1000):
        L.step()
        if d % 50 == 0:
            popCnt = L.populationCount()
            print(f'Day {d}: {popCnt['susceptible']} susceptible, {popCnt['infected']} infected, {popCnt['recovered']} recovered')
    
    # TODO: visualize data
