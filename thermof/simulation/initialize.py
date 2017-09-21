# Date: September 2017
# Author: Kutay B. Sezginel
"""
Initialize Lammps simulation using lammps_interface
"""
import os
from lammps_interface.lammps_main import LammpsSimulation
from lammps_interface.structure_data import from_CIF


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
