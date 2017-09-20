"""
Initializing job submission files for computing cluster
"""
from thermof.sample import slurm_file, pbs_file


def job_submission_file(file_name, parameters):
    """ Generate job submission file from given parameters """
    if parameters.scheduler == 'slurm':
        write_slurm_file(file_name, parameters)
    elif parameters.scheduler == 'pbs':
        write_pbs_file(file_name, parameters)
    else:
        print('Select job scheduler: slurm / pbs')


def write_slurm_file(file_name, parameters):
    """ Write slurm ob submission file """
    with open(slurm_file, 'r') as sf:
        job_lines = sf.readlines()
    job_lines[2] = '#SBATCH --job-name=%s\n' % parameters.name
    job_lines[3] = '#SBATCH --output=%s.out\n' % parameters.name
    job_lines[4] = '#SBATCH --nodes=%i\n' % parameters.nodes
    job_lines[5] = '#SBATCH --ntasks-per-node=%i\n' % parameters.ppn
    job_lines[6] = '#SBATCH --time=%s\n' % parameters.walltime
    job_lines[7] = '#SBATCH --cluster=%s\n' % parameters.cluster
    job_lines[17] = 'mpirun -np ${SLURM_NTASKS} lmp_mpi -in %s > %s\n' % (parameters.input, parameters.output)
    with open(file_name, 'w') as job_file:
        for line in job_lines:
            job_file.write(line)


def write_pbs_file(file_name, parameters):
    """ Write slurm ob submission file """
    with open(slurm_file, 'r') as sf:
        job_lines = sf.readlines()
    job_lines[3] = '#PBS -N %s\n' % parameters.name
    job_lines[4] = '#PBS -q %s\n' % parameters.queue
    job_lines[5] = '#PBS -l nodes=%i:ppn=%i\n' % (parameters.nodes, parameters.ppn)
    job_lines[6] = '#PBS -l walltime=%s\n' % parameters.walltime
    job_lines[15] = 'prun lammps < %s > %s' % (parameters.input, parameters.output)
    with open(file_name, 'w') as job_file:
        for line in job_lines:
            job_file.write(line)
