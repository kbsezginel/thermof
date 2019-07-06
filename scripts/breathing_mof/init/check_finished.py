"""
Check if simulatio results are finished in a given directory.
Each simulation should have directories with runs.
Cleanup and submit new simulation if not finished (optional).
"""
import os
import sys
import glob
import shutil
import subprocess
from lammps_tools import check_sim_finished

maindir = os.path.abspath(sys.argv[1])

def cleanup_run(rundir):
    keep_files = ['in.breathing_mof', 'data.breathing_mof', 'job.lammps']
    fdel = 0
    for f in os.listdir(rundir):
        if f not in keep_files:
            os.remove(os.path.join(rundir, f))
            fdel += 1
    print('%i files removed from %s' % (fdel, rundir))

nsim = 0
nofin, fin = [], []
for sim in os.listdir(maindir):
    simdir = os.path.join(maindir, sim)
    for run in os.listdir(simdir):
        rundir = os.path.join(simdir, run)
        # Check if sim finished
        outfile = os.path.join(rundir, 'lammps_out.txt')
        runfin = False
        if os.path.exists(outfile):
            runfin, runtime = check_sim_finished(outfile)
            if runfin:
                fin.append((sim, run))
                print('%s | %s finished in %s' % (sim, run, runtime))
        if not runfin:
            nofin.append((sim, run))
            print('%s | %s NOT FINISHED!' % (sim, run))
        nsim += 1

print('%i / %i simulations finished | %i not finished' % (len(fin), nsim, len(nofin)))

cleanup = input('Cleanup unfinished? (y / n): ')
resub = input('Resubmit? (y / n): ')
if resub == 'y':
    num_resub = int(input('Resubmit how many? (all: %i): ' % len(nofin)) or str(len(nofin)))
else:
    num_resub = 0

for sim_idx, run in enumerate(nofin):
    rundir = os.path.join(maindir, run[0], run[1])
    if cleanup == 'y':
        cleanup_run(rundir)
    if resub == 'y' and num_resub > sim_idx:
        # Submit job
        subprocess.run(['sbatch', 'job.lammps'], cwd=rundir)
