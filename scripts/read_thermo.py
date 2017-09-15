"""
Reads thermo data for a list of trials and saves results to a yaml file
"""
import os
import yaml
import numpy as np
from thermof.parameters import k_parameters
from thermof.read import read_run_info, read_thermo, read_log

# --------------------------------------------------------------------------------------------------
main = ''                                                           # Directory of trials
results_file = '%s-kest-results.yaml' % os.path.basename(main)      # Name of results file
# --------------------------------------------------------------------------------------------------
trial_list = [os.path.join(main, i) for i in os.listdir(main) if os.path.isdir(os.path.join(main, i))]
results = dict(temp=[], press=[], e_pair=[], e_mol=[], tot_eng=[], epsilon=[], sigma=[], trial=[])
k_par = k_parameters.copy()
fix_list = ['NVE1', 'NVE2', 'NVT']
var_list = ['e_pair', 'temp', 'e_mol', 'tot_eng', 'press']

for trial_index, trial in enumerate(trial_list, start=1):
    trial_name = os.path.basename(trial)
    print('\n%i / %i | %s #################################' % (trial_index, len(trial_list), trial_name), flush=True)

    ri = read_run_info(os.path.join(trial, 'Run1'))
    results['sigma'].append(ri['sigma'])
    results['epsilon'].append(ri['epsilon'])
    results['trial'].append(os.path.basename(trial))

    if trial_name not in ['S6.00-E0.80', 'S6.00-E1.00']:
        for run in os.listdir(trial):
            run_dir = os.path.join(trial, run)
            thermo = read_thermo(read_log(os.path.join(run_dir, 'log.lammps')))

            thermo_run = {}
            for var in var_list:
                var_avg = 0
                n_steps = 0
                thermo_run[var] = []
                # Get fix average
                for fix in fix_list:
                    var_avg += np.average(thermo[fix][var]) * thermo[fix]['step'][-1]
                    n_steps += thermo[fix]['step'][-1]
                var_avg = var_avg / n_steps
                thermo_run[var].append(var_avg)
        # Get run average
        for var in var_list:
            results[var].append(float(np.average(thermo_run[var])))

        print('T: %.2f | P: %.2f | E_tot: %.2f'
              % (results['temp'][-1], results['press'][-1], results['tot_eng'][-1]))
    else:
        for var in var_list:
            results[var].append(None)

with open(results_file, 'w') as rfile:
    yaml.dump(results, rfile)
