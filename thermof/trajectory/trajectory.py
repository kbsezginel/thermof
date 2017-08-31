# Date: February 2017
# Author: Kutay B. Sezginel
"""
Read, manipulate and analyze Lammps trajectory output files of thermal conductivity measurements
"""
from .io import read_trajectory


class Trajectory:
    """
    Reading and analyzing Lammps simulation trajectories in xyz format
    """
    def __init__(self, read=None):
        """
        Create a trajectory object.
        """
        if read is not None:
            self.read(read)

    def __repr__(self):
        """
        Returns basic trajectory info.
        """
        return "<Trajectory | atoms: %i | frames: %i>" % (self.n_atoms, self.n_frames)

    def __str__(self):
        """
        Returns path of trajectory file.
        """
        return self.path

    def __len__(self):
        """
        Returns number of frames.
        """
        return self.n_frames

    def read(self, traj_path):
        """
        Read xyz trajectory file.
        """
        traj = read_trajectory(traj_path)
        self.path = traj_path
        self.xyz = traj['xyz']
        self.timestep = traj['timestep']
        self.atoms = traj['atoms']
        self.coordinates = traj['coordinates']
        self.n_frames = len(traj['timestep'])
        self.n_atoms = len(traj['atoms'][0])
