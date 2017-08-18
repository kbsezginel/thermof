"""
Tests Simulation class read method
"""
import os
import yaml
import numpy as np
from teemof.read import read_thermal_flux, calculate_k, estimate_k, average_k
from teemof.read import read_run, read_trial
from teemof.simulation import Simulation


k_ref_file = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'thermal-conductivity.yaml')
time_ref_file = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'time.yaml')
trial_dir = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'ideal-mof-trial')
k_parameters = dict(kb=0.001987, conv=69443.84, dt=5, volume=80 * 80 * 80, temp=300, prefix='J0Jt_t')
k_est_iso_ref = [0.8624217134742657, 0.6839092609282974, 0.9263423943319228, 0.8656413422445915, 0.8983945996223535,
                 0.8802163796582159, 0.6416173216846418, 0.8356379755434158, 0.7098404203275488, 0.8686063495516347]


def test_simulation_read_run():
    """Test Simulation class read method for reading a single run with read_run"""
    run_dir = os.path.join(trial_dir, 'Run1')
    run_data = read_run(run_dir)
    sim = Simulation(read=run_dir, )
    sim.read(run_dir, setup='run')
    assert sim.run == run_data


def test_read_trial():
    k_parameters['isotropic'] = True
    k_parameters['average'] = True
    trial = read_trial(trial_dir, k_par=k_parameters, isotropic=True, average=True)
    sim = Simulation(read=trial_dir, setup='trial', parameters=k_parameters)
    assert trial == sim.trial
