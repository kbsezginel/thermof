"""
Calculate diffusivity using velocity autocorrelation.

1. Read autocorreleation files.
2. Integrate and calculate diffusion coefficient
3. Average for all runs and plot
"""
import os
import sys
import yaml
import numpy as np
import matplotlib.pyplot as plt


def plot_d(t, d_drx, trange=(0.05, 0.2), save=None, ylim=(0, 3e-4)):
    fig = plt.figure(figsize=(12, 3), dpi=300)
    fig.subplots_adjust(wspace=0.3)
    t0, t1 = int(len(t) * trange[0]), int(len(t) * trange[1])
    drx = ['x', 'y', 'z']
    for i, d in enumerate(d_drx):
        ax = fig.add_subplot(1, 3, i + 1)
        ax.plot(t, d)
        ax.plot(t[t0:t1], d[t0:t1], c='r')
        dest, dstd = np.average(d[t0:t1]), np.std(d[t0:t1])
        text = '%.1e ± %.1e $cm^2/s$' % (dest, dstd)
        ax.text(t[t0], ylim[1] * 0.92, text, horizontalalignment='left')
        ax.set_title(drx[i])
        plt.ticklabel_format(style='sci', axis='y', scilimits=(0,0))
        ax.set_ylim(ylim)
        ax.set_xlim(-10, 500)
        ax.set_xlabel('Time (ps)')
        ax.set_ylabel('Diffusivity ($cm^2/s$)')
    if save is not None:
        plt.savefig(save, bbox_inches='tight', dpi=300)


def read_velocity_autocorrelation(filename, p=100000, s=5, dt=1):
    with open(filename, 'r') as f:
        lines = f.readlines()
    v2, t = [], []
    for line in lines[-p:]:
        l = line.strip().split()
        v2.append(float(l[3]))
        t.append((float(l[0]) - 1) * dt * s / 1000)
    return v2, t


def integrate_vacf(vacf, n_atoms, dt, s, conversion):
    d = []
    for i, v in enumerate(vacf):
        if i == 0:
            d_t = v / 2
        if i > 0:
            d_t += v
        val = d_t / n_atoms * dt * s * conversion
        d.append(val)
    return d

def main(simdir):
    simlist = sorted(map(int, os.listdir(simdir)))

    # Angle and number of atoms (5 molecules / nm3)
    n_gas_atoms = {90: 2560, 80: 2521, 70: 2405, 60: 2217, 50: 1961, 40: 1645}
    angle = int(input('Enter the angle [90]: ') or '90')
    n_atoms = n_gas_atoms[angle]

    pltdir = os.path.abspath('plt')
    dt = 1.0            # fs
    s = 5               # sampling interval
    p = 100000          # correlation length
    conversion = 0.1    # A2/fs -> cm2/s
    trange = (0.05, 0.25)

    print(f'Found {len(simlist)} directories in {simdir}')
    print(f'Angle: {angle} | Num atoms: {n_atoms} | Timestep: {dt} | Sampling: {s} | Conversion: {conversion}')

    DATA = {}
    d_drx = []
    for drx in ['x', 'y', 'z']:
        DATA[drx] = {}
        v_runs = []
        for simno in simlist:
            filename = os.path.join(simdir, str(simno), f'V0Vt{drx}o.dat')
            v, t = read_velocity_autocorrelation(filename, p=p, s=s, dt=dt)
            d = integrate_vacf(v, n_atoms, dt, s, conversion)
            t0, t1 = int(len(t) * trange[0]), int(len(t) * trange[1])
            DATA[drx][simno]  = float(np.average(d[t0:t1]))
            v_runs.append(v)
        v_avg = np.average(v_runs, axis=0)
        d_avg = integrate_vacf(v_avg, n_atoms, dt, s, conversion)
        DATA[drx]['dest'] = float(np.average(d_avg[t0:t1]))
        DATA[drx]['dest_std'] = float(np.std([DATA[drx][i] for i in simlist]))
        d_drx.append(d_avg)

        text = '%.1e ± %.1e $cm^2/s$' % (DATA[drx]['dest'], DATA[drx]['dest_std'])
        print(f'{drx} | {text}')

    pltfile = os.path.join(pltdir, f'{angle}_d.png')
    plot_d(t, d_drx, save=pltfile)
    datadir = os.path.abspath('data')
    datafile = os.path.join(datadir, f'{angle}_d.yaml')
    with open(datafile, 'w') as f:
        yaml.dump(DATA, f)

if __name__ == "__main__":
    # Simulation directory
    simdir = os.path.abspath(sys.argv[1])
    main(simdir)
