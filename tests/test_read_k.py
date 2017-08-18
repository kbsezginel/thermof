"""
Tests reading thermal flux and calculating thermal conductivity for single run
"""
import os
import pytest
import yaml
import numpy as np
from teemof.read import get_flux_directions, average_k
from teemof.read import FluxFileNotFoundError, TimestepsMismatchError


k_ref_file = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'thermal-conductivity.yaml')
time_ref_file = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'time.yaml')
trial_dir = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'ideal-mof-trial')
k_parameters = dict(kb=0.001987, conv=69443.84, dt=5, volume=80 * 80 * 80,
                    temp=300, prefix='J0Jt_t', isotropic=False, average=True)


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
