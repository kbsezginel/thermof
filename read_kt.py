from lammps_results import read_trials
import sys
import os

trial_folder = 'Trial%s' % sys.argv[-1]
trial_dir = os.path.join(os.getcwd(), 'Results', trial_folder)
print('Reading results from %s' % trial_dir)

t0, t1 = 5, 10
print('Calculating kt between time: %i - %i' % (t0, t1))
read_trials(trial_dir)
