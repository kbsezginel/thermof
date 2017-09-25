# Date: September 2017
# Author: Kutay B. Sezginel
"""
Initialize Lammps simulation using lammps_interface
"""
import os
from lammps_interface.lammps_main import LammpsSimulation
from lammps_interface.structure_data import from_CIF
from thermof.initialize import read_lines, write_lines
from thermof.sample import lammps_input


def write_lammps_files(parameters):
    """
    Write Lammps files using lammps_interface.

    Args:
        - parameters (Parameters): Lammps simulation parameters

    Returns:
        - None: Writes Lammps simulation files to simulation directory
    """
    sim = LammpsSimulation(parameters)
    cell, graph = from_CIF(parameters.cif_file)
    sim.set_cell(cell)
    sim.set_graph(graph)
    sim.split_graph()
    sim.assign_force_fields()
    sim.compute_simulation_size()
    sim.merge_graphs()
    sim.write_lammps_files(parameters.sim_dir)


def get_npt_lines(simpar, npt_file=lammps_input['npt']):
    """
    Get input lines for NPT simulation using thermof_parameters.
    """
    npt_lines = read_lines(npt_file)
    npt_lines[1] = 'variable        pdamp      equal %i*${dt}\n' % simpar['npt']['pdamp']
    npt_lines[2] = 'variable        tdamp      equal %i*${dt}\n' % simpar['npt']['tdamp']
    npt_lines[4] = 'run             %i\n' % simpar['npt']['steps']
    return npt_lines


def get_nvt_lines(simpar, nvt_file=lammps_input['nvt']):
    """
    Get input lines for NVT simulation using thermof_parameters.
    """
    nvt_lines = read_lines(nvt_file)
    npt_lines[2] = 'run             %i\n' % simpar['nvt']['steps']
    return npt_lines


def get_nve_lines(simpar, nve_file=lammps_input['nve']):
    """
    Get input lines for NVE simulation (including thermal conductivity calc.) using thermof_parameters.
    """
    nve_lines = read_lines(nve_file)
    if simpar['nve']['equilibration'] >= 0:
        nve_lines[2] = 'run             %i\n' % simpar['nve']['equilibration']
    else:
        nve_lines = nve_lines[4:]
    nve_lines[42] = 'run             %i\n' % simpar['nve']['steps']
    return nve_lines


def get_simpar_lines(simpar, simpar_file=lammps_input['simpar']):
    """
    Get input lines for Lammps simulation parameters using thermof_parameters.
    """
    simpar_lines = read_lines(simpar_file)
    simpar_lines[1] = 'variable        T equal %i' % simpar['temperature']
    simpar_lines[2] = 'variable        dt equal %.1f' % simpar['dt']
    simpar_lines[3] = 'variable        seed equal %i' % simpar['seed']
    simpar_lines[4] = 'variable        p equal %i' simpar['correlation_length']
    simpar_lines[5] = 'variable        s equal %i' simpar['sample_interval']
    simpar_lines[7] = 'variable        txyz equal %i' % simpar['dump_xyz']
    simpar_lines[11] = 'thermo          %i' % simpar['thermo']
    simpar_lines[12] = 'thermo_style    %s' % ''.join(simpar['thermo_style'])
    return simpar_lines
