"""
Tests Simulation class read method
"""
import os
import yaml
import numpy as np
from teemof import Simulation
from teemof.parameters import k_parameters


k_ref_file = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'thermal-conductivity.yaml')
time_ref_file = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'time.yaml')
trial_dir = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'ideal-mof-trial')
trial_set_dir = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'ideal-mof-trial-set')
run_info_ref_file = os.path.join(trial_dir, 'Run1', 'run_info.yaml')
thermo_ref_file = os.path.join(trial_dir, 'Run1', 'thermo.yaml')
k_est_iso_ref = [0.8624217134742657, 0.6839092609282974, 0.9263423943319228, 0.8656413422445915, 0.8983945996223535,
                 0.8802163796582159, 0.6416173216846418, 0.8356379755434158, 0.7098404203275488, 0.8686063495516347]


def test_simulation_get_plot_data_for_run():
    """Test Simulation class get_plot_data method for pulling correct data for different plots of a run"""
    k_par = k_parameters.copy()
    k_par['read_thermo'] = True
    run_dir = os.path.join(trial_dir, 'Run1')
    sim = Simulation(read=run_dir, parameters=k_par, setup='run')
    with open(k_ref_file, 'r') as kref:
        k_ref = yaml.load(kref)
    with open(time_ref_file, 'r') as tiref:
        time_ref = yaml.load(tiref)
    with open(thermo_ref_file, 'r') as tref:
        thermo_ref = yaml.load(tref)
    assert sim.get_plot_data('thermo') == thermo_ref
    k_plot_data = sim.get_plot_data('k')
    assert k_plot_data['x'] == time_ref
    assert k_plot_data['y'][sim.run['directions'].index('x')] == k_ref
    assert k_plot_data['legend'] == sim.run['directions']
