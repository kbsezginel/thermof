# Date: August 2017
# Author: Kutay B. Sezginel
"""
Mean squared displacement calculation for Lammps trajectory.
"""
import numpy as np
import periodictable


def center_of_mass(atoms, coordinates):
    """ Calculate center of mass for given coordinates and atom names of a single frame

    Args:
        - atoms (list): List of element names
        - coordinates (list): List of coordinates (2D list)

    Returns:
        - list: Center of mass coordinate for list of atom coordinates
    """
    masses = np.array([periodictable.elements.symbol(atom).mass for atom in atoms])
    total_mass = masses.sum()
    x_cm = (masses * np.array([i[0] for i in coordinates])).sum() / total_mass
    y_cm = (masses * np.array([i[1] for i in coordinates])).sum() / total_mass
    z_cm = (masses * np.array([i[2] for i in coordinates])).sum() / total_mass
    return [x_cm, y_cm, z_cm]


def time_avg_displacement(coordinates, normalize=True, reference_frame=0):
    """
    Calculate time averaged (mean) displacement for a single atom in each direction using given trajectory coordinates.

    Args:
        - coordinates (list): 2D list of coordinates vs time
        - normalize (bool): Normalize displacement by subtracting coordinates from each frame for given reference frame
        - reference_frame (int): Index for reference frame

    Returns:
        - list: Average displacement for each direction
    """
    n_frames = len(coordinates)
    ref_frame = np.array(coordinates[reference_frame])
    if normalize:
        coordinates = np.array(coordinates) - ref_frame
    xd_sum, yd_sum, zd_sum = 0, 0, 0
    for frame in coordinates:
        xd_sum += frame[0]
        yd_sum += frame[1]
        zd_sum += frame[2]
    return [xd_sum / n_frames, yd_sum / n_frames, zd_sum / n_frames]


def time_avg_squared_displacement(coordinates, normalize=True, reference_frame=0):
    """
    Calculate time averaged (mean) squared displacement for a single atom in each direction using given trajectory coordinates.

    Args:
        - coordinates (list): 2D list of coordinates vs time
        - normalize (bool): Normalize displacement by subtracting coordinates from each frame for given reference frame
        - reference_frame (int): Index for reference frame

    Returns:
        - list: Average squared displacement for each direction
    """
    n_frames = len(coordinates)
    ref_frame = np.array(coordinates[reference_frame])
    if normalize:
        coordinates = np.array(coordinates) - ref_frame
    xd_sum, yd_sum, zd_sum = 0, 0, 0
    for frame in coordinates:
        xd_sum += frame[0] ** 2
        yd_sum += frame[1] ** 2
        zd_sum += frame[2] ** 2
    return [xd_sum / n_frames, yd_sum / n_frames, zd_sum / n_frames]
