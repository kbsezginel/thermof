# Date: February 2017
# Author: Kutay B. Sezginel
"""
Read, manipulate and analyze Lammps trajectory output files of thermal conductivity measurements
"""
import numpy as np
from .io import read_trajectory, write_trajectory, generate_xyz
from .tools import center_of_mass, calculate_distances, subdivide_coordinates, subdivide_atoms


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
        return "<Trajectory frames: %i | atoms: %i | dimensions: %i>" % (self.n_atoms, self.n_frames, self.n_dimensions)

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

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            check1 = (self.n_frames, self.n_atoms, self.n_dimensions) == (other.n_frames, other.n_atoms, other.n_dimensions)
            check2 = np.allclose(self.coordinates, other.coordinates) and self.atoms == other.atoms
            return check1 and check2
        else:
            return False

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
        self.n_frames, self.n_atoms, self.n_dimensions = np.shape(traj['coordinates'])

    def write(self, traj_path, frames=None):
        """
        Write xyz trajectory file.
        """
        write_trajectory(self.xyz, traj_path, frames)

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
        self.xyz = generate_xyz(self.coordinates, self.atoms)

    def subdivide(self, frames=None, atoms=None, dimensions=None):
        """
        Subdivide trajectory by selecting frames, atoms and dimensions.

        Args:
            - atoms (list): List of atoms to be included in subdivision
            - frames (list): List of frames to be included in the subdivision
            - dimensions (list): List of dimensions to be included in the subdivision

        Returns:
            - Trajectory: New trajectory object

        Examples:

            >>> traj_div = traj.subdivide(atoms=list(range(5)), frames=[0], dimensions=[1])
            <Trajectory | frames: 1 | atoms: 5 | dimensions: 1>
        """
        div_coor = subdivide_coordinates(self.coordinates, frames, atoms, dimensions)
        div_traj = Trajectory()
        div_traj.coordinates = div_coor
        div_traj.n_frames, div_traj.n_atoms, div_traj.n_dimensions = np.shape(div_coor)
        div_traj.atoms = subdivide_atoms(self.atoms, frames, atoms)
        if frames is None:
            frames = list(range(self.n_frames))
        if hasattr(self, 'timestep'):
            div_traj.timestep = [ts for i, ts in enumerate(self.timestep) if i in frames]
        if hasattr(self, 'xyz'):
            div_traj.xyz = [xyz for i, xyz in enumerate(self.xyz) if i in frames]
        if hasattr(self, 'path'):
            div_traj.path = self.path
        return div_traj

    def set_coordinates(self, coordinates):
        """
        Initialize Trajectory by setting coordinates.

        Args:
            - unit_cell (list): 3D list including coordinates of each atom for each frame.

        Returns:
            - None (assigns trajectory properties)
        """
        self.coordinates = coordinates

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

    def calculate_com(self):
        """
        Get center of mass coordinates for the trajectory.
        """
        self.com = [center_of_mass(fa, fc) for fa, fc in zip(self.atoms, self.coordinates)]

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
