"""
Tests trajectory read method
"""
import os
import numpy as np
from thermof import Trajectory

mof_trial_dir = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'ideal-mof-trial')
ipmof_trial_dir = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'ip-mof-trial')


def test_trajectory_read_method_for_single_ideal_mof():
    """ Test trajectory class read method for non-interpenetrated ideal MOF """
    traj = Trajectory(read=os.path.join(mof_trial_dir, 'Run1', 'traj.xyz'))
    assert len(traj.xyz[0]) == 3586
    assert len(traj.atoms[0]) == 3584
    assert len(traj.coordinates[0]) == 3584
    assert traj.n_frames == 61
    assert traj.coordinates[0][0] == [0, 0, 0]
    assert np.allclose(traj.coordinates[-1][-1], [69.4517, 69.960, 76.5111])


def test_trajectory_read_method_for_interpenetrated_ideal_mof():
    """ Test trajectory class read method for interpenetrated ideal MOF """
    traj = Trajectory(read=os.path.join(ipmof_trial_dir, 'Run1', 'traj.xyz'))
    assert len(traj.xyz[0]) == 7170
    assert len(traj.atoms[0]) == 7168
    assert len(traj.coordinates[0]) == 7168
    assert traj.n_frames == 61
    assert traj.coordinates[0][0] == [0, 0, 0]
    assert np.allclose(traj.coordinates[-1][-1], [74.1941, 74.2373, 0.916302])
