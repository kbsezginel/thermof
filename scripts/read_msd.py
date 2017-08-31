"""
Reads mean squared displacement for a list of trials and saves results to a yaml file
"""
import os
import yaml
from teemof.trajectory import read_trajectory, msd_distance
from teemof.read import read_legend

# --------------------------------------------------------------------------------------------------
main = ''
ref_atom1 = 298
ref_atom2 = 3809
results_file = '%s-MSD-results.yaml' % os.path.basename(main)
# --------------------------------------------------------------------------------------------------

trial_list = [os.path.join(main, i) for i in os.listdir(main) if os.path.isdir(os.path.join(main, i))]
results = dict(msd1=[], msd2=[], sigma=[], epsilon=[], trial=[])

for trial_index, trial in enumerate(trial_list, start=1):
    trial_name = os.path.basename(trial)
    print('\n%i / %i | %s #################################' % (trial_index, len(trial_list), trial_name), flush=True)
    if trial_name not in ['S6.00-E0.80', 'S6.00-E1.00']:
        run_list = [os.path.join(trial, i) for i in os.listdir(trial) if os.path.isdir(os.path.join(trial, i))]
        msd1_avg = []
        msd2_avg = []
        for run in run_list:
            traj_file = os.path.join(run, 'traj.xyz')
            traj = read_trajectory(traj_file)
            msd1_avg.append(msd_distance(traj['coordinates'], atom=ref_atom1))
            msd2_avg.append(msd_distance(traj['coordinates'], atom=ref_atom2))

        results['msd1'].append(sum(msd1_avg) / len(msd1_avg))
        results['msd2'].append(sum(msd2_avg) / len(msd2_avg))
        print('MSD1: %.2f (%i) | MSD2: %.2f (%i)'
              % (results['msd1'][-1], len(msd1_avg), results['msd2'][-1], len(msd2_avg)))
    else:
        results['msd1'].append(None)
        results['msd2'].append(None)

    results['sigma'].append(read_legend(trial, key='sigma'))
    results['epsilon'].append(read_legend(trial, key='epsilon'))
    results['trial'].append(os.path.basename(trial))

with open(results_file, 'w') as rfile:
    yaml.dump(results, rfile)
