"""
Plot thermal conductivity results for breathing mof.
"""
import os, sys
from thermof_tools import check_sim_finished


sim_dir = os.path.abspath(sys.argv[1])
sim_name = os.path.basename(sim_dir)
print('Reading data from %s' % sim_dir)
fin = {}
for run in os.listdir(sim_dir):
    outfile = os.path.join(sim_dir, run, 'lammps_out.txt')
    try:
        fin[run] = check_sim_finished(outfile)
        print(f'RUN: {run:2s} | FIN: {fin[run][0]:2} | TIME: {fin[run][1]:15s}')
    except Exception as e:
        print('RUN: {run} | {e}')

nfin = [fin[run][0] for run in fin].count(True)
print(f'{nfin} / {len(fin)} finished!')

