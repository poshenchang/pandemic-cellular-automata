import numpy as np
import scipy
import matplotlib.pyplot as plt
from argparse import ArgumentParser

parser = ArgumentParser(prog = 'python cellsim.py')
parser.add_argument('-s', '--seed', help = 'set seed for deterministic output', type = int)
args = parser.parse_args()

# global variables

board_size = 20                 # size for the board
scale_factor = 0.5              # scale factor of change in virus_val and antibody_val
precision = 100                 # number of steps a day is divided into
attr_variation = 0.3            # variation of attributes of individual cells
fluctuation = 0.1               # randomness within value update
prob_infected = 0.01            # probability of a cell initially being infected
virus_init = 0.01               # amount of virus of initially infected cells
rate_vv = 0.5                   # change rate of virus depending on amount of virus
rate_va = 3.1                   # change rate of virus depending on amount of antibodies
rate_av = 3.0                   # change rate of antibodies depending on amount of virus
antibody_decay_rate = 0.01      # natural decay for antibodies
saturation_param = 0.5          # saturation parameter for antibody production

threshold_infected = 0.2        # threshold amount of virus for a cell to be infected
threshold_recovered = 0.5       # threshold amount of antibody for a cell to be recovered

rng = np.random.default_rng()   # generates random float distributed uniformly over [0,1)

weight_spread = [[0.1, 0.1, 0.1, 0.1, 0.1],
                [0.1, 0.3, 0.3, 0.3, 0.1],
                [0.1, 0.3, 1.0, 0.3, 0.1],
                [0.1, 0.3, 0.3, 0.3, 0.1],
                [0.1, 0.1, 0.1, 0.1, 0.1]]  # weight for dependency of the change of rate of virus on neighbor cells


class cell:
    def __init__(self, type=None, model="linear"):
        # initialize model type
        # linear: dV and dA are linear in virus_val and antibody_val
        # saturation: include saturation of antibody production
        self.model = model
        # cell parameters
        self.rate_vv = np.random.lognormal(np.log(rate_vv), attr_variation)
        self.rate_va = np.random.lognormal(np.log(rate_va), attr_variation)
        self.rate_av = np.random.lognormal(np.log(rate_av), attr_variation)

        # initialize virus_val and antibody_val according to cell type
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
    
    def __delta_virus(self, exposure=0):
        if self.model == "linear":
            return self.rate_vv*exposure - self.rate_va*self.antibody_val*self.virus_val
        elif self.model == "saturation":
            return self.rate_vv*exposure - self.rate_va*self.antibody_val*self.virus_val
        else:
            return 0
    
    def __delta_antibody(self):
        if self.model == "linear":
            return self.rate_av*self.virus_val - antibody_decay_rate*self.antibody_val
        elif self.model == "saturation":
            return self.rate_av*self.virus_val/(1 + saturation_param*self.virus_val) - antibody_decay_rate*self.antibody_val
        else:
            return 0
    
    def update_val(self, exposure=0):
        V, A = self.virus_val, self.antibody_val

        # compute deltaV and delta_antibody
        fluct = np.random.lognormal(0, fluctuation)
        deltaV = fluct * scale_factor * self.__delta_virus(exposure) / precision
        deltaA = fluct * scale_factor * self.__delta_antibody() / precision

        # update virus_val and antibody_val
        self.virus_val = max(0.0, min(1.0, V + deltaV))
        self.antibody_val = max(0.0, min(1.0, A + deltaA))
    

class board:
    def __init__(self, size, model="linear"):
        self.size = size
        self.model = model
        self.cells = []
        for i in range(size):
            self.cells.append([cell(model=self.model) for j in range(size)])

    def step(self):
        for _ in range(precision):
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
    
    def run(self, num_days=100, print_count=10, plot=True):
        sus = np.zeros(num_days)
        inf = np.zeros(num_days)
        rec = np.zeros(num_days)
        x = np.array(range(num_days))
        for d in range(num_days):
            self.step()
            pop_cnt = self.population_count()
            if print_count > 0 and d % print_count == 0:
                print(f'Day {d}: {pop_cnt['susceptible']} susceptible, '
                               f'{pop_cnt['infected']} infected, '
                               f'{pop_cnt['recovered']} recovered')
            sus[d] = pop_cnt['susceptible']
            inf[d] = pop_cnt['infected']
            rec[d] = pop_cnt['recovered']
        if plot:
            y = np.vstack((inf, rec, sus))
            fig, ax = plt.subplots()
            ax.stackplot(x, y, labels=('infected', 'recovered', 'susceptible'))
            plt.xlabel('Days')
            plt.ylabel('Population')
            plt.legend()
            plt.show()

        return sus, inf, rec

    def run_multiple_rand(self, num_days=100, num_runs=10, plot=True):
        sus = [np.zeros(num_days) for _ in range(num_runs)]
        inf = [np.zeros(num_days) for _ in range(num_runs)]
        rec = [np.zeros(num_days) for _ in range(num_runs)]
        x = np.array(range(num_days))
        for i in range(num_runs):
            self.__init__(self.size)
            sus[i], inf[i], rec[i] = self.run(num_days, print_count=0, plot=False)
            if plot:
                plt.plot(x, sus[i], color='blue', linewidth='0.5')
                plt.plot(x, inf[i], color='orange', linewidth='0.5')
                plt.plot(x, rec[i], color='green', linewidth='0.5')
            print(f'Run {i+1} successful')
        if plot:
            plt.xlabel('Days')
            plt.ylabel('Population')
            plt.show()
        return sus, inf, rec


if __name__ == '__main__':
    if type(args.seed) == int:
        rng = np.random.default_rng(seed = args.seed)

    sim = board(board_size, model="saturation")
    sim.run(50)
    
    # TODO: simulation log
    # TODO: visualize data
