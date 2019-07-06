"""
Run with directory to the data.
Read parameter search data
Plot average thermal conductivity (both over runs and directions)
Plot 2D histogram.
"""
import os, csv, sys
import numpy as np
import yaml
from thermof_tools import read_volume, read_thermal_flux, calculate_k, estimate_k
from thermof_plot import plot_kest


TERMS = ['', '_bond', '_angle']  # thermal conductivity contribution terms
P = 100000                       # correlation length
S = 5                            # sample interval
DT = 1                           # timestep (fs)
V_IDEAL = 80 * 80 * 80           # mof ideal volume
T0, T1 = 25, 45                  # thermal conductivity read interval
HIST_DATA = {}
main = os.path.abspath(sys.argv[1])
for sim in os.listdir(main):
    sim_dir = os.path.join(main, sim)
    sim_data = {'v': [], 'k': [], 'k_bond': [], 'k_angle': [],
                'j': [], 'j_angle': [], 'j_bond': []}
    for run in os.listdir(sim_dir):
        run_dir = os.path.join(sim_dir, run)

        ## READ VOLUME -------------------------------------
        vol_file = os.path.join(run_dir, 'vol_angles.csv')
        vol_data = read_volume(vol_file)
        v_avg = sum(vol_data['v']) / len(vol_data['v'])
        v_ratio = v_avg / v_ideal * 100
        sim_data['v'].append(v_ratio)

        ## READ THERMAL FLUX -------------------------------
        for trm in TERMS:
            for drx in ['x', 'y', 'z']:
                flux_file = os.path.join(run_dir, 'J0Jt_t%s%s.dat' % (drx, term))
                flux, time = read_thermal_flux(flux_file)
                k = calculate_k(flux, v_avg)
                sim_data['k%s' % trm].append(k)
    # Average multiple runs and directions for each term
    for trm in TERMS:
        sim_data['k%s' % trm] = np.average(sim_data['k%s' % trm], axis=0)
    sim_data['v'] = sum(sim_data['v']) / len(sim_data['v'])
    sim_data['k_est'] = estimate_k(sim_data['k'], time, t0=T0, t1=T1)

    # Plot thermal conductivity and HCACF

    # Histogram data
    HIST_DATA[sim] = {'k': sim_data['k_est'], 'v': sim_data['v']}
    print('%8s | k: %5.2f | V: %.1f' % (sim, sim_data['k_est'], sim_data['v']))


with open('parameter_search_data.yaml', 'w') as f:
    yaml.dump(HIST_DATA, f)