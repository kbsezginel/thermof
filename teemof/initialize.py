# Initialize Lammps input files of thermal conductivity measurements
# Date: Februay 2017
# Author: Kutay B. Sezginel
import os
import yaml


sample_dir = os.path.join(os.getcwd(), 'sample')
# Lammps input file with thermal flux measured in single direction
single_inp_path = os.path.join(sample_dir, 'in_single.cond.sample')        # Single MOF
# Lammps input file with thermal flux measured in three directions
single_inp3_path = os.path.join(sample_dir, 'in3_single.cond.sample')      # Single MOF
ipmof_inp3_path = os.path.join(sample_dir, 'in3_ipmof.cond.sample')        # Interpenetrated MOF
# Lammps structure files
single_data_path = os.path.join(sample_dir, 'lammps_single.data.sample')   # Single MOF
ipmof_data_path = os.path.join(sample_dir, 'lammps_ipmof.data.sample')     # Interpenetrated MOF
# Job submission file for Frank
qsub_path = os.path.join(sample_dir, 'lammps_qsub.sh.sample')

sample_files = dict(inp=ipmof_inp3_path, data=ipmof_data_path, qsub=qsub_path)


def get_files(sample_files):
    """ Read selected sample files """
    with open(sample_files['inp'], 'r') as sample_input:
        input_lines = sample_input.readlines()
    with open(sample_files['data'], 'r') as sample_input:
        data_lines = sample_input.readlines()
    with open(sample_files['qsub'], 'r') as qsub_input:
        qsub_lines = qsub_input.readlines()
    return input_lines, data_lines, qsub_lines


def export_lines(file_lines, export_path):
    """ Exports array of lines onto a file """
    with open(export_path, 'w') as f:
        for l in file_lines:
            f.write(l)


def change_seed(input_lines, seed=None):
    """ Change seed number of Lammps input """
    if seed is None:
        seed = random.randint(100000, 999999)
    for i, line in enumerate(input_lines):
        if 'seed equal' in line:
            seed_index = i
    input_lines[seed_index] = 'variable        seed equal %i\n' % seed
    return input_lines


def change_thermo(input_lines, thermo=10000):
    """ Change seed number of Lammps input """
    for i, line in enumerate(input_lines):
        if 'thermo' in line:
            thermo_index = i
    input_lines[thermo_index] = 'thermo          %i\n' % thermo
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

    new_lines = input_lines[:pair_indices[0]] + pair_lines + input_lines[pair_indices[-1] + 1:]
    return new_lines


def change_masses(data_lines, masses):
    """ Change atoms masses of Lammps.data file
        Masses list format:
            - [[atom1, mass1], [atom2, mass2], ...] """
    mass_indices = []
    for i, line in enumerate(data_lines):
        if 'Masses' in line:
            mass_indices.append(i + 2)
        if 'Atoms' in line:
            mass_indices.append(i - 1)

    mass_lines = []
    for m in masses:
        atom_type, atom_mass = m
        mass_lines.append('%i %.3f\n' % (atom_type, atom_mass))
    new_lines = data_lines[:mass_indices[0]] + mass_lines + data_lines[mass_indices[-1]:]
    return new_lines


def lammps_qsub(qsub_lines, name='Lammps', walltime='12:00:00', nodes=1, ppn=4, queue='shared'):
    """ Genereate qsub file for Lammps """
    new_lines = qsub_lines[:3]
    new_lines += ['#PBS -N %s\n' % name]
    new_lines += ['#PBS -q %s\n' % queue]
    new_lines += ['#PBS -l nodes=%i:ppn=%i\n' % (nodes, ppn)]
    new_lines += ['#PBS -l walltime=%s\n' % walltime]
    new_lines += qsub_lines[7:]

    return new_lines


def add_run_info(run_info, run_dir):
    """ Add yaml file to run directory that contains simulation information """
    run_info_path = os.path.join(run_dir, 'run_info.yaml')
    yaml.dump(run_info, open(run_info_path, 'w'))
