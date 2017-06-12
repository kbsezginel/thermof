# Read Lammps output files of thermal conductivity measurements
# Date: Februay 2017
# Author: Kutay B. Sezginel
import os
import math
import yaml
from teemof.reldist import reldist


parameters = dict(kb=0.001987, conv=69443.84, dt=5, volume=80 * 80 * 80, temp=300)


def read_kt(file_path, dt=parameters['dt'], kt_index=3):
    """ Read kt vs time data from Lammps simulation output file """
    with open(file_path, 'r') as j:
        kt = []
        time = []
        for line_index, line in enumerate(j, start=1):
            if line_index >= 200015:
                l = line.split()
                t = (float(l[0]) - 1) * dt / 1000.0
                kt.append(float(l[kt_index]))
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
    print('\n------ %s ------' % os.path.split(trial_dir)[-1]) if verbose else None
    trial_data = []
    runs_id = []
    for run_index, run in enumerate(os.listdir(trial_dir)):
        run_dir = os.path.join(trial_dir, run)
        if os.path.isdir(run_dir):
            try:
                k_data_files, directions = check_kt_directions(run_dir)
                run_data = []
                for direc, data_path in zip(directions, k_data_files):
                    kt, time = read_kt(data_path)
                    kt = convert_kt(kt)
                    trial_data.append(kt)
                    run_data.append(kt)
                    runs_id.append('%s-%s' % (run, direc))
                run_avg_kt = avg_kt(run_data)
                run_message = '%s -> kt: %.3f W/mK -> %i direction(s)' % (run, get_kt(run_avg_kt, time), len(k_data_files))
                print(run_message) if verbose else None
            except Exception as e:
                print('%s -> Could not read, error: %s' % (run, e))
    trial_avg_kt = avg_kt(trial_data)
    approx_kt = get_kt(trial_avg_kt, time, t0=t0, t1=t1)
    print('Average -> %.3f W/mK from %i runs' % (approx_kt, len(trial_data))) if verbose else None
    return trial_data, time, runs_id


def check_kt_directions(run_dir):
    """ Return thermal data for each direction as list """
    run_list = os.listdir(run_dir)
    k_list = []
    directions = []
    for f in run_list:
        if 'J0Jt_t' in f:
            k_list.append(os.path.join(run_dir, f))
            directions.append(f.split('.')[0].split('J0Jt_t')[1])
    return k_list, directions


def read_log(log_path):
    """ Read log.lammps file """
    with open(log_path, 'r') as log:
        log_lines = log.readlines()

    for line_index, line in enumerate(log_lines):
        if 'thermo' in line:
            thermo_step = int(line.split()[1])
        if 'Equilibration and thermalisation' in line:
            nvt_start = line_index + 7
            nvt_steps = int(log_lines[line_index + 4].split()[1])
            nvt_end = int(nvt_steps / thermo_step) + nvt_start + 1
        elif 'Equilibration in nve' in line:
            nve_start = line_index + 5
            nve_steps = int(log_lines[line_index + 2].split()[1])
            nve_end = int(nve_steps / thermo_step) + nve_start + 1

    nvt_lines = log_lines[nvt_start:nvt_end]
    nve_lines = log_lines[nve_start:nve_end]

    nvt_data = read_thermo_data(nvt_lines)
    nve_data = read_thermo_data(nve_lines)

    return nvt_data, nve_data


def read_thermo_data(thermo_data_lines):
    """ Read simulation output data for given lines """
    log_data = dict(step=[], temp=[], pair_eng=[], mol_eng=[], tot_eng=[], press=[])
    for data_line in thermo_data_lines:
        data = data_line.split()
        log_data['step'].append(float(data[0]))
        log_data['temp'].append(float(data[1]))
        log_data['pair_eng'].append(float(data[2]))
        log_data['mol_eng'].append(float(data[3]))
        log_data['tot_eng'].append(float(data[4]))
        log_data['press'].append(float(data[5]))
    return log_data


def read_run_info(run_dir):
    """ Read run info yaml file """
    run_info_path = os.path.join(run_dir, 'run_info.yaml')
    run_info = yaml.load(open(run_info_path, 'r'))
    return run_info


def read_legend(trial_dir, key='name', run='Run1'):
    """ Read legend name from given trial """
    run_dir = os.path.join(trial_dir, run)
    run_info = read_run_info(run_dir)
    return run_info[key]


def read_distance_runs(trial_dir, start=0, end=300000):
    """ Read relative distance data for given trial with multiple runs """
    hist_data = []
    for run in os.listdir(trial_dir):
        traj_path = os.path.join(trial_dir, run, 'traj.xyz')
        x_coords, y_coords, z_coords = reldist(traj_path, end=end)
        x_coords.append(0)
        x_coords.append(1)
        y_coords.append(0)
        y_coords.append(1)

        title = '%s' % run
        sort_param = int(run.split('Run')[1])
        hist_data.append((x_coords[start:], y_coords[start:], z_coords[start:], title, sort_param))

    return sorted(hist_data, key=lambda x: x[4])


def read_distance_trials(trial_set_dir, run='Run1', start=0, end=300000, xkey='sigma'):
    """ Read relative distance data for given trial set """
    hist_data = []
    for i, trial in enumerate(os.listdir(trial_set_dir), start=1):
        trial_dir = os.path.join(trial_set_dir, trial)
        traj_path = os.path.join(trial_dir, run, 'traj.xyz')
        x_coords, y_coords, z_coords = reldist(traj_path, end=end)
        x_coords.append(0)
        x_coords.append(1)
        y_coords.append(0)
        y_coords.append(1)

        leg = read_legend(trial_dir, key='legend')
        sort_param = read_legend(trial_dir, key=xkey)
        title = '%s' % leg
        hist_data.append((x_coords[start:], y_coords[start:], z_coords[start:], title, sort_param))

    return sorted(hist_data, key=lambda x: x[4])
