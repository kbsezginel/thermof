"""
Initialize Lammps simulation for given number of runs with same input files but different seed number
"""
import os
import glob
import shutil

# --------------------------------------------------------------------------------------------------
source_dir = ''         # Directory for reading source Lammps simulation files
sim_dir = ''            # Directory for initializing Lammps simulation files
job_name = ''           # Job name for simulations
n_runs = 10
seed_start = 123456
# --------------------------------------------------------------------------------------------------


def change_seed(source_input, dest_input, seed=None):
    """ Change seed number of Lammps input """
    with open(source_input, 'r') as inp_src:
        input_lines = inp_src.readlines()
    if seed is None:
        seed = random.randint(100000, 999999)
    for i, line in enumerate(input_lines):
        if 'seed equal' in line:
            seed_index = i
    input_lines[seed_index] = 'variable        seed equal %i\n' % seed
    with open(dest_input, 'w') as inp_dest:
        for line in input_lines:
            inp_dest.write(line)
    return None


def lammps_qsub(source_qsub, dest_qsub, name='Lammps', walltime='24:00:00', nodes=1, ppn=12, queue='idist_big'):
    """ Genereate qsub file for Lammps for PBS"""
    with open(source_qsub, 'r') as q_src:
        qsub_lines = q_src.readlines()
    new_lines = qsub_lines[:3]
    new_lines += ['#PBS -N %s\n' % name]
    new_lines += ['#PBS -q %s\n' % queue]
    new_lines += ['#PBS -l nodes=%i:ppn=%i\n' % (nodes, ppn)]
    new_lines += ['#PBS -l walltime=%s\n' % walltime]
    new_lines += qsub_lines[7:]
    with open(dest_qsub, 'w') as q_dest:
        for line in new_lines:
            q_dest.write(line)
    return None


input_file = glob.glob(os.path.join(source_dir, 'in.*'))[0]
inp_name = os.path.basename(input_file)
print('Using input file: %s' % input_file)

qsub_file = glob.glob(os.path.join(source_dir, '*qsub*'))[0]
qsub_name = os.path.basename(qsub_file)
print('Using qsub file: %s' % qsub_file)

source_files = [os.path.join(source_dir, i) for i in os.listdir(source_dir)]
source_files.remove(input_file)
source_files.remove(qsub_file)

for run in range(1, n_runs + 1):
    run_dir = os.path.join(sim_dir, 'Run%i' % run)
    os.makedirs(run_dir, exist_ok=True)
    for f in source_files:
        shutil.copy(f, run_dir)
    seed = seed_start + run
    change_seed(input_file, os.path.join(run_dir, inp_name), seed=seed)
    lammps_qsub(qsub_file, os.path.join(run_dir, qsub_name), name='%s-R%i' % (job_name, run))
    print('Run %i --- Seed: %i' % (run, seed))
