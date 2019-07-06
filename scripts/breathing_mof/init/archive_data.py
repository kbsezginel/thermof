"""
Archive finished simulations to zfs.
"""
import os
import sys
import glob
import shutil
from lammps_tools import check_sim_finished


main_dir = os.path.abspath(sys.argv[1])
archive_dir = '/zfs1/cwilmer/kbs37/breathing_mof/parameter_search_3'

print('Moving from %s to %s' % (main_dir, archive_dir))
for sim in os.listdir(main_dir):
    simdir = os.path.join(main_dir, sim)
    simfin = []
    for run in os.listdir(simdir):
        rundir = os.path.join(simdir, run)
        outfile = os.path.join(rundir, 'lammps_out.txt')
        runfin = False
        if os.path.exists(outfile):
            runfin, runtime = check_sim_finished(outfile)
        simfin.append(runfin)
    if all(simfin):
        print('%5s | ALL runs finished, archiving...' % sim)
        shutil.move(simdir, os.path.join(archive_dir, sim))

    else:
        print('%5s | %i / %i finished, skipping...' % (sim, simfin.count(True), len(simfin)))
