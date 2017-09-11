"""
Tests time averaged displacement for trajectory.
"""
import numpy as np
from thermof.trajectory.displacement import mean_displacement


def test_mean_displacement():
    """ Tests time averaged (mean) displacement for linear motion of a single particle """
    coordinates = [[0, 0, 0], [1, 1, 1], [2, 2, 2], [3, 3, 3], [4, 4, 4], [5, 5, 5]]
    assert np.allclose([2.5, 2.5, 2.5], mean_displacement(coordinates))
    assert np.allclose([1.5, 1.5, 1.5], mean_displacement(coordinates, reference_frame=1))
    assert np.allclose([0.5, 0.5, 0.5], mean_displacement(coordinates, reference_frame=2))
