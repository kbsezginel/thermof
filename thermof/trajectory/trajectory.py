# Date: February 2017
# Author: Kutay B. Sezginel
"""
Read, manipulate and analyze Lammps trajectory output files of thermal conductivity measurements
"""
import numpy as np
from .io import read_trajectory, write_trajectory
from .tools import center_of_mass, calculate_distances


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

        Args:
            - traj_path (str): xyz trajectory file path to read

        Returns:
            - None: Assigns path, xyz, timestep, atoms, coordinates, n_frames, n_atoms variables
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

        Args:
            - n_repeat (int): Repeat each frame <n_repeat> number of times
            - write (str / None): Write xyz trajectory to given path (default: None)

        Returns:
            - list: List of lines for each frame of the stretched xyz trajectory
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

    def get_com(self):
        """
        Get center of mass coordinates for the trajectory.
        """
        self.com = [center_of_mass(fa, fc) for fa, fc in zip(self.atoms, self.coordinates)]

    def set_cell(self, unit_cell):
        """
        Set unit cell dimensions for the trajectory.

        Args:
            - unit_cell (list): Unit cell dimensions for periodic boundary conditions (ORTHORHOMBIC ONLY)

        Returns:
            - None (assigns cell dimensons to self.cell)
        """
        if len(unit_cell) == 3:
            self.cell = unit_cell
        else:
            print('List dimension for the cell must be 3')

    def calculate_distances(self, reference_frame=0):
        """
        Calculate distance of each atom from it's reference position for each frame in the trajectory.
        ---------- ORTHORHOMBIC ONLY ----------

        Args:
            - reference_frame (int): Reference frame to calculate the distances from

        Returns:
            - None (assigns distances to self.distances as a numpy array)
        """
        self.distances = calculate_distances(self.coordinates, self.cell, reference_frame=reference_frame)

    def calculate_mean_disp(self, reference_frame=0):
        """
        Calculate time averaged (mean) displacement <d> for given atoms.

        Args:
            - reference_frame (int): Index for reference frame

        Returns:
            - None (assigns mean displacement <d> to self.mean_disp as a numpy array)
        """
        if not hasattr(self, 'distances'):
            if hasattr(self, 'cell'):
                self.calculate_distances(reference_frame=reference_frame)
            else:
                print('Please define simulation cell size and calculate distances')
        n_frames, n_atoms = np.shape(self.distances)
        self.mean_disp = np.zeros((n_atoms, ))
        for atom in range(n_atoms):
            d_sum = 0
            for frame in range(n_frames):
                d_sum += self.distances[frame][atom]
            self.mean_disp[atom] = d_sum / n_frames

    def calculate_mean_squared_disp(self, reference_frame=0):
        """
        Calculate time averaged (mean) displacement <d2> for given atoms.

        Args:
            - reference_frame (int): Index for reference frame

        Returns:
            - None (assigns mean squared displacement <d2> to self.mean_squared_disp as a numpy array)
        """
        if not hasattr(self, 'distances'):
            if hasattr(self, 'cell'):
                self.calculate_distances(reference_frame=reference_frame)
            else:
                print('Please define simulation cell size and calculate distances')
        n_frames, n_atoms = np.shape(self.distances)
        self.mean_squared_disp = np.zeros((n_atoms, ))
        for atom in range(n_atoms):
            d_sum = 0
            for frame in range(n_frames):
                d_sum += self.distances[frame][atom] ** 2
            self.mean_squared_disp[atom] = d_sum / n_frames
