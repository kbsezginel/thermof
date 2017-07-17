# Modify Lammps trajectory output files of thermal conductivity measurements
# Date: Februay 2017
# Author: Kutay B. Sezginel
import os
import periodictable


def change_xyz_atom_names(traj_path, atoms=['C', 'O'], targets=['1', '2']):
    """ Change atom names of xyz trajectory file """
    with open(traj_path, 'r') as t:
        traj = t.readlines()
    new_traj = []
    for t in traj:
        new_t = list(t)
        for atom, target in zip(atoms, targets):
            if t[0] == target:
                new_t[0] = atom
        new_t = ''.join(new_t)
        new_traj.append(new_t)
    new_traj_path = os.path.join(os.path.split(traj_path)[0], 'new_traj.xyz')
    with open(new_traj_path, 'w') as nt:
        for t in new_traj:
            nt.write(t)


def change_xyz_trajectories(trial_dir, name='traj.xyz', atoms=['C', 'O'], targets=['1', '2'], verbose=True):
    """ Change trajectory files for multiple runs of a single trial """
    run_list = os.listdir(trial_dir)
    for run in run_list:
        if os.path.isdir(os.path.join(trial_dir, run)):
            print('Trajectory: %s' % run) if verbose else None
            xyz_traj_path = os.path.join(trial_dir, run, name)
            change_xyz_atom_names(xyz_traj_path, atoms=atoms, targets=targets)


def read_trajectory(traj_path):
    """ Read xyz traectory and return coordinates as a list """
    with open(traj_path, 'r') as t:
        traj = t.readlines()

    n_atoms = int(traj[0].strip())                # Get nmber of atoms from first line
    n_frames = int(len(traj) / (n_atoms + 2))     # Calculate number of frames (assuming n_atoms is constant)

    trajectory = {'atoms': [], 'coordinates': [], 'xyz': [], 'timestep': []}
    for frame in range(n_frames):
        start = frame * (n_atoms + 2)             # Frame start
        end = (frame + 1) * (n_atoms + 2) - 1     # Frame end
        trajectory['xyz'].append(traj[start:end])
        trajectory['timestep'].append(traj[start + 1].strip().split()[2])
        trajectory['atoms'].append([line.split()[0] for line in traj[start + 2:end]])
        trajectory['coordinates'].append([[float(i) for i in line.split()[1:4]] for line in traj[start + 2:end]])

    return trajectory


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
