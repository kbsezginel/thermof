"""
Add runs with different seed numbers.
>>> python add_runs.py simdir
Would create run directories in simdir starting from 2 using 1 as reference.
"""
import os, sys
import shutil
from glob import glob
from lammps_tools import change_job_name


refno = input('Enter reference (start) sim no [1]: ') or '1'
start_seed = int(input('Enter starting seed no [123456]: ') or '123456')
nruns = int(input('Enter number of total runs: '))
job_name = input('Enter job name: ')
# File name prefixes for glob to find files
data_file_name = 'data.*'
in_file_name = 'in.*'
job_file_name = 'job.*'

simdir = os.path.abspath(sys.argv[1])
refdir = os.path.join(simdir, refno)

def change_seed(source_input, dest_input, seed=999999):
    """ Change seed number of Lammps input """
    with open(source_input, 'r') as inp_src:
        input_lines = inp_src.readlines()
    for i, line in enumerate(input_lines):
        if 'seed equal' in line:
            input_lines[i] = 'variable        seed equal %i\n' % seed
    with open(dest_input, 'w') as inp_dest:
        for line in input_lines:
            inp_dest.write(line)
    return None


for run in range(int(refno) + 1, int(refno) + nruns):
    rundir = os.path.join(simdir, str(run))
    print('Adding -> %s' % rundir)
    os.makedirs(rundir, exist_ok=True)
    # Data file
    data_file = glob(os.path.join(refdir, data_file_name))[0]
    shutil.copy(data_file, rundir)
    # Change seed number
    in_file = glob(os.path.join(refdir, in_file_name))[0]
    change_seed(in_file, os.path.join(rundir, os.path.basename(in_file)), seed=start_seed + run)
    # Change job name
    job_file = glob(os.path.join(refdir, job_file_name))[0]
    change_job_name(job_file, os.path.join(rundir, os.path.basename(job_file)), job_name='%s-%i' % (job_name, run))
