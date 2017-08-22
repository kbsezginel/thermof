# Date: August 2017
# Author: Kutay B. Sezginel
"""
Simulation class for reading and initializing Lammps simulations
"""
import pprint
from teemof.read import read_run, read_trial, read_trial_set
from teemof.parameters import k_parameters, plot_parameters
from teemof.visualize import plot_thermal_conductivity, plot_distance_histogram, plot_thermo
from teemof.visualize import subplot_thermal_conductivity


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

    def plot(self, selection, data=None):
        """
        Plot Lammps simulation results.
        """
        if data is None:
            plot_data = self.get_plot_data(plot=selection)
        else:
            plot_data = data
        if selection == 'k':
            plot_thermal_conductivity(plot_data, self.plot_parameters['k'])
        elif selection == 'hist':
            plot_distance_histogram(plot_data, self.plot_parameters['hist'])
        elif selection == 'thermo':
            plot_thermo(plot_data, self.plot_parameters['thermo'])
        elif selection == 'k_sub':
            subplot_thermal_conductivity(plot_data, self.plot_parameters['k_sub'])
        else:
            print('Select plot: "k" | "k_sub" | "hist" | "thermo"')

    def get_plot_data(self, plot='k', setup=None):
        """
        Pulls corresponding data for selected plot.
        """
        plot_data = {}
        if setup is None:
            setup = self.setup
        if plot == 'k':
            if setup == 'run':
                plot_data = dict(x=self.run['time'], legend=self.run['directions'])
                plot_data['y'] = [self.run['k'][d] for d in self.run['directions']]
            elif setup == 'trial':
                plot_data = dict(x=self.trial['data']['Run1']['time'], legend=self.trial['runs'])
                plot_data['y'] = [self.trial['data'][run]['k']['iso'] for run in self.trial['runs']]
            elif setup == 'trial_set':
                ref_run = self.trial_set['data'][self.trial_set['trials'][0]]['runs'][0]
                ref_trial = self.trial_set['trials'][0]
                plot_data['x'] = self.trial_set['data'][ref_trial]['data'][ref_run]['time']
                plot_data['y'] = [self.trial_set['data'][trial]['avg']['k']['iso'] for trial in self.trial_set['trials']]
                plot_data['legend'] = self.trial_set['trials']
        elif plot == 'k_sub':
            if setup == 'run':
                plot_data = dict(x=self.run['time'], legend=self.run['directions'])
                plot_data['y'] = [self.run['k'][d] for d in self.run['directions']]
            elif setup == 'trial':
                plot_data = dict(x=self.trial['data']['Run1']['time'], legend=self.trial['runs'])
                plot_data['y'] = [self.trial['data'][run]['k']['iso'] for run in self.trial['runs']]
            elif setup == 'trial_set':
                ref_run = self.trial_set['data'][self.trial_set['trials'][0]]['runs'][0]
                ref_trial = self.trial_set['trials'][0]
                plot_data['x'] = self.trial_set['data'][ref_trial]['data'][ref_run]['time']
                plot_data['y'] = [self.trial_set['data'][trial]['avg']['k']['iso'] for trial in self.trial_set['trials']]
                plot_data['legend'] = self.trial_set['trials']
        elif plot == 'thermo':
            if setup == 'run':
                self.plot_parameters['thermo']['title'] = self.run['name']
                plot_data = self.run['thermo']
            elif setup == 'trial':
                self.plot_parameters['thermo']['title'] = '%s' % (self.trial['runs'][0])
                plot_data = self.trial['data'][self.trial['runs'][0]]['thermo']
            elif setup == 'trial_set':
                ref_run = self.trial_set['data'][self.trial_set['trials'][0]]['runs'][0]
                ref_trial = self.trial_set['trials'][0]
                self.plot_parameters['thermo']['title'] = '%s - %s' % (ref_trial, ref_run)
                plot_data = self.trial_set['data'][ref_trial]['data'][ref_run]['thermo']
        elif plot == 'hist':
            pass
        else:
            print('Select plot: "k" | "k_sub" | "hist" | "thermo"')
        return plot_data

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
