"""
Tests reading thermal flux and calculating thermal conductivity for multiple trials with multiple runs
"""
import os
import yaml
import numpy as np
from thermof.read import read_trial_set
from thermof.parameters import k_parameters


k_ref_file = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'thermal-conductivity.yaml')
time_ref_file = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'time.yaml')
trial_set_dir = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'ideal-mof-trial-set')
k_est_iso_ref = [0.8624217134742657, 0.6839092609282974, 0.9263423943319228, 0.8656413422445915, 0.8983945996223535,
                 0.8802163796582159, 0.6416173216846418, 0.8356379755434158, 0.7098404203275488, 0.8686063495516347]


def test_read_trial_set():
    """Test method for reading a set of trial with multiple runs"""
    with open(k_ref_file, 'r') as kref:
        k_ref = yaml.load(kref)
    with open(time_ref_file, 'r') as tref:
        time_ref = yaml.load(tref)
    k_par = k_parameters.copy()
    k_par['isotropic'] = True
    k_par['average'] = True
    trial_set = read_trial_set(trial_set_dir, k_par=k_par)
    assert np.allclose(trial_set['data']['trial1']['data']['Run1']['k']['x'], k_ref)
    assert np.allclose(trial_set['data']['trial2']['data']['Run3']['time'], time_ref)
    assert np.isclose(trial_set['data']['trial1']['data']['Run1']['k_est']['iso'], k_est_iso_ref[0])
    assert np.isclose(trial_set['data']['trial1']['data']['Run2']['k_est']['iso'], k_est_iso_ref[1])
    assert np.isclose(trial_set['data']['trial2']['data']['Run3']['k_est']['iso'], k_est_iso_ref[2])
    assert np.isclose(trial_set['data']['trial2']['data']['Run4']['k_est']['iso'], k_est_iso_ref[3])
    assert np.isclose(trial_set['data']['trial1']['avg']['k_est']['iso'], (k_est_iso_ref[0] + k_est_iso_ref[1]) / 2)
    assert np.isclose(trial_set['data']['trial2']['avg']['k_est']['iso'], (k_est_iso_ref[2] + k_est_iso_ref[3]) / 2)
