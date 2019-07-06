"""
Scan a range of parameters for bonds and angles.
"""
import os, sys
import shutil
import numpy as np
from lammps_tools import change_input_variables, change_job_name


k_bond = np.arange(1, 11, 1)
k_angle = np.arange(1, 11, 1)
n_runs = 5

main = '/ihome/cwilmer/kbs37/breathing_mof/parameter_search'
refdir = '/ihome/cwilmer/kbs37/breathing_mof/ref'
ref_inp = os.path.join(refdir, 'in.breathing_mof')
ref_data = os.path.join(refdir, 'data.breathing_mof')
ref_job = os.path.join(refdir, 'job.lammps')

nsim = 0
nrun = 0
for kb in k_bond:
    for ka in k_angle:
        seed = 123456
        nsim += 1
        for run in range(1, n_runs + 1):
            print('\rk_angle: %3i | k_bond: %3i | Run: %2i' % (ka, kb, run), end='')
            simdir = os.path.join(main, '%i-%i' % (kb, ka))
            rundir = os.path.join(simdir, str(run))
            os.makedirs(rundir, exist_ok=True)
            variables = {'seed': seed, 'k_angle': ka, 'k_bond': kb}
            shutil.copy(ref_data, os.path.join(rundir, 'data.breathing_mof'))
            change_job_name(ref_job, os.path.join(rundir, 'job.lammps'),
                            job_name='bmof-%i-%i-%i' % (kb, ka, run))
            change_input_variables(ref_inp, os.path.join(rundir, 'in.breathing_mof'), variables)
            seed += 1
            nrun +=1

print('\n------\n%i simulations | %i runs generated' % (nsim, nrun))
