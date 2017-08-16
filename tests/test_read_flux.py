"""
Tests reading thermal flux and calculating thermal conductivity
"""
import os
import numpy as np
from teemof.read import read_thermal_flux, convert_kt, get_kt


def test_k_calculation():
    flux_file = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'thermal-flux.dat')
    flux, time = read_thermal_flux(flux_file)
    k_parameters = dict(kb=0.001987, conv=69443.84, dt=5, volume=80 * 80 * 80, temp=300)
    J = convert_kt(flux, kt_par=k_parameters)
    k = get_kt(J, time, t0=5, t1=10)
    assert np.isclose(k, 0.8778570946468635)
