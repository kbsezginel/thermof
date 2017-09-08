"""
Tests trajectory calculate distances method.
"""
import os
import numpy as np
from thermof import Trajectory

mof_trial_dir = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'ideal-mof-trial')
ipmof_trial_dir = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'ip-mof-trial')


def test_trajectory_calculate_distances(max_dist=5):
    """
    Tests interatomic distance calculation for the Trajectory class
        - Test first frame is all zeros
        - Make sure all distances are less than max distance (5 A)
        - Test a known distance
    """
    traj = Trajectory(read=os.path.join(mof_trial_dir, 'Run1', 'traj.xyz'))
    traj.calculate_distances()
    assert np.allclose(traj.distances[0], np.zeros(traj.n_atoms))
    for frame in traj.distances:
        assert np.all(frame < max_dist)
    assert np.isclose(traj.distances[3][3], 0.5159079779340517)
