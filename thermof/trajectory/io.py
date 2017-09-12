# Date: August 2017
# Author: Kutay B. Sezginel
"""
Read, write Lammps trajectory in xyz format.
"""
import os


def read_trajectory(traj_path):
    """ Read xyz trajectory and return coordinates as a list

        Args:
            - traj_path (str): xyz trajectory path to read

        Returns:
            - dict: Trajectory dictionary with atoms, coordinates, timestep and xyz keys
    """
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


def write_trajectory(trajectory_xyz, traj_path, frames=None):
    """ Write xyz trajectory to a file

    Args:
        - trajectory_xyz (list): List of lines for each frame of the xyz trajectory
        - traj_path (str): xyz trajectory path to write

    Returns:
        - None: Write xyz trajectory file
    """
    if frames is None:
        frames = list(range(len(trajectory_xyz)))
    with open(traj_path, 'w') as traj:
        for frame in frames:
            xyz = trajectory_xyz[frame]
            for line in xyz:
                traj.write(line)
