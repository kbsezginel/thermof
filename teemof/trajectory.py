# Modify Lammps trajectory output files of thermal conductivity measurements
# Date: Februay 2017
# Author: Kutay B. Sezginel
import os


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


def change_xyz_trajectories(trial_dir, name='traj.xyz'):
    """ Change trajectory files for multiple runs and multiple trials """
    run_list = os.listdir(trial_dir)
    for run in run_list:
        if os.path.isdir(os.path.join(trial_dir, run)):
            print('Trajectory: %s' % run)
            xyz_traj_path = os.path.join(trial_dir, run, name)
            change_xyz_atom_names(xyz_traj_path)
