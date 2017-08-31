# Date: August 2017
# Author: Kutay B. Sezginel
"""
Read, write Lammps trajectory in xyz format.
"""
import os


def read_trajectory(traj_path):
    """ Read xyz trajectory and return coordinates as a list """
    with open(traj_path, 'r') as t:
        traj = t.readlines()

    n_atoms = int(traj[0].strip())                # Get number of atoms from first line
    n_frames = int(len(traj) / (n_atoms + 2))     # Calculate number of frames (assuming n_atoms is constant)

    trajectory = {'atoms': [], 'coordinates': [], 'xyz': [], 'timestep': []}
    for frame in range(n_frames):
        start = frame * (n_atoms + 2)             # Frame start
        end = (frame + 1) * (n_atoms + 2)         # Frame end
        trajectory['xyz'].append(traj[start:end])
        trajectory['timestep'].append(traj[start + 1].strip().split()[2])
        trajectory['atoms'].append([line.split()[0] for line in traj[start + 2:end]])
        trajectory['coordinates'].append([[float(i) for i in line.split()[1:4]] for line in traj[start + 2:end]])

    return trajectory


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
