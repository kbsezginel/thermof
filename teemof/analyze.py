# Analyze thermal conductivity results
# Date: June 2017
# Author: Kutay B. Sezginel
import os
import numpy as np
from teemof.read import avg_kt, get_kt, read_runs, read_legend


def analyze_trial_set(trial_set_dir, xkey='mass2', sort=True, t0=10, t1=20):
    """ Read thermal conductivity for a set of trials, get approximate kt values """
    trial_error, trial_std, x_data, y_data = [], [], [], []
    for trial in os.listdir(trial_set_dir):
        # Read each direction and and each run for given trial (30 data list)
        trial_dir = os.path.join(trial_set_dir, trial)
        run_data, time, runs_id = read_runs(trial_dir, verbose=False)

        # Get avg kt for each direction and each run
        run_kt = []
        for d in run_data:
            run_avg = get_kt(d, time, t0=10, t1=20)
            run_kt.append(run_avg)

        # Calculate standard deviation and error
        run_std = np.std(run_kt)
        trial_std.append(run_std)

        min_kt, max_kt = min(run_kt), max(run_kt)
        trial_error.append([min_kt, max_kt])

        # Get average thermal conductivity for trial
        avg_data = avg_kt(run_data)
        trial_kt = get_kt(avg_data, time, t0=t0, t1=t1)
        y_data.append(trial_kt)

        x_value = read_legend(trial_dir, key=xkey)
        x_data.append(x_value)

    if sort:
        x = [i[0] for i in sorted(zip(x_data, y_data))]
        y = [i[1] for i in sorted(zip(x_data, y_data))]
    else:
        x, y = x_data, y_data

    return dict(x=x, y=y, err=trial_error, std=trial_std)
