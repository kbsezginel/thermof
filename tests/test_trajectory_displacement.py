"""
Tests center of mass and mean square displacement for Trajectory class
"""
import os
import numpy as np
from thermof import Trajectory


mof_trial_dir = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'ideal-mof-trial')
ipmof_trial_dir = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'ip-mof-trial')


def test_center_of_mass_for_single_ideal_mof():
    """ Test trajectory class read method for non-interpenetrated ideal MOF """
    traj = Trajectory(read=os.path.join(mof_trial_dir, 'Run1', 'traj.xyz'))
    traj.change_atoms({'1': 'C'})
    traj.calculate_com()
    assert np.isclose(traj.com[0][0], traj.com[0][1], traj.com[0][2])


def test_center_of_mass_for_interpenetrated_ideal_mof():
    """ Test trajectory class read method for interpenetrated ideal MOF """
    traj = Trajectory(read=os.path.join(ipmof_trial_dir, 'Run1', 'traj.xyz'))
    traj.change_atoms({'1': 'C', '2': 'O'})
    traj.calculate_com()
    assert np.isclose(traj.com[0][0], traj.com[0][1], traj.com[0][2])


def test_calculate_mean_disp_for_single_ideal_mof():
    """ Test trajectory class calculate_mean_disp function for single ideal mof """
    traj = Trajectory(read=os.path.join(mof_trial_dir, 'Run1', 'traj.xyz'))
    traj.set_cell([80, 80, 80])
    traj.calculate_distances()
    traj.calculate_mean_disp()
    assert np.all(traj.mean_disp > 0.0)
    assert np.all(traj.mean_disp < 0.6)


def test_calculate_mean_squared_disp_for_single_ideal_mof():
    """ Test trajectory class calculate_mean_squared_disp function for single ideal mof """
    traj = Trajectory(read=os.path.join(mof_trial_dir, 'Run1', 'traj.xyz'))
    traj.set_cell([80, 80, 80])
    traj.calculate_distances()
    traj.calculate_mean_squared_disp()
    assert np.all(traj.mean_squared_disp > 0.0)
    assert np.all(traj.mean_squared_disp < 0.4)


def test_calculate_mean_disp_and_mean_squared_disp_for_linear_motion_of_particles():
    """ Test trajectory class calculate_mean_disp and calculate_mean_squared_disp functions
        for 6 particles with linear motion with alternative calculation """
    n_atoms, n_frames = 6, 6
    traj = Trajectory()
    traj.coordinates = [[[i + j, i + j, i + j] for i in range(n_atoms)] for j in range(n_frames)]
    traj.n_atoms, traj.n_frames = n_atoms, n_frames
    traj.set_cell([10, 10, 10])
    traj.calculate_distances()
    traj.calculate_mean_disp()
    traj.calculate_mean_squared_disp()
    assert np.allclose([np.sum(range(n_frames)) / n_frames * np.sqrt(3)] * n_atoms, traj.mean_disp)
    for i in range(traj.n_atoms):
        c0 = traj.coordinates[0][i]
        x2 = (np.array([f[i][0] for f in traj.coordinates]) - c0[0]) ** 2
        y2 = (np.array([f[i][1] for f in traj.coordinates]) - c0[1]) ** 2
        z2 = (np.array([f[i][2] for f in traj.coordinates]) - c0[2]) ** 2
        mean_squared_disp = sum(x2 + y2 + z2) / n_frames
        mean_disp = sum(np.sqrt(x2 + y2 + z2)) / n_frames
        assert np.allclose(mean_disp, traj.mean_disp[i])
        assert np.allclose(mean_squared_disp, traj.mean_squared_disp[i])
