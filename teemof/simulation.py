# Date: August 2017
# Author: Kutay B. Sezginel
"""
Simulation class for reading and initializing Lammps simulations
"""
from teemof.read import read_run, read_trial


k_parameters = dict(kb=0.001987, conv=69443.84, dt=5, volume=80 * 80 * 80,
                    temp=300, prefix='J0Jt_t', isotropic=False, average=True)


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
            print('Select setup: "run" "trial" "trial_set"')

    def initialize(self):
        pass
