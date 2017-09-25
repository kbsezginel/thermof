# Date: August 2017
# Author: Kutay B. Sezginel
"""
Simulation class for reading and initializing Lammps simulations
"""
import os
import pprint
from thermof.parameters import Parameters
from thermof.read import read_run, read_trial, read_trial_set, read_framework_distance
from thermof.visualize import plot_thermal_conductivity, plot_framework_distance, plot_thermo
from thermof.visualize import subplot_thermal_conductivity
from thermof.initialize.lammps import write_lammps_files, write_lammps_input
from thermof.initialize.job import job_submission_file
from thermof.mof import MOF
from .plot import get_plot_data


class Simulation:
    """
    Reading and initializing Lammps simulations
    """
    def __init__(self, read=None, setup=None, parameters=None, mof=None):
        """
        Create a Lammps simulation object.
        """
        if parameters is None:
            self.parameters = Parameters()
        else:
            self.parameters = parameters
        if read is not None and setup is not None:
            self.read(read, setup)
            self.setup = setup
            self.simdir = read
        elif mof is not None:
            self.set_mof(mof)

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

    def read(self, simdir, setup='run'):
        """
        Read Lammps simulation results from given directory.
        """
        self.setup = setup
        self.simdir = simdir
        self.name = os.path.basename(simdir)
        if setup == 'run':
            self.run = read_run(simdir, k_par=self.parameters.k)
        elif setup == 'trial':
            self.trial = read_trial(simdir, k_par=self.parameters.k)
        elif setup == 'trial_set':
            self.trial_set = read_trial_set(simdir, k_par=self.parameters.k)
        else:
            print('Select setup: "run" | "trial" | "trial_set"')

    def initialize(self):
        """
        Initialize input files for a Lammps simulation.
        """
        write_lammps_files(self.simdir, self.parameters)
        write_lammps_input(self.simdir, self.parameters)
        job_submission_file(os.path.join(self.simdir, '%s.%s' % ()))

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
            plot_thermal_conductivity(plot_data, self.parameters.plot['k'])
        elif selection == 'thermo':
            plot_thermo(plot_data, self.parameters.plot['thermo'])
        elif selection == 'k_sub':
            subplot_thermal_conductivity(plot_data, self.parameters.plot['k_sub'])
        elif selection == 'f_dist':
            plot_framework_distance(plot_data, self.parameters.plot['f_dist'])
        else:
            print('Select plot: "k" | "k_sub" | "f_dist" | "thermo"')

    def show_parameters(self, par=None):
        """
        Show selected simulation parameters.
        """
        self.parameters.show(par=par)
