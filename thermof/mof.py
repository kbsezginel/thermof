# Date: September 2017
# Author: Kutay B. Sezginel
"""
MOF class for file I/O and molecular operations.
"""
import os
import numpy as np
from . import ase


class MOF:
    """
    Metal Organic Framework class.
    """
    def __init__(self, read=None):
        """
        Initialize MOF object by reading a molecule file.name, unit cell volume and parameters, atom names and coordinates, and
        unique atom names and coordinates.
        """
        if read is not None:
            self.read(read)

    def __repr__(self):
        return "<MOF: %s | %i atoms>" % (self.name, len(self.atoms))

    def __str__(self):
        return self.name

    def __len__(self):
        return len(self.atoms)

    def __eq__(self, other):
        return (isinstance(other, self.__class__) and self.name == other.name)

    def __ne__(self, other):
        return not self.__eq__(other)

    def read(self, mof_file, file_format=None):
        """
        Read given MOF file using ASE.

        Args:
            - mof_file (str): Path to mof structure file.
            - file_format (str): File format for the MOF file (not necessary if same as extension).

        Returns:
            - None: Assigns molecular information (atoms, coordinates, cell, ...) to object.
        """
        if file_format is None:
            file_format = os.path.splitext(os.path.basename(mof_file))[1][1:]
        self.path = mof_file
        self.name = os.path.splitext(os.path.basename(mof_file))[0]
        self.ase_atoms, molecule = ase.read(mof_file, input_format=file_format)

        self.coordinates = molecule['coordinates']
        self.atoms = molecule['atoms']
        self.atom_numbers = molecule['atom_numbers']
        self.uc_size = molecule['uc_size']
        self.uc_angle = molecule['uc_angle']

    def write(self, write_dir=None, file_format='cif'):
        """
        Write MOF object using ASE.

        Args:
            - write_dir (str): Directory to write MOF structure file.
            - file_format (str): File format for the MOF file.

        Returns:
            - None: Writes file to given directory.
        """
        if write_dir is None:
            write_dir = os.getcwd()
        mof_file = os.path.join(write_dir, self.name + '.' + file_format)
        ase.write(mof_file, self.ase_atoms, file_format=file_format)

    def get_replication(self, min_cell_size):
        """
        Get required replication to fulfill given minimum cell size.
        """
        cell = [np.linalg.norm(vec) for vec in self.ase_atoms.cell]
        return [int(np.ceil(min_cell_size[i] / cell[i])) for i in range(3)]
