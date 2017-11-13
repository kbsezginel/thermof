# Date: September 2017
# Author: Kutay B. Sezginel
"""
Initializing job submission files for computing cluster
"""
import os
from thermof.sample import slurm_file, slurm_scratch_file, pbs_file
from . import read_lines, write_lines


def job_submission_file(simdir, parameters, verbose=True):
    """ Generate job submission file from given parameters """
    jobpar = parameters.job
    file_name = os.path.join(simdir, '%s.%s' % (jobpar['prefix'], jobpar['name']))
    print('III. Writing %s job submission file -> %s' % (jobpar['scheduler'], file_name)) if verbose else None
    if jobpar['scheduler'] == 'slurm':
        write_slurm_file(file_name, jobpar, sample=slurm_file)
    elif jobpar['scheduler'] == 'slurm-scratch':
        write_slurm_file(file_name, jobpar, sample=slurm_scratch_file)
    elif jobpar['scheduler'] == 'pbs':
        write_pbs_file(file_name, jobpar, sample=pbs_file)
    else:
        print('Select job scheduler: slurm / slurm-scratch / pbs')


def write_slurm_file(file_name, jobpar, sample):
    """ Write slurm job submission file """
    job_lines = read_lines(sample)
    job_lines[2] = '#SBATCH --job-name=%s\n' % jobpar['name']
    job_lines[3] = '#SBATCH --output=%s.out\n' % jobpar['name']
    job_lines[4] = '#SBATCH --nodes=%i\n' % jobpar['nodes']
    job_lines[5] = '#SBATCH --ntasks-per-node=%i\n' % jobpar['ppn']
    job_lines[6] = '#SBATCH --time=%s\n' % jobpar['walltime']
    job_lines[7] = '#SBATCH --cluster=%s\n' % jobpar['cluster']
    if jobpar['scheduler'] == 'slurm':
        job_lines[18] = 'srun --mpi=pmi2 lmp_mpi -in %s > %s\n' % (jobpar['input'], jobpar['output'])
    elif jobpar['scheduler'] == 'slurm-scratch':
        job_lines[24] = 'zfs=%s\n' % jobpar['zfsdir']
        job_lines[38] = 'lmpdir=%s\n' % (jobpar['lmpdir'])
        job_lines[39] = 'srun --mpi=pmi2 $lmpdir -in %s > %s\n' % (jobpar['input'], jobpar['output'])
    write_lines(file_name, job_lines)


def write_pbs_file(file_name, jobpar, sample):
    """ Write PBS job submission file """
    job_lines = read_lines(sample)
    job_lines[3] = '#PBS -N %s\n' % jobpar['name']
    job_lines[4] = '#PBS -q %s\n' % jobpar['queue']
    job_lines[5] = '#PBS -l nodes=%i:ppn=%i\n' % (jobpar['nodes'], jobpar['ppn'])
    job_lines[6] = '#PBS -l walltime=%s\n' % jobpar['walltime']
    job_lines[15] = 'prun lammps < %s > %s' % (jobpar['input'], jobpar['output'])
    write_lines(file_name, job_lines)
