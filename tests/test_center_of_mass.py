"""
Tests center of mass calculation
"""
import numpy as np
from thermof.trajectory.displacement import center_of_mass


def test_center_of_mass_for_linear_arrangement_of_atoms():
    """ Tests center of mass calculation for three linear atoms """
    coordinates = [[2, -2, 3], [1, -2, 3], [0, -2, 3]]
    assert np.allclose(center_of_mass(['C', 'C', 'C'], coordinates), [1, -2, 3])
    assert np.allclose(center_of_mass(['C', 'Zn', 'C'], coordinates), [1, -2, 3])
    assert np.allclose(center_of_mass(['N', 'O', 'N'], coordinates), [1, -2, 3])


def test_center_of_mass_for_square_arrangement_of_atoms():
    """ Tests center of mass calculation for square arrangement of atoms """
    coordinates = [[0, 0, 0], [1, 0, 0], [0, 1, 0], [1, 1, 0]]
    assert np.allclose(center_of_mass(['H', 'H', 'H', 'H'], coordinates), [0.5, 0.5, 0])
    assert np.allclose(center_of_mass(['C', 'O', 'O', 'C'], coordinates), [0.5, 0.5, 0])
