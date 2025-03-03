# Date: February 2017
# Author: Kutay B. Sezginel
"""
Initialize Lammps input files of thermal conductivity measurements
"""
import os
import yaml
from thermof.sample import samples, thermal_flux_file


def get_files(sample_files=samples['ideal_interpenetrated_mof']):
    """ Read selected sample files """
    with open(sample_files['inp'], 'r') as sample_input:
        input_lines = sample_input.readlines()
    with open(sample_files['data'], 'r') as sample_input:
        data_lines = sample_input.readlines()
    with open(sample_files['qsub'], 'r') as qsub_input:
        qsub_lines = qsub_input.readlines()
    return input_lines, data_lines, qsub_lines


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


def add_thermal_flux(input_lines):
    """ Add lines for thermal flux calculation in Lammps to input file """
    with open(thermal_flux_file, 'r') as flux:
        flux_lines = flux.readlines()
    return input_lines + flux_lines
