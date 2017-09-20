# Date: February 2017
# Author: Kutay B. Sezginel
"""
Initialize Lammps input files of thermal conductivity measurements
"""
import os
import yaml
from thermof.sample import samples, thermal_flux_file
from thermof.sample import slurm_file, pbs_file


def get_files(sample_files=samples['ideal_interpenetrated_mof']):
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


def job_submission_file(file_name, parameters):
    """ Generate job submission file from given parameters """
    if parameters.scheduler == 'slurm':
        write_slurm_file(file_name, parameters)
    elif parameters.scheduler == 'pbs':
        write_pbs_file(file_name, parameters)
    else:
        print('Select job scheduler: slurm / pbs')


def write_slurm_file(file_name, parameters):
    """ Write slurm ob submission file """
    with open(slurm_file, 'r') as sf:
        job_lines = sf.readlines()
    job_lines[2] = '#SBATCH --job-name=%s\n' % parameters.name
    job_lines[3] = '#SBATCH --output=%s.out\n' % parameters.name
    job_lines[4] = '#SBATCH --nodes=%i\n' % parameters.nodes
    job_lines[5] = '#SBATCH --ntasks-per-node=%i\n' % parameters.ppn
    job_lines[6] = '#SBATCH --time=%s\n' % parameters.walltime
    job_lines[7] = '#SBATCH --cluster=%s\n' % parameters.cluster
    job_lines[17] = 'mpirun -np ${SLURM_NTASKS} lmp_mpi -in %s > %s\n' % (parameters.input, parameters.output)
    with open(file_name, 'w') as job_file:
        for line in job_lines:
            job_file.write(line)


def write_pbs_file(file_name, parameters):
    """ Write slurm ob submission file """
    with open(slurm_file, 'r') as sf:
        job_lines = sf.readlines()
    job_lines[3] = '#PBS -N %s\n' % parameters.name
    job_lines[4] = '#PBS -q %s\n' % parameters.queue
    job_lines[5] = '#PBS -l nodes=%i:ppn=%i\n' % (parameters.nodes, parameters.ppn)
    job_lines[6] = '#PBS -l walltime=%s\n' % parameters.walltime
    job_lines[15] = 'prun lammps < %s > %s' % (parameters.input, parameters.output)
    with open(file_name, 'w') as job_file:
        for line in job_lines:
            job_file.write(line)


def add_run_info(run_info, run_dir):
    """ Add yaml file to run directory that contains simulation information """
    run_info_path = os.path.join(run_dir, 'run_info.yaml')
    yaml.dump(run_info, open(run_info_path, 'w'))


def add_thermal_flux(input_lines):
    """ Add lines for thermal flux calculation in Lammps to input file """
    with open(thermal_flux_file, 'r') as flux:
        flux_lines = flux.readlines()
    return input_lines + flux_lines
