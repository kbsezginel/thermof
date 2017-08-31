"""
Tests trajectory read and write methods.
"""
import os
import numpy as np
from collections import Counter
from thermof import Trajectory

mof_trial_dir = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'ideal-mof-trial')
ipmof_trial_dir = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'ip-mof-trial')


def test_trajectory_change_atom_names_for_single_ideal_mof():
    """ Test trajectory class change atoms method for non-interpenetrated ideal MOF """
    traj = Trajectory(read=os.path.join(mof_trial_dir, 'Run1', 'traj.xyz'))
    assert traj.get_unique_atoms() == ['1']


def test_trajectory_change_atom_names_for_single_ideal_mof():
    """ Test trajectory class change atoms method for interpenetrated ideal MOF """
    traj = Trajectory(read=os.path.join(ipmof_trial_dir, 'Run1', 'traj.xyz'))
    assert Counter(traj.get_unique_atoms()) == Counter(['1', '2'])
