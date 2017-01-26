def export_lines(file_lines, export_path):
    """ Exports array of lines onto a file """
    with open(export_path, 'w') as f:
        for l in file_lines:
            f.write(l)

def lammps_qsub(qsub_path, name='Lammps', walltime='12:00:00', nodes=1, ppn=4, queue='shared'):
    """ Genereate qsub file for Lammps """
    with open(qsub_path, 'r') as q:
        qsub_lines = q.readlines()

    new_lines = qsub_lines[:3]
    new_lines += ['#PBS -N %s\n' % name]
    new_lines += ['#PBS -q %s\n' % queue]
    new_lines += ['#PBS -l nodes=%i:ppn=%i\n' % (nodes, ppn)]
    new_lines += ['#PBS -l walltime=%s\n' % walltime]
    new_lines += qsub_lines[7:]

    return new_lines

def change_seed(input_lines, seed=None):
    """ Change seed number of Lammps input """
    if seed is None:
        seed = random.randint(100000, 999999)
    for i, line in enumerate(input_lines):
        if 'seed equal' in line:
            seed_index = i
    input_lines[seed_index] = 'variable        seed equal %i\n' % seed
    return input_lines


def change_pair_coeff(input_lines, coefficient_list):
    """ Change pair coefficients of Lammps input
        Coefficient list format:
            - [[id1, id2, eps, sig], ...] """
    pair_indices = []
    for i, line in enumerate(input_lines):
        if 'pair_coeff' in line:
            pair_indices.append(i)
    pair_lines = []
    for coefficient in coefficient_list:
        id1, id2, eps, sig = coefficient
        pair_lines.append('pair_coeff      %i %i %.3f %.3f\n' % (id1, id2, eps, sig))

    new_lines = sample_lines[:pair_indices[0]] + pair_lines + sample_lines[pair_indices[-1]+1:]
    return new_lines

def change_masses(input_lines, masses):
    """ Change atoms masses of Lammps input
        Masses list format:
            - [atom1, mass1, atom2, mass2] """
    mass_indices = []
    for i, line in enumerate(input_lines):
        if 'Masses' in line:
            mass_indices.append(i+2)
        if 'Atoms' in line:
            mass_indices.append(i-1)

    mass_lines = []
    for m in masses:
        atom_type, atom_mass = m
        mass_lines.append('%i %.3f\n' % (atom_type, atom_mass))
    new_lines = input_lines[:mass_indices[0]] + mass_lines + input_lines[mass_indices[-1]:]
    return new_lines
