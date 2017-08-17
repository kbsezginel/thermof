"""
Tests reading thermal flux and calculating thermal conductivity for trials with multiple runs
"""
import os
import yaml
import numpy as np
from teemof.read import read_thermal_flux, calculate_k, estimate_k, average_k
from teemof.read import read_run


k_ref_file = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'thermal-conductivity.yaml')
time_ref_file = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'time.yaml')
trial_dir = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'ideal-mof-trial')


def test_read_run():
    """Test reading a single run with read_run"""
    run_data = read_run(os.path.join(trial_dir, 'Run1'))
    with open(k_ref_file, 'r') as kref:
        k_ref = yaml.load(kref)
    with open(time_ref_file, 'r') as tref:
        time_ref = yaml.load(tref)
    assert run_data['name'] == 'Run1'
    assert np.isclose(run_data['k_est']['x'], 0.8778570946468635)
    assert np.allclose(run_data['time'], time_ref)
    assert np.allclose(run_data['k']['x'], k_ref)
