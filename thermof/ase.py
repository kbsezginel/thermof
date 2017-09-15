# Date: September 2017
# Author: Kutay B. Sezginel
"""
Atomic simulation environment (ase) wrapper for file I/O operations.
"""
import os
from ase.io import read as ase_read
from ase.io import write as ase_write
from ase.geometry import cell_to_cellpar as ase_cellpar
from ase import Atom as ase_atom


def read(file_path, input_format=None):
    if input_format is None:
        input_format = os.path.splitext(file_path)[1][1:]
    # Read molecule file
    atoms = ase_read(file_path, format=input_format)

    # Get atom coordinates and names
    atom_coors = atoms.get_positions()
    atom_numbers = atoms.numbers
    atom_names = atoms.get_chemical_symbols()

    # Get unit cell parameters (converting from unit cell vectors)
    uc = ase_cellpar(atoms.cell)

    molecule = {'uc_size': [uc[0], uc[1], uc[2]],
                'uc_angle': [uc[3], uc[4], uc[5]],
                'atoms': atom_names,
                'atom_numbers': atom_numbers,
                'coordinates': atom_coors}

    return atoms, molecule


def write(file_path, ase_atoms, file_format=None):
    ase_write(file_path, ase_atoms, format=file_format)
