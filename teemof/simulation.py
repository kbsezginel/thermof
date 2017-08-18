# Date: August 2017
# Author: Kutay B. Sezginel
"""
Simulation class for reading and initializing Lammps simulations
"""
import pprint
from teemof.read import read_run, read_trial, read_trial_set
from teemof.parameters import k_parameters


class Simulation:
    """
    Reading and initializing Lammps simulations
    """
    def __init__(self, read=None, setup=None, parameters=k_parameters):
        self.parameters = parameters
        if read is not None and setup is not None:
            self.read(read, setup)

    def read(self, sim_dir, setup='run'):
        if setup == 'run':
            self.run = read_run(sim_dir, k_par=self.parameters)
        elif setup == 'trial':
            self.trial = read_trial(sim_dir, k_par=self.parameters)
        elif setup == 'trial_set':
            self.trial_set = read_trial_set(sim_dir, k_par=self.parameters)
        else:
            print('Select setup: "run" | "trial" | "trial_set"')

    def show_parameters(self):
        pprint.pprint(self.parameters)

    def initialize(self):
        pass
