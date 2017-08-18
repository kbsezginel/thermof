"""
Tests reading thermal flux and calculating thermal conductivity
"""
import os
import pytest
import yaml
import numpy as np
from teemof.read import read_thermal_flux, calculate_k, estimate_k, average_k, get_flux_directions
from teemof.read import FluxFileNotFoundError, TimestepsMismatchError


flux_file = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'thermal-flux.dat')
flux_ref_file = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'flux.yaml')
time_ref_file = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'time.yaml')
k_ref_file = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'thermal-conductivity.yaml')
trial_dir = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'ideal-mof-trial')
k_parameters = dict(kb=0.001987, conv=69443.84, dt=5, volume=80 * 80 * 80,
                    temp=300, prefix='J0Jt_t', isotropic=False, average=True)


def test_read_thermal_flux():
    """Tests reading thermal flux data"""
    with open(flux_ref_file, 'r') as jref:
        flux_ref = yaml.load(jref)
    with open(time_ref_file, 'r') as tref:
        time_ref = yaml.load(tref)
    flux, time = read_thermal_flux(flux_file)
    assert np.allclose(flux, flux_ref)
    assert np.allclose(time, time_ref)


def test_thermal_conductivity_calculation():
    """Tests thermal conductivity calculation from thermal flux data"""
    with open(k_ref_file, 'r') as kref:
        k_ref = yaml.load(kref)
    flux, time = read_thermal_flux(flux_file)
    k = calculate_k(flux)
    assert np.allclose(k, k_ref)


def test_thermal_conductivity_average():
    """Tests thermal conductivity average for multiple runs data"""
    with open(k_ref_file, 'r') as kref:
        k_ref = yaml.load(kref)
    flux, time = read_thermal_flux(flux_file)
    assert np.allclose(average_k([flux, flux, flux, flux]), flux)


def test_thermal_conductivity_estimation():
    """Tests thermal conductivity estimation for given time range"""
    flux, time = read_thermal_flux(flux_file)
    J = calculate_k(flux, k_par=k_parameters)
    k = estimate_k(J, time, t0=5, t1=10)
    assert np.isclose(k, 0.8778570946468635)


def test_get_flux_directions_exception():
    """Tests whether thermal flux files note found exception is raised correctly"""
    k_parameters['prefix'] = 'wrong-name'
    with pytest.raises(FluxFileNotFoundError):
        get_flux_directions(os.path.join(trial_dir, 'Run1'), k_par=k_parameters)


def test_average_k_exception():
    """Tests whether trying to average thermal conductivity results with different
    number of timesteps raises exception correctly"""
    with open(k_ref_file, 'r') as kref:
        k_ref = yaml.load(kref)
    k_runs = [k_ref, k_ref[:10], k_ref[5:]]
    with pytest.raises(TimestepsMismatchError):
        average_k(k_runs)
