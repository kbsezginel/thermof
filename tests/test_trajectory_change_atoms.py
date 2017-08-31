"""
Tests trajectory read and write methods.
"""
import os
import numpy as np
from collections import Counter
from thermof import Trajectory

mof_trial_dir = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'ideal-mof-trial')
ipmof_trial_dir = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'ip-mof-trial')


def test_trajectory_change_atoms_for_single_ideal_mof():
    """ Test trajectory class change atoms method for non-interpenetrated ideal MOF """
    traj = Trajectory(read=os.path.join(mof_trial_dir, 'Run1', 'traj.xyz'))
    assert traj.get_unique_atoms() == ['1']
    traj.change_atoms({'1': 'C'})
    assert traj.get_unique_atoms() == ['C']
    ref_atoms = ['C'] * traj.n_atoms
    assert [line.split()[0] for line in traj.xyz[0][2:]] == ref_atoms
    assert traj.atoms[0] == ref_atoms


def test_trajectory_change_atoms_for_interpenetrated_ideal_mof():
    """ Test trajectory class change atoms method for interpenetrated ideal MOF """
    traj = Trajectory(read=os.path.join(ipmof_trial_dir, 'Run1', 'traj.xyz'))
    assert Counter(traj.get_unique_atoms()) == Counter(['1', '2'])
    traj.change_atoms({'1': 'C', '2': 'O'})
    assert Counter(traj.get_unique_atoms()) == Counter(['C', 'O'])
    ref_atoms = ['C'] * int(traj.n_atoms / 2) + ['O'] * int(traj.n_atoms / 2)
    assert [line.split()[0] for line in traj.xyz[0][2:]] == ref_atoms
    assert traj.atoms[0] == ref_atoms
