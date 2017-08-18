"""
Tests reading thermal flux and calculating thermal conductivity for single run
"""
import os
import pytest
import yaml
import numpy as np
from teemof.read import read_thermal_flux, calculate_k, estimate_k, average_k
from teemof.read import read_run


k_ref_file = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'thermal-conductivity.yaml')
time_ref_file = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'time.yaml')
trial_dir = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'ideal-mof-trial')


def test_get_flux_directions_exception():
    """Tests whether thermal flux files note found exception is raised correctly"""
    with pytest.raises(Exception):
        get_flux_directions(os.path.join(trial_dir, 'Run1'), prefix='wrong-name')


def test_average_k_exception():
    """Tests whether trying to average thermal conductivity results with different
    number of timesteps raises exception correctly"""
    with open(k_ref_file, 'r') as kref:
        k_ref = yaml.load(kref)
    k_runs = [k_ref, k_ref[:10], k_ref[5:]]
    with pytest.raises(Exception):
        average_k(k_runs)
