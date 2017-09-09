"""
Tests time averaged displacement for trajectory.
"""
import numpy as np
from thermof.trajectory.msd import time_avg_displacement


def test_time_avg_displacement():
    """ Tests time averaged displacement for linear motion of a single particle """
    coordinates = [[0, 0, 0], [1, 1, 1], [2, 2, 2], [3, 3, 3], [4, 4, 4], [5, 5, 5]]
    assert np.allclose([2.5, 2.5, 2.5], time_avg_displacement(coordinates))
    assert np.allclose([2, 2, 2], time_avg_displacement(coordinates, reference_frame=3))
    assert np.allclose([1.66667, 1.66667, 1.66667], time_avg_displacement(coordinates, reference_frame=5))
