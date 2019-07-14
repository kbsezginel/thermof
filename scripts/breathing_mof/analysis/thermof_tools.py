"""
Thermal conductivity helper functions.
"""
import os, csv
import numpy as np


def check_sim_finished(outfile):
    with open(outfile, 'r') as f:
        lines = f.readlines()
    fin, time = False, None
    if len(lines) > 0:
        if 'Total wall time' in lines[-1]:
            fin, time = True, lines[-1].split()[3]
    return fin, time


def read_volume(csv_file, skip_headers=True):
    """Read LAMMPS output volume vs timestep csv file"""
    with open(csv_file, 'r') as f:
        csv_reader = csv.reader(f, delimiter=',')
        if skip_headers:
            next(csv_reader, None)
        data = {'t': [], 'v': []}
        for row in csv_reader:
            data['t'].append(int(row[0]))
            data['v'].append(float(row[1]))
    return data


def read_thermal_flux(file_path, p=20000, s=5, dt=1):
    """Read thermal flux output from LAMMPS"""
    with open(file_path, 'r') as f:
        flux_lines = f.readlines()
    flux, time = [], []
    for line in flux_lines[-p:]:
        flux.append(float(line.strip().split()[3]))
        time.append((float(line.strip().split()[0]) - 1) * dt * s / 1000)
    return flux, time


def calculate_k(flux, volume, conv=69443.84, kb=0.001987, temperature=300, s=5, dt=1):
    """Calculate thermal conductivity (W/mK) from thermal flux autocorrelation function
    Args:
        - flux (list): Thermal flux autocorellation read by read_thermal_flux method
        - k_par (dict): Dictionary of calculation parameters
    Returns:
        - list: Thermal conductivity autocorrelation function
    """
    k = flux[0] / 2 * volume * (s * dt) / (kb * np.power(temperature, 2)) * conv
    k_data = [k]
    for J in flux[1:]:
        k = k + J * volume * (s * dt) / (kb * np.power(temperature, 2)) * conv
        k_data.append(k)
    return k_data

def estimate_k(k_data, time, t0=5, t1=10):
    """ Get approximate thermal conductivity value for a single simulation.
    The arithmetic average of k values are taken between given timesteps.
    Args:
        - k_data (list): Thermal conductivity autocorrelation function
        - time (list): Simulation timestep
        - t0: Timestep to start taking average of k values
        - t1: Timestep to end taking average of k values
    Returns:
        - float: Estimate thermal conductivity
    """
    start, end = time.index(t0), time.index(t1)
    return (sum(k_data[start:end]) / len(k_data[start:end]))


def read_run(run_dir, last_npt_step=500, p=20000, s=5, n_timesteps=1000000, dt=1, terms=['', '_bond', '_angle']):
    """Read LAMMPS simulation output (read volume and flux, calculate thermal conductivity)"""
    # READ VOLUME
    vol_file = os.path.join(run_dir, 'vol_angles.csv')
    vol_data = read_volume(vol_file)
    v, t = vol_data['v'][:last_npt_step], vol_data['t'][:last_npt_step]
    v_avg = sum(v) / len(v)
    DATA = {'v': v, 'v_avg': v_avg, 'v_time': t}

    # READ HCACF
    for term in terms:
        for drx in ['x', 'y', 'z']:
            flux_file = os.path.join(run_dir, 'J0Jt_t%s%s.dat' % (drx, term))
            flux, time = read_thermal_flux(flux_file, p=p, s=s, dt=dt)
            k = calculate_k(flux, v_avg, dt=dt)
            DATA['k%s%s' % (drx, term)] = k
            DATA['j%s%s' % (drx, term)] = flux
    DATA['time'] = time
    return DATA

def read_run_thermo(run_dir, header, keys, fixes, dt=1.0, log='log.lammps'):
    """Read thermal conductivity simulation thermo data"""
    log_file = os.path.join(run_dir, log)
    log = read_log(log_file, headers=header)
    thermo = read_thermo(log, keys, fixes)
    # Convert to picoseconds
    for idx, fix in enumerate(fixes):
        # The last NVE timestep is reset during simulation.
        # This adds the last step of previous NVE to the last NVE to make it continuous for plotting
        if idx == len(fixes) - 1:
            nve_start = thermo[fixes[-2]]['step'][-1]
            thermo[fix]['time'] = [(i + nve_start) * dt / 1000 for i in thermo[fix]['step']]
        else:
            thermo[fix]['time'] = [i * dt / 1000 for i in thermo[fix]['step']]
    return thermo

def read_log(log_file, headers='Step Temp E_pair E_mol TotEng Press'):
    """Read log.lammps file and return lines for multiple thermo data
    Args:
        - log_file (str): Lammps simulation log file path
        - headers (str): The headers for thermo data ('Step Temp E_pair E_mol TotEng Press')
    Returns:
        - list: 2D list of thermo lines for all fixes
    """
    with open(log_file, 'r') as log:
        log_lines = log.readlines()

    thermo_start = []
    thermo_end = []
    for line_index, line in enumerate(log_lines):
        if headers in line:
            start = line_index + 1
            thermo_start.append(start)
        if 'Loop time' in line:
            end = line_index
            thermo_end.append(end)

    thermo_data = []
    for s, e in zip(thermo_start, thermo_end):
        thermo_data.append(log_lines[s:e])

    return thermo_data


def read_thermo(thermo_data, headers=['step', 'temp', 'epair', 'emol', 'etotal', 'press'], fix=None):
    """Read thermo data from given thermo log lines
    Args:
        - thermo_data (list): 2D list of thermo lines for all fixes
        - headers (list): The headers for thermo data
        - fix (list): Name of the separate fixes in thermo
    Returns:
        - dict: Thermo data for all fixes separated as: thermo['fix1']['header1'] = ...
    """
    thermo = {}
    if fix is None:
        fix = list(range(len(thermo_data)))
    if len(fix) != len(thermo_data):
        print('Fixes: %s do not match fixes read in log file' % ' | '.join(fix))
    else:
        for t, thermo_fix in enumerate(thermo_data):
            ther = {key: [] for key in headers}
            for data in thermo_fix:
                line = data.strip().split()
                for i, h in enumerate(headers):
                    ther[h].append(float(line[i]))
            thermo[fix[t]] = ther
    return thermo
