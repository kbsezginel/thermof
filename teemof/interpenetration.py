import os


def interpenetrate_lampps_data(data_path, output_dir=os.getcwd()):
    """ Create interpenetrated strcuture from lammps data file """
    ipmof_path = os.path.join(output_dir, 'lammps_ipmof.data')

    with open(data_path, 'r') as d:
        data_lines = d.readlines()

    # lines for atom number and atom type etc.
    for atom_line_index, atom_line in enumerate(data_lines):
        if 'Atoms' in atom_line:
            atom_start = atom_line_index + 2
        if 'Bonds' in atom_line:
            atom_end = atom_line_index - 1
    coordinates = data_lines[atom_start:atom_end]
    mof_num_of_atoms = len(coordinates)

    # lines for bonds
    for bond_line_index, bond_line in enumerate(data_lines):
        if 'Bonds' in bond_line:
            bond_start = bond_line_index + 2
    bond_end = bond_line_index
    all_bonds = data_lines[bond_start:]
    mof_num_of_bonds = bond_end - bond_start + 1

    ipmof_num_of_atoms = int(data_lines[1].split()[0]) * 2
    ipmof_num_of_bonds = int(data_lines[2].split()[0]) * 2
    ipmof_num_atomtypes = int(data_lines[3].split()[0]) + 1
    ipmof_num_bondtypes = int(data_lines[4].split()[0]) + 2
    d = 10

    # cell size
    cell_x = '0 80  xlo xhi'
    cell_y = '0 80  ylo yhi'
    cell_z = '0 80  zlo zhi'

    # Masses
    mass_1 = '1 39.948'
    mass_2 = '2 39.948'

    # Writing into the new file
    with open(ipmof_path, 'w') as ipmof:
        ipmof.write('LAMMPS data file.\n')
        ipmof.write(' %i atoms\n' % ipmof_num_of_atoms)
        ipmof.write(' %i bonds\n' % ipmof_num_of_bonds)
        ipmof.write(' %i atom types\n' % ipmof_num_atomtypes)
        ipmof.write(' %s\n' % cell_x)
        ipmof.write(' %s\n' % cell_y)
        ipmof.write(' %s\n\n' % cell_z)
        ipmof.write('Masses\n\n')
        ipmof.write('%s\n%s\n\n' % (mass_1, mass_2))
        ipmof.write('Atoms\n\n')
        for coord in data_lines[atom_start:(atom_end)]:
            ipmof.write('%s' % coord)
        for atom in data_lines[atom_start:(atom_end)]:
            atom = atom.split()
            ipmof.write('%i %i %i %i %f %f %f\n' % (int(atom[0]) + mof_num_of_atoms,
                                                    int(atom[1]) + 1,
                                                    int(atom[2]) + 1,
                                                    int(atom[3]),
                                                    float(atom[4]) + float(d / 2),
                                                    float(atom[5]) + float(d / 2),
                                                    float(atom[6]) + float(d / 2)))
        ipmof.write('\nBonds\n\n')
        for bond in all_bonds:
            ipmof.write('%s' % bond)
        for bond in all_bonds:
            bond = bond.split()
            ipmof.write('%s %s %s %s\n' % (int(bond[0]) + mof_num_of_bonds,
                                           int(bond[1]) + 2,
                                           int(bond[2]) + int(mof_num_of_atoms),
                                           int(bond[3]) + int(mof_num_of_atoms)))


def lammps_data2xyz(data_path, output_dir=os.getcwd()):
    """ Converts lammps.data file into xyz format """
    xyz_path = os.path.join(output_dir, '%s.xyz' % os.path.basename(os.path.splitext(data_path)[0]))

    with open(data_path, 'r') as d:
        data_lines = d.readlines()

    for line_index, line in enumerate(data_lines):
        if 'Atoms' in line:
            start = line_index + 2
        if 'Bonds' in line:
            end = line_index - 1

    coordinates = data_lines[start:end]

    num_of_atoms = len(coordinates)
    new_coordinates = []
    for c in coordinates:
        x = c.split()[4]
        y = c.split()[5]
        z = c.split()[6]
        new_coordinates.append([x, y, z])

    with open(xyz_path, 'w') as xyz:
        xyz.write('%i\n' % num_of_atoms)
        xyz.write('lammps_mof\n')
        for c in new_coordinates:
            xyz.write('C %s %s %s\n' % (c[0], c[1], c[2]))
