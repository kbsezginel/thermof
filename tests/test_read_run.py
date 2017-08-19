"""
Tests reading thermal flux and calculating thermal conductivity for single run
"""
import os
import pytest
import yaml
import numpy as np
from teemof.read import read_thermal_flux, calculate_k, estimate_k, average_k
from teemof.read import read_run, FluxFileNotFoundError, RunDirectoryNotFoundError
from teemof.parameters import k_parameters


k_ref_file = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'thermal-conductivity.yaml')
time_ref_file = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'time.yaml')
trial_dir = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'ideal-mof-trial')


def test_read_run():
    """Test reading a single run with read_run"""
    k_par = k_parameters.copy()
    run_data = read_run(os.path.join(trial_dir, 'Run1'), k_par=k_par)
    with open(k_ref_file, 'r') as kref:
        k_ref = yaml.load(kref)
    with open(time_ref_file, 'r') as tref:
        time_ref = yaml.load(tref)
    assert run_data['name'] == 'Run1'
    assert np.isclose(run_data['k_est']['x'], 0.8778570946468635)
    assert np.allclose(run_data['time'], time_ref)
    assert np.allclose(run_data['k']['x'], k_ref)


def test_isotropic_read_run():
    """Test reading a single run and averaging directions"""
    k_par = k_parameters.copy()
    k_par['isotropic'] = True
    run_data = read_run(os.path.join(trial_dir, 'Run2'), k_par=k_par)

    flux_file_x = os.path.join(trial_dir, 'Run2', 'J0Jt_tx.dat')
    flux_x, time = read_thermal_flux(flux_file_x)
    J_x = calculate_k(flux_x, k_par=k_par)
    k_x = estimate_k(J_x, time, t0=5, t1=10)
    assert np.allclose(run_data['k']['x'], J_x)
    assert np.isclose(run_data['k_est']['x'], k_x)

    flux_file_y = os.path.join(trial_dir, 'Run2', 'J0Jt_ty.dat')
    flux_y, time = read_thermal_flux(flux_file_y)
    J_y = calculate_k(flux_y, k_par=k_par)
    k_y = estimate_k(J_y, time, t0=5, t1=10)
    assert np.allclose(run_data['k']['y'], J_y)
    assert np.isclose(run_data['k_est']['y'], k_y)

    flux_file_z = os.path.join(trial_dir, 'Run2', 'J0Jt_tz.dat')
    flux_z, time = read_thermal_flux(flux_file_z)
    J_z = calculate_k(flux_z, k_par=k_par)
    k_z = estimate_k(J_z, time, t0=5, t1=10)
    assert np.allclose(run_data['k']['z'], J_z)
    assert np.isclose(run_data['k_est']['z'], k_z)

    J_iso = average_k([J_x, J_y, J_z])
    assert np.allclose(run_data['k']['iso'], J_iso)

    k_iso = estimate_k(J_iso, time, t0=5, t1=10)
    assert np.allclose(run_data['k_est']['iso'], k_iso)


def test_read_run_input_error():
    """Tests whether read_run raises exception for missing flux file correctly"""
    run_dir = os.path.join(trial_dir, 'Run1')
    k_par = k_parameters.copy()
    k_par['prefix'] = 'wrong-name'
    with pytest.raises(FluxFileNotFoundError):
        read_run(run_dir, k_par=k_par, t0=5, t1=10)


def test_read_run_directory_not_found_error():
    """Tests whether read_run raises exception for missing flux file correctly"""
    run_dir = os.path.join(trial_dir, 'Run11')
    k_par = k_parameters.copy()
    with pytest.raises(RunDirectoryNotFoundError):
        read_run(run_dir, k_par=k_par, t0=5, t1=10)


def test_read_run_read_info():
    """Tests whether read_run raises exception for missing flux file correctly"""
    run_dir = os.path.join(trial_dir, 'Run1')
    k_par = k_parameters.copy()
    k_par['read_info'] = True
    run = read_run(run_dir, k_par=k_par, t0=5, t1=10)
    run_info_path = os.path.join(run_dir, 'run_info.yaml')
    with open(os.path.join(run_dir, 'run_info.yaml'), 'r') as ri:
        ref_run_info = yaml.load(ri)
    assert run['info'] == ref_run_info
