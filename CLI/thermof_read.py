"""
TherMOF command line interface.
"""
import os
import argparse
from thermof import Simulation, Parameters, Trajectory
from thermof.parameters import k_parameters, plot_parameters


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
parser.add_argument('simdir', type=str, help='Lammps simulation directory.')

# Optional arguments
parser.add_argument('--setup', '-s', default='run', type=str, metavar='',
                    help='Simulation setup (run | trial | trial_set).')
parser.add_argument('--no_parameters', '-np', action='store_true', default=False,
                    help='Dont read simulation parameters, use default.')
parser.add_argument('--plot', '-p', nargs='+', default=[],
                    help='Plot HCACF, k, and thermodynamic properties.')
parser.add_argument('--kavg', '-k', nargs=2, default=[10, 20],
                    help='Average thermal conductivity btw. given time interval (ps).')
parser.add_argument('--write', '-w', action='store_true', default=False,
                    help='Write results to a file.')

# Parse arguments
args = parser.parse_args()

# Initialize simulation and read
simdir = os.path.abspath(args.simdir)
if args.no_parameters:
    sim = Simulation(setup=args.setup)
else:
    sim = Simulation(setup=args.setup)
    sim.simdir = simdir
    sim.read_parameters()
sim.parameters.thermof['kpar']['t0'] = int(args.kavg[0])
sim.parameters.thermof['kpar']['t1'] = int(args.kavg[1])
sim.read(simdir, setup=args.setup)

# Plotting
if len(args.plot) > 0:
    sim.parameters.plot = plot_parameters.copy()
    sim.parameters.plot['k_sub']['k_est_t0'] = int(args.kavg[0])
    sim.parameters.plot['k_sub']['k_est_t1'] = int(args.kavg[1])
    for plt in args.plot:
        sim.parameters.plot[plt]['save'] = os.path.join(simdir, '%s-%s.png' % (os.path.basename(simdir), plt))
        sim.plot(plt)
