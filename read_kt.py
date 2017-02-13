from teemof.read import read_trials
import sys
import os


main_dir = os.path.join(os.getcwd(), '..', 'Trials')
t0, t1 = 4, 8

if len(sys.argv) > 1:
    trial_folder = 'Trial%s' % sys.argv[-1]
    trial_dir = os.path.join(main_dir, trial_folder)
    print('Reading results from %s' % trial_dir)

    print('Calculating kt between time: %i - %i' % (t0, t1))
    read_trials(trial_dir, t0=t0, t1=t1)
else:
    print('Please enter trial number')
