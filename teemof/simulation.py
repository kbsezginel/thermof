# Date: August 2017
# Author: Kutay B. Sezginel
"""
Simulation class for reading and initializing Lammps simulations
"""
import pprint
from teemof.read import read_run, read_trial, read_trial_set
from teemof.parameters import k_parameters, plot_parameters
from teemof.visualize import plot_thermal_conductivity, plot_distance_histogram, plot_thermo


class Simulation:
    """
    Reading and initializing Lammps simulations
    """
    def __init__(self, read=None, setup=None, parameters=k_parameters.copy()):
        """
        Create a Lammps simulation object.
        """
        self.parameters = parameters
        self.plot_parameters = plot_parameters.copy()
        if read is not None and setup is not None:
            self.read(read, setup)
            self.setup = setup

    def read(self, sim_dir, setup='run'):
        """
        Read Lammps simulation results from given directory.
        """
        self.setup = setup
        if setup == 'run':
            self.run = read_run(sim_dir, k_par=self.parameters)
        elif setup == 'trial':
            self.trial = read_trial(sim_dir, k_par=self.parameters)
        elif setup == 'trial_set':
            self.trial_set = read_trial_set(sim_dir, k_par=self.parameters)
        else:
            print('Select setup: "run" | "trial" | "trial_set"')

    def initialize(self):
        """
        Initialize input files for a Lammps simulation.
        """
        pass

    def plot(self, selection):
        """
        Plot Lammps simulation results.
        """
        if selection == 'k':
            plot_data = {}
            plot_data['x'] = self.trial['data']['Run1']['time']
            plot_data['y'] = [self.trial['data'][run]['k']['iso'] for run in self.trial['runs']]
            plot_data['legend'] = self.trial['runs']
            plot_thermal_conductivity(plot_data, self.plot_parameters['k'])
        elif selection == 'hist':
            plot_data = {}
            plot_distance_histogram(plot_data, self.plot_parameters['hist'])
        elif selection == 'thermo':
            plot_thermo(self.run['thermo'], self.plot_parameters['thermo'])
        else:
            print('Select plot: "k" | "k_est" | "hist"')

    def show_parameters(self):
        """
        Show thermal conductivity parameters.
        """
        pprint.pprint(self.parameters)

    def show_plot_parameters(self):
        """
        Show plot parameters.
        """
        pprint.pprint(self.plot_parameters)
