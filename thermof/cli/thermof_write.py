"""
TherMOF command line interface.
"""
import os
import argparse
from thermof import Simulation
from thermof import Parameters


def main():
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
     >>> python thermof_write.py IRMOF-1.cif

    would read IRMOF-1 cif file, analyze topology, assign force field (default: UFF) and
    create input files for a Lammps simulation.

     >>> python thermof_write.py IRMOF-1.cif --forcefield UFF4MOF --fix MIN NPT NVT NVE --scheduler pbs
    would initialize Lammps simulation files with UFF4MOF force field for following procedure:
    Minimization, NPT, NVT, and NVE emsembles. It would also create a job submission script for pbs scheduler.
        """,
        formatter_class=argparse.RawDescriptionHelpFormatter)

    default_params = {}
    # Positional arguments
    parser.add_argument('molecule', type=str, help='Molecule file to read (must be in .cif format).')

    # Optional arguments
    parser.add_argument('--runs', '-r', default=1, type=int, metavar='',
                        help='Number of runs (different seed number is used for each run).')
    parser.add_argument('--forcefield', '-ff', default='UFF', type=str, metavar='',
                        help='Force field for molecule file ([UFF] / BTW_FF / Dreiding / UFF4MOF / Dubbeldam).')
    parser.add_argument('--fix', nargs='+', default=['NVT'], type=str,
                        help='Lammps fix types (MIN / NPT / NVT / NVE).')
    parser.add_argument('--scheduler', default='slurm', type=str, metavar='',
                        help='Job scheduler (pbs / [slurm] / slurm-scratch).')

    # Parse arguments
    args = parser.parse_args()

    # Initialize simulation
    simpar = Parameters()
    sim = Simulation(mof=args.molecule, parameters=simpar)
    mof_name = os.path.splitext(os.path.basename(args.molecule))[0]
    sim.simdir = os.path.join(os.path.dirname(args.molecule), mof_name)

    sim.parameters.lammps['force_field'] = args.forcefield
    sim.parameters.lammps['mol_ff'] = args.forcefield
    sim.parameters.thermof['fix'] = args.fix
    sim.parameters.job['scheduler'] = args.scheduler
    try:
        if args.runs == 1:
            sim.initialize()
        elif args.runs > 1:
            sim.initialize_runs(args.runs)
    except Exception as e:
        print(e)


if __name__ == '__main__':
    main()
