# Date: February 2017
# Author: Kutay B. Sezginel
"""
Read, manipulate and analyze Lammps trajectory output files of thermal conductivity measurements
"""
from .io import read_trajectory, write_trajectory


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

    def write(self, traj_path):
        """
        Write xyz trajectory file.
        """
        write_trajectory(self.xyz, traj_path)

    def stretch(self, n_repeat, write=None):
        """
        Repeats each frame a given number of time.
        """
        xyz_stretch = []
        for xyz in self.xyz:
            for r in range(n_repeat):
                xyz_stretch.append(xyz)
        if write is not None:
            write_trajectory(xyz_stretch, write)
        return xyz_stretch

    def get_unique_atoms(self):
        """
        Finds unique atom names in the trajectory.
        """
        self.unique_atoms = list(set([atom for frame in self.atoms for atom in frame]))
        return self.unique_atoms

    def change_atoms(self, atom_map):
        """
        Changes atom names in trajectory (both self.atoms and self.xyz).

        Args:
            - atom_map (dict): Keys are atoms to be changed and values are new atoms (ex: {'1': 'C', '2': 'O'})

        Returns:
            - None (changes self.xyz and self.atoms to new atoms)
        """
        new_atoms = []
        for frame in self.atoms:
            frame_atoms = []
            for atom in frame:
                new_atom = atom_map[atom]
                frame_atoms.append(new_atom)
            new_atoms.append(frame_atoms)
        self.atoms = new_atoms

        new_xyz = []
        for frame in self.xyz:
            xyz_frame = frame[:2]
            for line in frame[2:]:
                atom = line.split()[0]
                new_line = line.replace(atom, atom_map[atom])
                xyz_frame.append(new_line)
            new_xyz.append(xyz_frame)
        self.xyz = new_xyz
