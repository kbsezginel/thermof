# Date: August 2017
# Author: Kutay B. Sezginel
"""
Simulation class for reading and initializing Lammps simulations
"""
import os
import yaml
import shutil
import glob
from thermof.parameters import Parameters, plot_parameters
from thermof.read import read_run, read_trial, read_trial_set
from thermof.initialize.lammps import write_lammps_files, write_lammps_input
from thermof.initialize.job import job_submission_file
from thermof.mof import MOF
from .plot import plot_simulation


class Simulation:
    """
    Reading and initializing Lammps simulations
    """
    def __init__(self, read=None, setup=None, parameters=None, mof=None, read_parameters=False):
        """
        Create a Lammps simulation object.
        """
        self.setup = '---'
        if parameters is None:
            self.parameters = Parameters()
            print('WARNING!: Default simulation parameters are loaded.')
        else:
            self.parameters = parameters
        if setup is not None:
            self.setup = setup
            if read is not None:
                self.read(read, setup, read_parameters=read_parameters)
        elif mof is not None:
            self.set_mof(mof)
        self.verbose = True

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

    def read(self, simdir, setup, read_parameters=False):
        """
        Read Lammps simulation results from given directory.
        """
        self.setup = setup
        self.simdir = simdir
        self.name = os.path.basename(simdir)
        if read_parameters:
            self.read_parameters()
        if setup == 'run':
            self.run = read_run(simdir, k_par=self.parameters.thermof['kpar'])
        elif setup == 'trial':
            self.trial = read_trial(simdir, k_par=self.parameters.thermof['kpar'])
        elif setup == 'trial_set':
            self.trial_set = read_trial_set(simdir, k_par=self.parameters.thermof['kpar'])
        else:
            print('Select setup: "run" | "trial" | "trial_set"')

    def initialize(self):
        """
        Initialize input files for a Lammps simulation.
        """
        self.setup = '|'.join(self.parameters.thermof['fix'])
        self.set_dir(self.simdir)
        write_lammps_files(self.simdir, self.parameters, verbose=self.verbose)
        write_lammps_input(self.simdir, self.parameters, verbose=self.verbose)
        job_submission_file(self.simdir, self.parameters, verbose=self.verbose)
        self.save_parameters()
        print('Done!') if self.verbose else None

    def initialize_runs(self, n_runs, run_parameters=None):
        """
        Initialize input files for a Lammps simulation with multiple runs.
        """
        self.setup = '|'.join(self.parameters.thermof['fix'])
        self.set_dir(self.simdir)
        write_lammps_files(self.simdir, self.parameters, verbose=self.verbose)
        inp_file = glob.glob(os.path.join(self.simdir, 'in.*'))[0]
        data_file = glob.glob(os.path.join(self.simdir, 'data.*'))[0]
        jobname = self.parameters.job['name']
        for run in range(1, n_runs + 1):
            rundir = os.path.join(self.simdir, '%i' % run)
            os.makedirs(rundir)
            shutil.copy(inp_file, rundir)
            shutil.copy(data_file, rundir)
            self.parameters.thermof['seed'] += 1
            self.parameters.job['name'] = '%s-%i' % (jobname, run)
            if run_parameters is not None:
                for par_key, par_val in run_parameters.items():
                    self.parameters.thermof[par_key] = par_val[run - 1]
            write_lammps_input(rundir, self.parameters, verbose=self.verbose)
            job_submission_file(rundir, self.parameters, verbose=self.verbose)
            self.save_parameters(simdir=rundir)
        os.remove(inp_file)
        os.remove(data_file)
        print('Done!') if self.verbose else None

    def set_dir(self, simdir):
        """
        Set simulation directory for initialization.
        """
        if os.path.exists(simdir):
            shutil.rmtree(simdir)
            print('Removing existing simulation directory -> %s' % simdir)
        os.makedirs(simdir)
        self.simdir = simdir

    def set_mof(self, mof_file):
        """
        Set MOF file for Lammps simulation
        """
        self.mof = MOF(mof_file)
        self.parameters.lammps['cif_file'] = self.mof.path
        self.parameters.job['name'] = self.mof.name
        self.parameters.job['input'] = 'in.%s' % self.mof.name
        if self.parameters.thermof['min_cell_size'] is not None:
            rep = self.mof.get_replication(self.parameters.thermof['min_cell_size'])
        else:
            rep = [1, 1, 1]
        self.parameters.lammps['replication'] = ' '.join([str(i) for i in rep])
        self.mof.volume = self.mof.get_volume(rep)
        self.parameters.thermof['mof'] = dict(name=self.mof.name,
                                              replication=rep,
                                              volume=self.mof.volume)
        self.parameters.thermof['kpar']['volume'] = self.mof.volume

    def plot(self, selection, data=None):
        """
        Plot Lammps simulation results.
        """
        if 'plot' not in vars(self.parameters).keys():
            self.parameters.plot = plot_parameters.copy()
        plot_simulation(self, selection, data)

    def show_parameters(self, par=None):
        """
        Show selected simulation parameters.
        """
        self.parameters.show(par=par)

    def save_parameters(self, simdir=None, parameters=['thermof', 'lammps', 'job']):
        """
        Save simulation parameters.
        """
        if simdir is None:
            simdir = self.simdir
        self.parameters.save(parameters=parameters, savedir=simdir, verbose=self.verbose)

    def read_parameters(self, simpar_file=None, setup=None):
        """
        Read simulation parameters.
        """
        if simpar_file is None:
            if self.setup == 'run':
                run_dir = self.simdir
            elif self.setup == 'trial':
                for run in os.listdir(self.simdir):
                    if os.path.isdir(os.path.join(self.simdir, run)) and 'simpar.yaml' in os.listdir(os.path.join(self.simdir, run)):
                        run_dir = os.path.join(self.simdir, run)
                        break
            elif self.setup == 'trial_set':
                for trial in os.listdir(self.simdir):
                    for run in os.listdir(os.path.join(self.simdir, trial)):
                        if 'simpar.yaml' in os.listdir(os.path.join(self.simdir, run)):
                            run_dir = os.path.join(self.simdir, run)
                            break
            simpar_file = os.path.join(run_dir, 'simpar.yaml')
        else:
            run_dir = os.path.dirname(simpar_file)
        print('Reading simulation parameters from -> %s' % run_dir) if self.verbose else None
        with open(simpar_file, 'r') as sp:
            simpar = yaml.load(sp)
        self.parameters = Parameters(simpar)

    def summarize(self, run_dict, padding=0):
        for i in run_dict.keys():
            if type(run_dict[i]) == dict:
                keys = [str(i) for i in list(run_dict[i].keys())]
                info = '%s%-10s -> dict: %s' % (' ' * padding, str(i), ' '.join(keys))
                print(info)
                self.summarize(run_dict[i], padding=padding + 5)
            elif type(run_dict[i]) in [str, int, float]:
                info = '%s%-10s -> %s' % (' ' * padding, i, run_dict[i])
                print(info)
            elif type(run_dict[i]) == list:
                info = '%s%-10s -> list of length: %s' % (' ' * padding, i, len(run_dict[i]))
                print(info)
            else:
                info = '%s%-10s -> %s' % (' ' * padding, i, type(run_dict[i]))
                print(info)
