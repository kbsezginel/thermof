"""
Calculate diffusivity using velocity autocorrelation.

1. Read autocorreleation files.
2. Integrate and calculate diffusion coefficient
3. Average for all runs and plot
"""
import os
import sys
import numpy as np
import matplotlib.pyplot as plt


def plot_vacf(t, v, d, text='', trange=(0.05, 0.2), save=None):
    fig = plt.figure(figsize=(9, 3), dpi=300)
    fig.subplots_adjust(wspace=0.2)

    ax = fig.add_subplot(1, 2, 1)
    ax.plot(t, v)
    ax.set_xlabel('Time')
    ax.set_ylabel('ACF')

    ax = fig.add_subplot(1, 2, 2)
    ax.plot(t, d)
    t0, t1 = int(len(t) * trange[0]), int(len(t) * trange[1])
    ax.plot(t[t0:t1], d[t0:t1], c='r')
    dest = np.average(d[t0:t1])
    ax.plot([t[t0], t[t1]], [dest, dest], c='k')
    ax.text(t[t0], dest * 0.85, text, horizontalalignment='left')
    ax.set_xlabel('Time')
    ax.set_ylabel('Integral')
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


def integrate_vacf(vacf, n_atoms, dt, conversion):
    d = []
    for i, v in enumerate(vacf):
        if i == 0:
            d_t = v / 2
        if i > 0:
            d_t += v
        val = d_t / n_atoms * dt * conversion
        d.append(val)
    return d

def main(simdir):
    simlist = sorted(map(int, os.listdir(simdir)))

    # Angle and number of atoms (5 molecules / nm3)
    n_gas_atoms = {90: 2560, 80: 2521, 70: 2405, 60: 2217, 50: 1961, 40: 1645}
    angle = int(input('Enter the angle [90]: ') or '90')
    n_atoms = n_gas_atoms[angle]

    pltdir = os.path.abspath('plt')
    pltfile = os.path.join(pltdir, f'{angle}_d.png')
    dt = 1.0            # fs
    conversion = 1e-5   # A2/s -> cm2/s
    trange = (0.05, 0.25)

    print(f'Found {len(simlist)} directories in {simdir}')
    print(f'Angle: {angle} | Num atoms: {n_atoms} | Timestep: {dt} | Conversion {conversion}')

    DATA = {'dest': []}
    allv = []
    for simno in simlist:
        for drx in ['x', 'y', 'z']:
            filename = os.path.join(simdir, str(simno), f'V0Vt{drx}o.dat')
            v, t = read_velocity_autocorrelation(filename)
            d = integrate_vacf(v, n_atoms, dt, conversion)
            t0, t1 = int(len(t) * trange[0]), int(len(t) * trange[1])
            DATA['dest'].append(np.average(d[t0:t1]))
            allv.append(v)

    DATA['t'] = t
    DATA['v'] = np.average(allv, axis=0)
    DATA['d'] = integrate_vacf(DATA['v'], n_atoms, dt, conversion)
    DATA['dest_avg'] = np.average(DATA['d'][t0:t1])
    DATA['dest_std'] = np.std(DATA['dest'])

    text = '%.1e ± %.1e $cm^2/s$' % (DATA['dest_avg'], DATA['dest_std'])
    plot_vacf(DATA['t'], DATA['v'], DATA['d'], text=text, save='test.png')


if __name__ == "__main__":
    # Simulation directory
    simdir = os.path.abspath(sys.argv[1])
    main(simdir)
