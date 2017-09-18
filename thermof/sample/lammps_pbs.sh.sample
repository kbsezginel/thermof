#!/bin/bash

#PBS -j oe
#PBS -N MOF5-333
#PBS -q idist_big
#PBS -l nodes=1:ppn=8
#PBS -l walltime=24:00:00
#PBS -S /bin/bash

echo JOB_ID: $PBS_JOBID JOB_NAME: $PBS_JOBNAME HOSTNAME: $PBS_O_HOST
echo start_time: `date`
cd $PBS_O_WORKDIR
module purge
module load lammps/31Mar17

prun lammps < in.thermof > lammps_out.txt

echo end_time: `date`
# workaround for .out / .err files not always being copied back to $PBS_O_WORKDIR
cp /var/spool/torque/spool/$PBS_JOBID.OU $PBS_O_WORKDIR/$PBS_JOBID$(hostname)_$$.out
cp /var/spool/torque/spool/$PBS_JOBID.ER $PBS_O_WORKDIR/$PBS_JOBID$(hostname)_$$.err
exit
