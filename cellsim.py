import numpy as np
import scipy
import matplotlib.pyplot as plt
from argparse import ArgumentParser

parser = ArgumentParser(prog = 'python cellsim.py')
parser.add_argument('-s', '--seed', help = 'set seed for deterministic output', type = int)
args = parser.parse_args()

# global variables

board_size = 20       # size for the board
timestep = 0.01     # time step for each update
prob_infected = 0.01    # probability of a cell initially being infected
virus_init = 0.5     # amount of virus of initially infected cells
rate_vv = 0.5           # change rate of virus depending on amount of virus
rate_va = 4             # change rate of virus depending on amount of antibodies
rate_av = 2             # change rate of antibodies depending on amoung of virus
antibody_decay_rate = 0.0       # natural decay for antibodies

threshold_infected = 0.5    # threshold amount of virus for a cell to be infected
threshold_recovered = 0.5   # threshold amount of antibody for a cell to be recovered

rng = np.random.default_rng()   # generates random float distributed uniformly over [0,1)

weight_spread = [[0.3, 0.3, 0.3, 0.3, 0.3],
                [0.3, 0.6, 0.6, 0.6, 0.3],
                [0.3, 0.6, 1.0, 0.6, 0.3],
                [0.3, 0.6, 0.6, 0.6, 0.3],
                [0.3, 0.3, 0.3, 0.3, 0.3]]  # weight for dependency of the change of rate of virus on neighbor cells


class cell:
    def __init__(self, type=None, model="linear"):
        if type == 'infected':
            self.virus_val = virus_init
            self.antibody_val = 0
        elif type == 'recovered':
            self.virus_val = 0
            self.antibody_val = 1
        else:
            if rng.random() < prob_infected:
                self.virus_val = virus_init
            else:
                self.virus_val = 0
            self.antibody_val = 0

    def update_val(self, exposure=0):
        V, A = self.virus_val, self.antibody_val

        # update virus_val according to exposure and A
        deltaV = timestep*(rate_vv*exposure - rate_va*A)
        self.virus_val = max(0.0, min(1.0, V + deltaV))

        # update antibody_val according to V and A
        deltaA = timestep*(rate_av*V - antibody_decay_rate*A)
        self.antibody_val = max(0.0, min(1.0, A + deltaA))
    

class board:
    def __init__(self, size):
        self.size = size
        self.cells = []
        for i in range(size):
            self.cells.append([cell() for j in range(size)])

    def step(self):
        virus_distribution = []
        for row in self.cells:
            virus_distribution.append([c.virus_val for c in row])
        virus_weight = scipy.signal.convolve2d(virus_distribution, weight_spread, 'same')
        for i in range(self.size):
            for j in range(self.size):
                self.cells[i][j].update_val(exposure = virus_weight[i][j])
    
    def population_count(self):
        cnt = {
            'susceptible': 0, 'infected': 0, 'recovered': 0
        }
        for row in self.cells:
            for c in row:
                if c.virus_val >= threshold_infected:
                    cnt['infected'] += 1
                elif c.antibody_val >= threshold_recovered:
                    cnt['recovered'] += 1
                else:
                    cnt['susceptible'] += 1
        return cnt

if __name__ == '__main__':
    if type(args.seed) == int:
        rng = np.random.default_rng(seed = args.seed)

    sim = board(board_size)
    for d in range(1000):
        sim.step()
        if d % 50 == 0:
            pop_cnt = sim.population_count()
            print(f'Day {d}: {pop_cnt['susceptible']} susceptible, {pop_cnt['infected']} infected, {pop_cnt['recovered']} recovered')
    
    # TODO: visualize data
