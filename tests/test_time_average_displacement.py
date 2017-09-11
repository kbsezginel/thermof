"""
Tests time averaged displacement for trajectory.
"""
import numpy as np
from thermof.trajectory.tools import time_avg_displacement, time_avg_squared_displacement


def test_time_averaged_displacement_with_different_reference_frames():
    """ Tests time averaged (mean) displacement for linear motion of a single particle """
    coordinates = [[0, 0, 0], [1, 1, 1], [2, 2, 2], [3, 3, 3], [4, 4, 4], [5, 5, 5]]
    assert np.allclose([2.5, 2.5, 2.5], time_avg_displacement(coordinates))
    assert np.allclose([1.5, 1.5, 1.5], time_avg_displacement(coordinates, reference_frame=1))
    assert np.allclose([0.5, 0.5, 0.5], time_avg_displacement(coordinates, reference_frame=2))


def test_time_averaged_displacement_with_multiple_atoms():
    """ Test trajectory class calculate_mean_disp function for all atoms """
    n_atoms, n_frames = 6, 6
    coordinates = [[[i + j, i + j, i + j] for i in range(n_atoms)] for j in range(n_frames)]
    for atom in range(n_atoms):
        atom_coordinates = [coordinates[i][atom] for i in range(n_frames)]
        assert np.allclose([np.sum(range(n_frames)) / n_frames] * 3, time_avg_displacement(atom_coordinates))


def test_time_averaged_squared_displacement_with_multiple_atoms():
    """ Test trajectory class calculate_mean_disp function for all atoms """
    n_atoms, n_frames = 6, 6
    coordinates = [[[i + j, i + j, i + j] for i in range(n_atoms)] for j in range(n_frames)]
    for atom in range(n_atoms):
        atom_coordinates = [coordinates[i][atom] for i in range(n_frames)]
        assert np.allclose([np.sum(np.arange(n_frames) ** 2) / n_frames] * 3, time_avg_squared_displacement(atom_coordinates))
