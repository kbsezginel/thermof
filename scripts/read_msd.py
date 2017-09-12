"""
Reads mean squared displacement for a list of trials and saves results to a yaml file
"""
import os
import yaml
from teemof.trajectory import Trajectory
from teemof.read import read_legend
# --------------------------------------------------------------------------------------------------
main = ''
"""
   FRONT          BACK
1  o---o  2    5  o---o  6
   |   |          |   |
3  o---o  4    7  o---o  8

   x   y   z   #   |  x   y   z   #
1  30  40  40  234 |  35  45  45  3818
2  40  40  40  298 |  45  45  45  3882
3  30  30  40  226 |  35  35  45  3810
4  40  30  40  290 |  45  35  45  3874
5  30  40  30  233 |  35  45  35  3817
6  40  40  30  297 |  45  45  35  3881
7  30  30  30  225 |  35  35  35  3809
8  40  30  30  289 |  45  35  35  3873
"""
box1_atoms = [234, 298, 226, 290, 233, 297, 225, 289]
box2_atoms = [3818, 3882, 3810, 3874, 3817, 3881, 3809, 3873]
ipbox_atoms = box1_atoms + box2_atoms

results_file = '%s-MSD-results.yaml' % os.path.basename(main)
# --------------------------------------------------------------------------------------------------
trial_list = [os.path.join(main, i) for i in os.listdir(main) if os.path.isdir(os.path.join(main, i))]
results = dict(msd1=[], msd2=[], msd=[], md1=[], md2=[], md=[], sigma=[], epsilon=[], trial=[])

for trial_index, trial in enumerate(trial_list, start=1):
    trial_name = os.path.basename(trial)
    print('\n%i / %i | %s #################################' % (trial_index, len(trial_list), trial_name), flush=True)
    if trial_name not in ['S6.00-E0.80', 'S6.00-E1.00']:
        run_list = [os.path.join(trial, i) for i in os.listdir(trial) if os.path.isdir(os.path.join(trial, i))]
        msd1_avg, msd2_avg, msd_avg = [], [], []
        md1_avg, md2_avg, md_avg = [], [], []
        for run in run_list:
            traj_file = os.path.join(run, 'traj.xyz')
            traj = Trajectory(read=traj_file)

            traj_box1 = traj.subdivide(atoms=box1_atoms)
            traj_box1.set_cell([80, 80, 80])
            traj_box1.calculate_distances()
            traj_box1.calculate_mean_disp()
            traj_box1.calculate_mean_squared_disp()
            md1_avg.append(sum(traj_box1.mean_disp) / len(traj_box1.mean_disp))
            msd1_avg.append(sum(traj_box1.mean_squared_disp) / len(traj_box1.mean_squared_disp))

            traj_box2 = traj.subdivide(atoms=box2_atoms)
            traj_box2.set_cell([80, 80, 80])
            traj_box2.calculate_distances()
            traj_box2.calculate_mean_disp()
            traj_box2.calculate_mean_squared_disp()
            md2_avg.append(sum(traj_box2.mean_disp) / len(traj_box2.mean_disp))
            msd2_avg.append(sum(traj_box2.mean_squared_disp) / len(traj_box2.mean_squared_disp))

            traj_ipbox = traj.subdivide(atoms=ipbox_atoms)
            traj_ipbox.set_cell([80, 80, 80])
            traj_ipbox.calculate_distances()
            traj_ipbox.calculate_mean_disp()
            traj_ipbox.calculate_mean_squared_disp()
            md_avg.append(sum(traj_ipbox.mean_disp) / len(traj_ipbox.mean_disp))
            msd_avg.append(sum(traj_ipbox.mean_squared_disp) / len(traj_ipbox.mean_squared_disp))

        results['msd1'].append(sum(msd1_avg) / len(msd1_avg))
        results['md1'].append(sum(md1_avg) / len(md1_avg))
        results['msd2'].append(sum(msd2_avg) / len(msd2_avg))
        results['md2'].append(sum(md2_avg) / len(md2_avg))
        results['msd'].append(sum(md_avg) / len(msd_avg))
        results['md'].append(sum(md_avg) / len(md_avg))
        print('MSD1: %.2f (%i) | MSD2: %.2f (%i) MSD: %.2f (%i)'
              % (results['msd1'][-1], len(msd1_avg), results['msd2'][-1], len(msd2_avg), results['msd'][-1], len(msd_avg)))
    else:
        results['msd1'].append(None)
        results['md1'].append(None)
        results['msd2'].append(None)
        results['md2'].append(None)
        results['msd'].append(None)
        results['md'].append(None)

    results['sigma'].append(read_legend(trial, key='sigma'))
    results['epsilon'].append(read_legend(trial, key='epsilon'))
    results['trial'].append(os.path.basename(trial))

with open(results_file, 'w') as rfile:
    yaml.dump(results, rfile)
