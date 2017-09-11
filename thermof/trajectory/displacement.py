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


def mean_displacement(coordinates, normalize=True, reference_frame=0):
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
    ref_frame = coordinates[reference_frame]
    xd_sum, yd_sum, zd_sum = 0, 0, 0
    for frame in coordinates:
        xd_sum += frame[0]
        yd_sum += frame[1]
        zd_sum += frame[2]
    if normalize:
        xd_sum -= ref_frame[0] * n_frames
        yd_sum -= ref_frame[1] * n_frames
        zd_sum -= ref_frame[2] * n_frames
    return [xd_sum / n_frames, yd_sum / n_frames, zd_sum / n_frames]


def mean_squared_displacement(pos_data, dt=1):
    """ Calculate MSD for single dimension """
    msd_sum = 0
    n_points = len(pos_data) - dt
    for i in range(n_points):
        msd_sum += (pos_data[i + dt] - pos_data[i]) ** 2
    return (msd_sum / n_points)


def get_msd(trajectory, dt=1):
    """ Calculate MSD for given trajectory """
    msd = []
    for direction in range(3):
        pos_data = [i[direction] for i in trajectory['com']]
        msd.append(mean_squared_displacement(pos_data, dt))
    return msd


def msd_distance(coordinates, frames='all', atom=0):
    """ Calculate MSD for single atom using a reference frame and given frames
        - coordinates: list of coordinates for each frame
        - frames: frames to use for calculation ('all' or tuple -> (start, end))
        - atom: atom index to use for calculation
    """
    if frames == 'all':
        frames = (0, len(coordinates))
    d_sum = 0
    n_frames = len(coordinates[frames[0]:frames[1]])
    for frame in range(1, n_frames):
        coor_ref = coordinates[frame - 1][atom]         # Atom position at t -> r(t)
        coor = coordinates[frame][atom]                 # Atom position at t + 1 => r(t + 1)
        d_sum += np.sqrt(((coor[0] - coor_ref[0]) ** 2 +
                          (coor[1] - coor_ref[1]) ** 2 +
                          (coor[2] - coor_ref[2]) ** 2))
    return (d_sum / n_frames)
