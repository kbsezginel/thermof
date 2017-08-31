"""
Tests trajectory read method
"""
import os
import numpy as np
from thermof.trajectory import read_trajectory

mof_trial_dir = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'ideal-mof-trial')
ipmof_trial_dir = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'ip-mof-trial')


def test_read_trajectory_for_single_ideal_mof():
    """ Test xyz trajectory is read correctly for non-interpenetrated ideal MOF """
    traj = read_trajectory(os.path.join(mof_trial_dir, 'Run1', 'traj.xyz'))
    assert len(traj['xyz'][0]) == 3586
    assert len(traj['atoms'][0]) == 3584
    assert len(traj['coordinates'][0]) == 3584
    assert len(traj['timestep']) == 61
    assert traj['coordinates'][0][0] == [0, 0, 0]
    assert np.allclose(traj['coordinates'][-1][-1], [69.4517, 69.960, 76.5111])


def test_read_trajectory_for_interpenetrated_ideal_mof():
    """ Test xyz trajectory is read correctly for interpenetrated ideal MOF """
    traj = read_trajectory(os.path.join(ipmof_trial_dir, 'Run1', 'traj.xyz'))
    assert len(traj['xyz'][0]) == 7170
    assert len(traj['atoms'][0]) == 7168
    assert len(traj['coordinates'][0]) == 7168
    assert len(traj['timestep']) == 61
    assert traj['coordinates'][0][0] == [0, 0, 0]
    assert np.allclose(traj['coordinates'][-1][-1], [74.1941, 74.2373, 0.916302])
