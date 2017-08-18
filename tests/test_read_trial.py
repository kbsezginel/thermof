"""
Tests reading thermal flux and calculating thermal conductivity for trials with multiple runs
"""
import os
import yaml
import numpy as np
from teemof.read import read_thermal_flux, calculate_k, estimate_k, average_k
from teemof.read import read_run, read_trial


k_ref_file = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'thermal-conductivity.yaml')
time_ref_file = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'time.yaml')
trial_dir = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'ideal-mof-trial')
k_parameters = dict(kb=0.001987, conv=69443.84, dt=5, volume=80 * 80 * 80, temp=300, prefix='J0Jt_t')
k_est_iso_ref = [0.8624217134742657, 0.6839092609282974, 0.9263423943319228, 0.8656413422445915, 0.8983945996223535,
                 0.8802163796582159, 0.6416173216846418, 0.8356379755434158, 0.7098404203275488, 0.8686063495516347]


def test_read_trial():
    with open(k_ref_file, 'r') as kref:
        k_ref = yaml.load(kref)
    with open(time_ref_file, 'r') as tref:
        time_ref = yaml.load(tref)
    trial = read_trial(trial_dir, k_par=k_parameters, isotropic=True, average=True)
    assert np.allclose(trial['data']['Run5']['time'], time_ref)
    assert np.allclose(trial['data']['Run1']['k']['x'], k_ref)
    assert np.isclose(trial['data']['Run1']['k_est']['x'], 0.8778570946468635)
    for i, k_ref in enumerate(k_est_iso_ref, start=1):
        assert np.isclose(trial['data']['Run%i' % i]['k_est']['iso'], k_ref)
    assert np.isclose(trial['avg']['k_est']['iso'], 0.817262775736688)
