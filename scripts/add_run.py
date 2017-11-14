"""
Copy files for all finished simulations to a new directory, change seed number and job name.

python add_run.py RUN1 RUN1-2
"""
import os
import sys
import glob
import shutil


def check_finished(sim_dir, file_name='lammps_out.txt'):
    finished = False
    dir_list = os.listdir(sim_dir)
    if file_name in dir_list:
        with open(os.path.join(sim_dir, file_name), 'r') as lout:
            lammps_lines = lout.readlines()
        if len(lammps_lines) > 0:
            if 'Total wall time' in lammps_lines[-1]:
                walltime = lammps_lines[-1].split()[-1]
                print('%-20s -> finished in %s' % (os.path.basename(sim_dir), walltime))
                finished = True
            elif any(['log' in f for f in dir_list]):
                print('%-20s -> NOT completed' % os.path.basename(sim_dir))
            else:
                print('%-20s -> ERROR' % os.path.basename(sim_dir))
        else:
            print('%-20s -> NOT started' % os.path.basename(sim_dir))
    else:
        print('%-20s -> Lammps out file not found' % os.path.basename(sim_dir))
    return finished


def change_seed(source_input, dest_input, seed=None, add_seed=1):
    """ Change seed number of Lammps input """
    with open(source_input, 'r') as inp_src:
        input_lines = inp_src.readlines()
    for i, line in enumerate(input_lines):
        if 'seed equal' in line:
            seed_index = i
    if seed is None:
        seed = int(input_lines[seed_index].split()[3]) + add_seed
    input_lines[seed_index] = 'variable        seed equal %i\n' % seed
    with open(dest_input, 'w') as inp_dest:
        for line in input_lines:
            inp_dest.write(line)
    return None


def change_job_name(source_input, dest_input, job_name=None, run=None):
    """ Change job name for Lammps slurm submission """
    with open(source_input, 'r') as inp_src:
        input_lines = inp_src.readlines()
    for i, line in enumerate(input_lines):
        if '--job-name' in line:
            job_index = i
    if job_name is None and run is not None:
        job_name = '%s-%i' % (input_lines[job_index].split('=')[1].strip(), int(run))
    input_lines[job_index] = '#SBATCH --job-name=%s\n' % job_name
    with open(dest_input, 'w') as inp_dest:
        for line in input_lines:
            inp_dest.write(line)
    return None


run_dir = sys.argv[1]
new_run = sys.argv[2]
run_id = int(new_run.split('-')[1])
zfs_dir = '/zfs1/7/cwilmer/kbs37/Lammps/TC'
zfs_run_dir = os.path.join(zfs_dir, run_dir)

if os.path.isdir(new_run):
    del_new_run = input('New run directory exists, delete?: ')
if del_new_run in ['y', 'Y', 'yes']:
    shutil.rmtree(new_run)

results = []
for mof in os.listdir(run_dir):
    mof_dir = os.path.join(run_dir, mof)
    zfs_mof_dir = os.path.join(zfs_run_dir, mof)
    finished = check_finished(zfs_mof_dir)
    if finished:
        results.append(finished)
        # Make new directory
        new_mof_dir = os.path.join(new_run, mof)
        os.makedirs(new_mof_dir)
        # Copy all files
        sim_files = []
        for sf in ['in.*', 'job.*', 'data.*', 'simpar.yaml']:
            sim_files += glob.glob(os.path.join(mof_dir, sf))
        if len(sim_files) != 4:
            print('Simulation files are not 4', sim_files)
        for simf in sim_files:
            shutil.copy(simf, new_mof_dir)
        # Change seed number
        inp_file = os.path.join(mof_dir, 'in.%s' % mof)
        new_inp_file = os.path.join(new_mof_dir, 'in.%s' % mof)
        change_seed(inp_file, new_inp_file, add_seed=run_id)
        # Change job name
        job_file = os.path.join(mof_dir, 'job.%s' % mof)
        new_job_file = os.path.join(new_mof_dir, 'job.%s' % mof)
        change_job_name(job_file, new_job_file, run=run_id)
