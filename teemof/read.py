# Read Lammps output files of thermal conductivity measurements
# Date: Februay 2017
# Author: Kutay B. Sezginel
import os
import math


parameters = dict(kb=0.001987, conv=69443.84, dt=5, volume=80 * 80 * 80, temp=300)


def read_kt(file_path, dt=parameters['dt']):
    """ Read kt vs time data from Lammps simulation output file """
    with open(file_path, 'r') as j:
        kt = []
        time = []
        for line_index, line in enumerate(j, start=1):
            if line_index >= 200015:
                l = line.split()
                t = (float(l[0]) - 1) * dt / 1000.0
                kt.append(float(l[3]))
                time.append(t)
    return kt, time


def convert_kt(k_data, param=parameters):
    """ Convert Lammps output data to W/mK thermal conductivity """
    volume = param['volume']
    dt = param['dt']
    k_b = param['kb']
    temp = param['temp']
    conversion = param['conv']
    new_kt = []
    for data_index, data in enumerate(k_data):
        if data_index == 0:
            kt = data / 2 * volume * dt / (k_b * math.pow(temp, 2)) * conversion
            new_kt.append(kt)
        if data_index > 0:
            kt = kt + data * volume * dt / (k_b * math.pow(temp, 2)) * conversion
            new_kt.append(kt)
    return new_kt


def avg_kt(k_data_list):
    """ Calculate average of thermal conductivity for multiple runs """
    n = len(k_data_list[0])
    for i in k_data_list:
        m = len(i)
        if m != n:
            print('Data mismatch', i)
    avg_data = []
    for data_index in range(n):
        data = sum([i[data_index] for i in k_data_list]) / len(k_data_list)
        avg_data.append(data)
    return avg_data


def get_kt(kt, time, t0=5, t1=10):
    """ Get approximate thermal conductivity value for a single run """
    start = time.index(t0)
    end = time.index(t1)
    kt_data = []
    for i in range(start, end):
        kt_data.append(kt[i])
    kt_avg = sum(kt[start:end]) / len(kt[start:end])
    return kt_avg


def read_trials(mult_trial_dir, t0=4, t1=8, verbose=True):
    """ Read multiple trials with multiple runs"""
    trial_data = []
    trial_names = []
    for single_trial in os.listdir(mult_trial_dir):
        single_trial_dir = os.path.join(mult_trial_dir, single_trial)
        if os.path.isdir(single_trial_dir):
            run_data, time, runs_id = read_runs(single_trial_dir, t0=t0, t1=t1, verbose=verbose)
            trial_avg_kt = avg_kt(run_data)
            trial_data.append(trial_avg_kt)
        trial_names.append(single_trial)
    return trial_data, trial_names


def read_runs(trial_dir, t0=4, t1=8, verbose=True):
    """ Read multiple runs for single trial """
    print('\n------ %s ------' % os.path.split(trial_dir)[-1])
    trial_data = []
    runs_id = []
    for run_index, run in enumerate(os.listdir(trial_dir)):
        run_dir = os.path.join(trial_dir, run)
        if os.path.isdir(run_dir):
            runs_id.append(run)
            try:
                k_data_files = check_kt_directions(run_dir)
                run_data = []
                for data_path in k_data_files:
                    kt, time = read_kt(data_path)
                    kt = convert_kt(kt)
                    trial_data.append(kt)
                    run_data.append(kt)
                run_avg_kt = avg_kt(run_data)
                run_message = '%s -> kt: %.3f W/mK -> %i direction(s)' % (run, get_kt(run_avg_kt, time), len(k_data_files))
                print(run_message) if verbose else None
            except Exception as e:
                print('%s -> Could not read, error: %s' % (run, e))
    trial_avg_kt = avg_kt(trial_data)
    approx_kt = get_kt(trial_avg_kt, time, t0=t0, t1=t1)
    print('Average -> %.3f W/mK from %i runs' % (approx_kt, len(trial_data)))
    return trial_data, time, runs_id


def check_kt_directions(run_dir):
    """ Return thermal data for each direction as list """
    run_list = os.listdir(run_dir)
    k_list = []
    for f in run_list:
        if 'J0Jt_t' in f:
            k_list.append(os.path.join(run_dir, f))
    return k_list
