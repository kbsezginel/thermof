"""
TherMOF command line interface.
"""
import argparse


parser = argparse.ArgumentParser(
    description="""
----------------------------------------------------------------------------
████████╗██╗  ██╗███████╗██████╗ ███╗   ███╗ ██████╗ ███████╗
╚══██╔══╝██║  ██║██╔════╝██╔══██╗████╗ ████║██╔═══██╗██╔════╝
   ██║   ███████║█████╗  ██████╔╝██╔████╔██║██║   ██║█████╗
   ██║   ██╔══██║██╔══╝  ██╔══██╗██║╚██╔╝██║██║   ██║██╔══╝
   ██║   ██║  ██║███████╗██║  ██║██║ ╚═╝ ██║╚██████╔╝██║
   ╚═╝   ╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝╚═╝     ╚═╝ ╚═════╝ ╚═╝

TherMOF: Thermal transport in Metal-Organic Frameworks
-----------------------------------------------------------------------------
    """,
    epilog="""
Example:
python thermof_write.py IRMOF-1.cif

would read IRMOF-1 cif file, analyze topology, assign force field (default: UFF) and
create input files for a Lammps simulation.
    """,
    formatter_class=argparse.RawDescriptionHelpFormatter)


default_params = {}

# Positional arguments
parser.add_argument('molecule', type=str, help='Molecule file to read.')

# Optional arguments
parser.add_argument('--forcefield', '-ff', default='UFF', type=str, metavar='',
                    help='Force field for molecule file.')

# Parse arguments
args = parser.parse_args()
