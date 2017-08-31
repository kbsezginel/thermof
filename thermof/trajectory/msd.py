# Date: August 2017
# Author: Kutay B. Sezginel
"""
Mean squared displacement calculation for Lammps trajectory.
"""
import math
import periodictable


def center_of_mass(atoms, coordinates):
    """ Calculate center of mass for given coordinates and atom names """
    xsum, ysum, zsum = 0, 0, 0
    for atom, coor in zip(atoms, coordinates):
        mass = periodictable.elements.symbol(atom).mass
        wx, wy, wz = [mass * i for i in coor]
        xsum += wx
        ysum += wy
        zsum += wz
    return [xsum, ysum, zsum]


def get_com(trajectory):
    """ Analyze center of mass coordinate change """
    trajectory['com'] = []
    for atoms, coors in zip(trajectory['atoms'], trajectory['coordinates']):
        com = center_of_mass(atoms, coors)
        trajectory['com'].append(com)
    x_avg = sum([i[0] for i in trajectory['com']]) / len(trajectory['com'])
    y_avg = sum([i[1] for i in trajectory['com']]) / len(trajectory['com'])
    z_avg = sum([i[2] for i in trajectory['com']]) / len(trajectory['com'])
    trajectory['com_avg'] = [x_avg, y_avg, z_avg]
    return trajectory


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
        d_sum += math.sqrt(((coor[0] - coor_ref[0]) ** 2 +
                            (coor[1] - coor_ref[1]) ** 2 +
                            (coor[2] - coor_ref[2]) ** 2))
    return (d_sum / n_frames)
