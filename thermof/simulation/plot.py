# Date: August 2017
# Author: Kutay B. Sezginel
"""
Plot functions for Simulation class
"""
import os
from thermof.read import read_framework_distance
from thermof.visualize import plot_thermal_conductivity, plot_framework_distance, plot_thermo
from thermof.visualize import subplot_thermal_conductivity


def plot_simulation(simulation, selection, data=None):
    """
    Plot Lammps simulation results.
    """
    if data is None:
        plot_data = get_plot_data(simulation, plot=selection)
    else:
        plot_data = data
    if selection == 'k':
        plot_thermal_conductivity(plot_data, simulation.parameters.plot['k'])
    elif selection == 'thermo':
        plot_thermo(plot_data, simulation.parameters.plot['thermo'])
    elif selection == 'k_sub':
        subplot_thermal_conductivity(plot_data, simulation.parameters.plot['k_sub'])
    elif selection == 'hcacf':
        subplot_thermal_conductivity(plot_data, simulation.parameters.plot['hcacf'])
    elif selection == 'f_dist':
        plot_framework_distance(plot_data, simulation.parameters.plot['f_dist'])
    else:
        print('Select plot: "k" | "k_sub" | "hcacf" | "f_dist" | "thermo"')


def get_plot_data(simulation, plot='k', setup=None):
    """
    Pulls corresponding data for selected plot.
    """
    plot_data = {}
    if setup is None:
        setup = simulation.setup
    if plot == 'k':
        if setup == 'run':
            plot_data = dict(x=simulation.run['time'], legend=simulation.run['directions'])
            plot_data['y'] = [simulation.run['k'][d] for d in simulation.run['directions']]
        elif setup == 'trial':
            plot_data = dict(x=simulation.trial['data'][simulation.trial['runs'][0]]['time'], legend=simulation.trial['runs'])
            plot_data['y'] = [simulation.trial['data'][run]['k']['iso'] for run in simulation.trial['runs']]
        elif setup == 'trial_set':
            ref_run = simulation.trial_set['data'][simulation.trial_set['trials'][0]]['runs'][0]
            ref_trial = simulation.trial_set['trials'][0]
            plot_data['x'] = simulation.trial_set['data'][ref_trial]['data'][ref_run]['time']
            plot_data['y'] = [simulation.trial_set['data'][trial]['avg']['k']['iso'] for trial in simulation.trial_set['trials']]
            plot_data['legend'] = simulation.trial_set['trials']
    elif plot == 'k_sub':
        if setup == 'run':
            plot_data = dict(x=simulation.run['time'], legend=simulation.run['directions'])
            plot_data['y'] = [simulation.run['k'][d] for d in simulation.run['directions']]
        elif setup == 'trial':
            plot_data = dict(x=simulation.trial['data'][simulation.trial['runs'][0]]['time'], legend=simulation.trial['runs'])
            plot_data['y'] = [simulation.trial['data'][run]['k']['iso'] for run in simulation.trial['runs']]
        elif setup == 'trial_set':
            ref_run = simulation.trial_set['data'][simulation.trial_set['trials'][0]]['runs'][0]
            ref_trial = simulation.trial_set['trials'][0]
            plot_data['x'] = simulation.trial_set['data'][ref_trial]['data'][ref_run]['time']
            plot_data['y'] = [simulation.trial_set['data'][trial]['avg']['k']['iso'] for trial in simulation.trial_set['trials']]
            plot_data['legend'] = simulation.trial_set['trials']
    elif plot == 'hcacf':
        if setup == 'run':
            plot_data = dict(x=simulation.run['time'], legend=simulation.run['directions'])
            plot_data['y'] = [simulation.run['hcacf'][d] for d in simulation.run['directions']]
        elif setup == 'trial':
            plot_data = dict(x=simulation.trial['data'][simulation.trial['runs'][0]]['time'], legend=simulation.trial['runs'])
            plot_data['y'] = [simulation.trial['data'][run]['hcacf']['iso'] for run in simulation.trial['runs']]
        elif setup == 'trial_set':
            ref_run = simulation.trial_set['data'][simulation.trial_set['trials'][0]]['runs'][0]
            ref_trial = simulation.trial_set['trials'][0]
            plot_data['x'] = simulation.trial_set['data'][ref_trial]['data'][ref_run]['time']
            plot_data['y'] = [simulation.trial_set['data'][trial]['avg']['hcacf']['iso'] for trial in simulation.trial_set['trials']]
            plot_data['legend'] = simulation.trial_set['trials']
    elif plot == 'thermo':
        if setup == 'run':
            simulation.parameters.plot['thermo']['title'] = simulation.run['name']
            plot_data = simulation.run['thermo']
        elif setup == 'trial':
            simulation.parameters.plot['thermo']['title'] = '%s' % (simulation.trial['runs'][0])
            plot_data = simulation.trial['data'][simulation.trial['runs'][0]]['thermo']
        elif setup == 'trial_set':
            ref_run = simulation.trial_set['data'][simulation.trial_set['trials'][0]]['runs'][0]
            ref_trial = simulation.trial_set['trials'][0]
            simulation.parameters.plot['thermo']['title'] = '%s - %s' % (ref_trial, ref_run)
            plot_data = simulation.trial_set['data'][ref_trial]['data'][ref_run]['thermo']
    elif plot == 'f_dist':
        if setup == 'run':
            run_list = [simulation.simdir]
        elif setup == 'trial':
            run_list = [os.path.join(simulation.simdir, run) for run in simulation.trial['runs']]
        elif setup == 'trial_set':
            run_list = [os.path.join(simulation.simdir, trial, ref_run) for trial in simulation.trial_set['trials']]
        plot_data = read_framework_distance(run_list, simulation.parameters.plot['f_dist'])
    else:
        print('Select plot: "k" | "k_sub" | "hcacf" | "hist" | "thermo"')
    return plot_data
