"""
Tests reading thermal flux and calculating thermal conductivity for trials with multiple runs
"""
import os
import yaml
import numpy as np
from teemof.read import read_thermal_flux, calculate_k, estimate_k, average_k


trial_dir = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'ideal-mof-trial')
