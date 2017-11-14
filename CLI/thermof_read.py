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
python thermof_read.py IRMOF-1

would read simulation results from IRMOF-1 directory.
You would need a Lammps log file and simpar.yaml (produced by thermof) to be able to
read simulation results.
    """,
    formatter_class=argparse.RawDescriptionHelpFormatter)


default_params = {}

# Positional arguments
parser.add_argument('simulation-dir', type=str, help='Lammps simulation directory.')

# Optional arguments
parser.add_argument('--plot', '-p', action='store_true', default=False,
                    help='Plot HCACF, k, and thermodynamic properties.')
parser.add_argument('--write', '-w', action='store_true', default=False,
                    help='Write results to a file.')

# Parse arguments
args = parser.parse_args()
