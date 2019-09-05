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
p = int(input('Enter correlation length (p) in timesteps [100000]: ') or '100000')
s = int(input('Enter dump interval (s) in timesteps [5]: ') or '5')
dt = float(input('Enter timestep (dt) [1.0]: ') or '1.0')
angle = float(input('Enter angle (degrees) [90]: ') or '90')
kest = input('Estimate k between [0.7, 1.0] in fractions: ') or '0.7, 1.0'
kest = tuple(map(float, kest.split(',')))
V_IDEAL = 80 * 80 * 80 * np.sin(np.deg2rad(angle))
terms = ['', '_bond', '_angle']
print('Using p: %i | s: %i | dt: %.1f | V: %i with terms -> %s' % (p, s, dt, V_IDEAL, ' | '.join(terms)))

pltdir = os.path.join('plt', sim_name)
os.makedirs(pltdir, exist_ok=True)
datadir = os.path.join('data', sim_name)
os.makedirs(datadir, exist_ok=True)

print('Reading data from %s' % sim_dir)
DATA = {}
for run in os.listdir(sim_dir):
    run_dir = os.path.join(sim_dir, run)
    try:
        DATA[run] = read_run(run_dir, p=p, s=s, dt=dt, kest=kest, terms=terms)
    except Exception as e:
        print(f'RUN: {run} | {e}')

# Calculate run averages
AVG_DATA = {}
for drx in ['x', 'y', 'z']:
    for trm in ['', '_bond', '_angle']:
        k_runs, kest_runs = [], []
        for run in DATA:
            kr = DATA[run]['k%s%s' % (drx, trm)]
            k_runs.append(kr)
            t0, t1 = int(kest[0] * len(kr)), int(kest[1] * len(kr))
            kest_runs.append(np.average(kr[t0:t1]))
        k_avg = np.average(k_runs, axis=0)
        AVG_DATA[f'{drx}{trm}'] = {'k': k_avg, 'kest': np.average(k_avg[t0:t1]), 't': DATA[run]['time'],
                                   'kest_avg': np.average(kest_runs), 'kest_std': np.std(kest_runs)}
        print(f'{drx} | {trm} | K (avg): {np.average(k_avg[t0:t1])} (std): {np.std(kest_runs)}')
with open(os.path.join(datadir, f'k_avg_{sim_name}.yaml'), 'w') as f:
    yaml.dump(AVG_DATA, f)

print('Plotting to %s' % pltdir)
# Plot individual runs
for drx in ['x', 'y', 'z']:
    plot_hcacf(DATA, drx=drx, terms=terms,
               save=os.path.join(pltdir, '%s_hcacf_%s.png' % (sim_name, drx)))
    plot_k(DATA, drx=drx, terms=terms,
           save=os.path.join(pltdir, '%s_k_%s.png' % (sim_name, drx)))

# Plot direction averages
plot_hcacf_avg(DATA, terms=terms, save=os.path.join(pltdir, '%s_hcacf_avg.png' % sim_name))
plot_k_avg(AVG_DATA, terms=terms, kest=kest, save=os.path.join(pltdir, '%s_k_avg.png' % sim_name))
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
