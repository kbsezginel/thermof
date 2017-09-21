# Date: August 2017
# Author: Kutay B. Sezginel
"""
Simulation class for reading and initializing Lammps simulations
"""
import os
import pprint
from thermof.read import read_run, read_trial, read_trial_set, read_framework_distance
from thermof.parameters import k_parameters, plot_parameters
from thermof.visualize import plot_thermal_conductivity, plot_framework_distance, plot_thermo
from thermof.visualize import subplot_thermal_conductivity
from thermof.initialize.lammps import write_lammps_files
from thermof.initialize.job import job_submission_file
from thermof.initialize.tc import add_thermal_conductivity
from thermof.mof import MOF
from .plot import get_plot_data


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
            self.sim_dir = read

    def __repr__(self):
        """
        Returns basic simulation info
        """
        return "<Simulation | setup: %s | total runs: %i>" % (self.setup, len(self))

    def __str__(self):
        """
        Returns name of directory the results were read from
        """
        return self.name

    def __len__(self):
        """
        Returns number of total runs in simulation
        """
        if self.setup == 'run':
            n_runs = 1
        elif self.setup == 'trial':
            n_runs = len(self.trial['runs'])
        elif self.setup == 'trial_set':
            n_runs = 0
            for trial in self.trial_set['trials']:
                n_runs += len(self.trial_set['data'][trial]['runs'])
        return n_runs

    def read(self, sim_dir, setup='run'):
        """
        Read Lammps simulation results from given directory.
        """
        self.setup = setup
        self.sim_dir = sim_dir
        self.name = os.path.basename(sim_dir)
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

    def set_mof(self, mof_file):
        """
        Set MOF file for Lammps simulation
        """
        self.mof = MOF(mof_file)

    def plot(self, selection, data=None):
        """
        Plot Lammps simulation results.
        """
        if data is None:
            plot_data = get_plot_data(plot=selection)
        else:
            plot_data = data
        if selection == 'k':
            plot_thermal_conductivity(plot_data, self.plot_parameters['k'])
        elif selection == 'thermo':
            plot_thermo(plot_data, self.plot_parameters['thermo'])
        elif selection == 'k_sub':
            subplot_thermal_conductivity(plot_data, self.plot_parameters['k_sub'])
        elif selection == 'f_dist':
            plot_framework_distance(plot_data, self.plot_parameters['f_dist'])
        else:
            print('Select plot: "k" | "k_sub" | "f_dist" | "thermo"')

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
