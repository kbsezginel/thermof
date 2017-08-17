"""
Tests reading thermal flux and calculating thermal conductivity
"""
import os
import yaml
import numpy as np
from teemof.read import read_thermal_flux, calculate_k, estimate_k, average_k


flux_file = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'thermal-flux.dat')
flux_ref_file = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'flux.yaml')
time_ref_file = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'time.yaml')
k_ref_file = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'thermal-conductivity.yaml')


def test_thermal_flux_calculation():
    with open(flux_ref_file, 'r') as jref:
        flux_ref = yaml.load(jref)
    with open(time_ref_file, 'r') as tref:
        time_ref = yaml.load(tref)
    flux, time = read_thermal_flux(flux_file)
    assert np.allclose(flux, flux_ref)
    assert np.allclose(time, time_ref)


def test_thermal_conductivity_calculation():
    with open(k_ref_file, 'r') as kref:
        k_ref = yaml.load(kref)
    flux, time = read_thermal_flux(flux_file)
    k = calculate_k(flux)
    assert np.allclose(k, k_ref)


def test_thermal_conductivity_average():
    with open(k_ref_file, 'r') as kref:
        k_ref = yaml.load(kref)
    flux, time = read_thermal_flux(flux_file)
    assert np.allclose(average_k([flux, flux, flux, flux]), flux)


def test_thermal_conductivity_estimation():
    flux_file = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'thermal-flux.dat')
    flux, time = read_thermal_flux(flux_file)
    k_parameters = dict(kb=0.001987, conv=69443.84, dt=5, volume=80 * 80 * 80, temp=300)
    J = calculate_k(flux, k_par=k_parameters)
    k = estimate_k(J, time, t0=5, t1=10)
    assert np.isclose(k, 0.8778570946468635)
