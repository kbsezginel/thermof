"""
Tests Simulation class read method
"""
import os
import yaml
import numpy as np
from thermof.read import read_run, read_trial, read_trial_set
from thermof import Simulation
from thermof.parameters import k_parameters


k_ref_file = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'thermal-conductivity.yaml')
time_ref_file = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'time.yaml')
trial_dir = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'ideal-mof-trial')
trial_set_dir = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'ideal-mof-trial-set')
run_info_ref_file = os.path.join(trial_dir, 'Run1', 'run_info.yaml')
thermo_ref_file = os.path.join(trial_dir, 'Run1', 'thermo.yaml')
k_est_iso_ref = [0.8624217134742657, 0.6839092609282974, 0.9263423943319228, 0.8656413422445915, 0.8983945996223535,
                 0.8802163796582159, 0.6416173216846418, 0.8356379755434158, 0.7098404203275488, 0.8686063495516347]


def test_simulation_read_run():
    """Test Simulation class read method for reading a single run with read_run"""
    k_par = k_parameters.copy()
    k_par['read_thermo'] = True
    k_par['read_info'] = True
    run_dir = os.path.join(trial_dir, 'Run1')
    run_data = read_run(run_dir, k_par=k_par)
    sim = Simulation(read=run_dir, parameters=k_par)
    sim.read(run_dir, setup='run')
    with open(run_info_ref_file, 'r') as riref:
        run_info_ref = yaml.load(riref)
    with open(thermo_ref_file, 'r') as tref:
        thermo_ref = yaml.load(tref)
    assert sim.run == run_data
    assert sim.run['info'] == run_info_ref
    assert sim.run['thermo'] == thermo_ref
    assert len(sim) == 1
    assert str(sim) == 'Run1'


def test_simulation_read_trial():
    """Test Simulation class read method for reading a trial"""
    k_par = k_parameters.copy()
    k_par['isotropic'] = True
    k_par['average'] = True
    trial = read_trial(trial_dir, k_par=k_par)
    sim = Simulation(read=trial_dir, setup='trial', parameters=k_par)
    assert trial == sim.trial
    assert len(sim) == 10
    assert str(sim) == 'ideal-mof-trial'


def test_simulation_read_trial_set():
    """Test Simulation class read method for reading a trial set"""
    k_par = k_parameters.copy()
    k_par['isotropic'] = True
    k_par['average'] = True
    trial_set = read_trial_set(trial_set_dir, k_par=k_par)
    sim = Simulation(read=trial_set_dir, setup='trial_set', parameters=k_par)
    assert trial_set == sim.trial_set
    assert len(sim) == 4
    assert str(sim) == 'ideal-mof-trial-set'
