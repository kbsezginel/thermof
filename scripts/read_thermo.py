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
results = dict(temp=[], press=[], e_pair=[], e_mol=[], e_tot=[], epsilon=[], trial=[])
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
        # sim = Simulation(read=trial, setup='trial', parameters=k_par)
        for run in os.listdir(trial):
            run_dir = os.path.join(trial, run)
            thermo = read_thermo(read_log(os.path.join(run_dir, 'log.lammps')))

            thermo_run = {}
            for var in variable_list:
                var_avg = 0
                n_steps = 0
                for fix in fix_list:
                    var_avg += np.average(thermo[fix][var]) * thermo[fix]['step'][-1]
                    n_steps += thermo[fix]['step'][-1]
                var_avg = var_avg / n_steps
                thermo_run[var] = var_avg


        # Get fix average
        # Get variable average
        # Get run average

        trial = read_trial(trial, k_par=k_par, t0=5, t1=10, verbose=False)
        results['k'].append(trial['avg']['k_est']['iso'])
        results['max'].append(trial['avg']['k_est']['stats']['iso']['max'])
        results['min'].append(trial['avg']['k_est']['stats']['iso']['min'])
        results['std'].append(float(trial['avg']['k_est']['stats']['iso']['std']))
        print('k: %.2f | std: %.2f | max: %.2f | min: %.2f'
              % (results['k'][-1], results['std'][-1], results['max'][-1], results['min'][-1]))
    else:
        results['k'].append(None)
        results['std'].append(None)
        results['max'].append(None)
        results['min'].append(None)


with open(results_file, 'w') as rfile:
    yaml.dump(results, rfile)
