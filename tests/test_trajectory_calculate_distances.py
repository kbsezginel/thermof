"""
Tests trajectory calculate distances method.
"""
import os
import numpy as np
from thermof import Trajectory
from thermof.trajectory.tools import calculate_distances

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
    traj.set_cell([80, 80, 80])
    traj.calculate_distances()
    assert np.allclose(traj.distances[0], np.zeros(traj.n_atoms))
    for frame in traj.distances:
        assert np.all(frame < max_dist)
    assert np.isclose(traj.distances[3][3], 0.5159079779340517)


def test_trajectory_calculate_distances_nonzero_reference_frame(max_dist=5):
    """
    Tests interatomic distance calculation for the Trajectory class
        - Test seventh frame (reference frame) is all zeros
        - Make sure all distances are less than max distance (5 A)
        - Test a known distance
    """
    traj = Trajectory(read=os.path.join(mof_trial_dir, 'Run1', 'traj.xyz'))
    traj.set_cell([80, 80, 80])
    traj.calculate_distances(reference_frame=7)
    assert np.allclose(traj.distances[7], np.zeros(traj.n_atoms))
    for frame in traj.distances:
        assert np.all(frame < max_dist)
    assert np.isclose(traj.distances[0][3], 0.23030113908032163)


def test_calculate_distances_with_trajectory_calculate_distances(max_dist=5):
    """
    Tests interatomic distance calculation for the Trajectory class
        - Test first frame is all zeros
        - Make sure all distances are less than max distance (5 A)
        - Test a known distance
    """
    traj = Trajectory(read=os.path.join(mof_trial_dir, 'Run1', 'traj.xyz'))
    traj.set_cell([80, 80, 80])
    traj.calculate_distances()
    distances = calculate_distances(traj.coordinates, [80, 80, 80], reference_frame=0)
    assert np.allclose(traj.distances, distances)
