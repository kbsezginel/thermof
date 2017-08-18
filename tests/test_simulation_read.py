"""
Tests Simulation class read method
"""
import os
import yaml
import numpy as np
from teemof.read import read_run, read_trial, read_trial_set
from teemof import Simulation
from teemof.parameters import k_parameters


k_ref_file = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'thermal-conductivity.yaml')
time_ref_file = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'time.yaml')
trial_dir = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'ideal-mof-trial')
trial_set_dir = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'ideal-mof-trial-set')
k_est_iso_ref = [0.8624217134742657, 0.6839092609282974, 0.9263423943319228, 0.8656413422445915, 0.8983945996223535,
                 0.8802163796582159, 0.6416173216846418, 0.8356379755434158, 0.7098404203275488, 0.8686063495516347]


def test_simulation_read_run():
    """Test Simulation class read method for reading a single run with read_run"""
    k_par = k_parameters.copy()
    run_dir = os.path.join(trial_dir, 'Run1')
    run_data = read_run(run_dir, k_par=k_par)
    sim = Simulation(read=run_dir, parameters=k_par)
    sim.read(run_dir, setup='run')
    assert sim.run == run_data


def test_simulation_read_trial():
    """Test Simulation class read method for reading a trial"""
    k_par = k_parameters.copy()
    k_par['isotropic'] = True
    k_par['average'] = True
    trial = read_trial(trial_dir, k_par=k_par)
    sim = Simulation(read=trial_dir, setup='trial', parameters=k_par)
    assert trial == sim.trial


def test_simulation_read_trial_set():
    """Test Simulation class read method for reading a trial set"""
    k_par = k_parameters.copy()
    k_par['isotropic'] = True
    k_par['average'] = True
    trial_set = read_trial_set(trial_set_dir, k_par=k_par)
    sim = Simulation(read=trial_set_dir, setup='trial_set', parameters=k_par)
    assert trial_set == sim.trial_set
