"""
Plot thermal conductivity results for breathing mof.
"""
import os, sys
import numpy as np
from thermof_tools import read_run, read_run_thermo
from thermof_plot import plot_hcacf, plot_hcacf_avg, plot_thermo
from thermof_plot import plot_k, plot_k_avg, plot_volume


sim_dir = os.path.abspath(sys.argv[1])
sim_name = os.path.basename(sim_dir)
p = int(input('Enter correlation length (p) in timesteps [20000]: ') or '20000')
s = int(input('Enter dump interval (s) in timesteps [5]: ') or '5')
dt = float(input('Enter timestep (dt) [1.0]: ') or '1.0')
angle = float(input('Enter angle (degrees) [90]: ') or '90')
V_IDEAL = 80 * 80 * 80 * np.sin(np.deg2rad(angle))
terms = ['', '_bond', '_angle']
print('Using p: %i | s: %i | dt: %.1f | V: %i with terms -> %s' % (p, s, dt, V_IDEAL, ' | '.join(terms)))

pltdir = os.path.join('plt', sim_name)
os.makedirs(pltdir, exist_ok=True)

print('Reading data from %s' % sim_dir)
DATA = {}
for run in os.listdir(sim_dir):
    run_dir = os.path.join(sim_dir, run)
    run_data = read_run(run_dir, p=p, s=s, dt=dt, terms=terms)
    DATA[run] = run_data

print('Plotting to %s' % pltdir)
for drx in ['x', 'y', 'z']:
    plot_hcacf(DATA, drx=drx, terms=terms,
               save=os.path.join(pltdir, '%s_hcacf_%s.png' % (sim_name, drx)))
    plot_k(DATA, drx=drx, terms=terms,
           save=os.path.join(pltdir, '%s_k_%s.png' % (sim_name, drx)))
plot_hcacf_avg(DATA, terms=terms, save=os.path.join(pltdir, '%s_hcacf_avg.png' % sim_name))
plot_k_avg(DATA, terms=terms, save=os.path.join(pltdir, '%s_k_avg.png' % sim_name))
plot_volume(DATA, V_IDEAL=V_IDEAL, time_conv=0.001*dt,
            save=os.path.join(pltdir, '%s_volume.png' % sim_name))
print('Done!')

# THERMO --------------------------------------------------------------------------------
header = 'Step Temp TotEng E_angle E_bond Volume Lx Ly Lz'
keys = ['step', 'temp', 'etot', 'eangle', 'ebond', 'volume', 'lx' 'ly', 'lz']
fixes = ['NPT', 'NVT', 'NVE1', 'NVE2']

print('Reading thermo data...')
THERMO = {}
for run in os.listdir(sim_dir):
    run_dir = os.path.join(sim_dir, run)
    THERMO[run] = read_run_thermo(run_dir, header, keys, fixes)
print('Plotting thermo...')
plot_thermo(THERMO, variable='temp', add_line=300, legend_loc=4,
            save=os.path.join(pltdir, '%s_temperature.png' % sim_name))
plot_thermo(THERMO, variable='etot', legend_loc=4,
            save=os.path.join(pltdir, '%s_etot.png' % sim_name))
print('Done!')
