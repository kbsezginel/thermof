"""
TherMOF plot functions for breathing MOF thermal transport analysis.
Date: July 2019
Author: Kutay B. Sezginel
"""
import matplotlib.pyplot as plt
import numpy as np

def plot_hcacf(DATA, drx='x', terms=['', '_bond', '_angle'],
               figsize=(20, 5), dpi=300, hspace=0.45, wspace=0.2, ncol=5,
               xlabel='Time (ps)', ylabel='HCACF',
               ylim=(None, None), xlim=(None, None), save=None):
    """
    Plot HCACF for breathing mof.
    drx : ['x', 'y', 'z'] Direction
    terms : HCACF contribution by total, bonds, angles
    """
    fig = plt.figure(figsize=figsize, dpi=dpi)
    fig.subplots_adjust(hspace=hspace, wspace=wspace)
    run_list = [str(i) for i in sorted([int(i) for i in DATA])]
    nrow = np.ceil(len(run_list) / ncol)
    for idx, run in enumerate(run_list, start=1):
        ax = fig.add_subplot(nrow, ncol, idx)
        for t in terms:
            ax.plot(DATA[run]['time'], DATA[run]['j%s%s' % (drx, t)], alpha=0.9)
        ax.set_title('%s (%s)' % (run, drx))
        ax.set_xlabel(xlabel)
        ax.set_ylabel(ylabel)
        ax.set_ylim(ylim)
        ax.set_xlim(xlim)
        if idx == 1:
            ax.legend(['k%s%s' % (drx, t) for t in terms], loc=1, frameon=False)
    if save is not None:
        plt.savefig(save, transparent=True, bbox_inches='tight', dpi=dpi)

def plot_hcacf_avg(DATA, terms=['', '_bond', '_angle'],
                   figsize=(15, 3), dpi=300, hspace=0.3, wspace=0.2,
                   xlabel='Time (ps)', ylabel='HCACF',
                   ylim=(None, None), xlim=(None, None), save=None):
    """
    Plot HCACF average for breathing mof.
    terms : HCACF contribution by total, bonds, angles
    """
    fig = plt.figure(figsize=figsize, dpi=dpi)
    fig.subplots_adjust(hspace=hspace, wspace=wspace)
    for plt_idx, drx in enumerate(['x', 'y', 'z'], start=1):
        AVG_DATA = {}
        for t in terms:
            AVG_DATA['j%s%s' % (drx, t)] = []
        run_list = [str(i) for i in sorted([int(i) for i in DATA])]
        for idx, run in enumerate(run_list, start=1):
            for trm in AVG_DATA:
                AVG_DATA[trm].append(DATA[run][trm])
        for trm in AVG_DATA:
            AVG_DATA[trm] = np.average(AVG_DATA[trm], axis=0)

        ax = fig.add_subplot(1, 3, plt_idx)
        legend = []
        for trm in AVG_DATA:
            ax.plot(DATA['1']['time'], AVG_DATA[trm])
            legend.append(trm)
        ax.legend(legend, loc=1, frameon=False)
        ax.set_xlabel(xlabel)
        ax.set_ylabel(ylabel)
        ax.set_ylim(ylim)
        ax.set_xlim(xlim)
    if save is not None:
        plt.savefig(save, transparent=True, bbox_inches='tight', dpi=dpi)


def plot_k(DATA, drx='x', terms=['', '_bond', '_angle'],
           figsize=(20, 5), dpi=300, hspace=0.45, wspace=0.2, ncol=5,
           xlabel='Time (ps)', ylabel='k (W / mK)',
           ylim=(None, None), xlim=(None, None), save=None):
    """
    Plot k for breathing mof.
    drx : ['x', 'y', 'z'] Direction
    terms : k contribution by total, bonds, angles
    """
    fig = plt.figure(figsize=figsize, dpi=dpi)
    fig.subplots_adjust(hspace=hspace, wspace=wspace)
    run_list = [str(i) for i in sorted([int(i) for i in DATA])]
    nrow = np.ceil(len(run_list) / ncol)

    for idx, run in enumerate(run_list, start=1):
        ax = fig.add_subplot(nrow, ncol, idx)
        for t in terms:
            ax.plot(DATA[run]['time'], DATA[run]['k%s%s' % (drx, t)], alpha=0.9)
        ax.set_title('%s (%s)' % (run, drx))
        ax.set_xlabel(xlabel)
        ax.set_ylabel(ylabel)
        ax.set_ylim(ylim)
        ax.set_xlim(xlim)
        if idx == 1:
            ax.legend(['k%s%s' % (drx, t) for t in terms], loc=2, frameon=False)
    if save is not None:
        plt.savefig(save, transparent=True, bbox_inches='tight', dpi=dpi)


def plot_k_avg(DATA, terms=['', '_bond', '_angle'],
                   figsize=(15, 3), dpi=300, hspace=0.3, wspace=0.2,
                   xlabel='Time (ps)', ylabel='k (W / mK)',
                   ylim=(None, None), xlim=(None, None), save=None):
    """
    Plot k average for breathing mof.
    terms : k contribution by total, bonds, angles
    """
    fig = plt.figure(figsize=figsize, dpi=dpi)
    fig.subplots_adjust(hspace=hspace, wspace=wspace)
    for plt_idx, drx in enumerate(['x', 'y', 'z'], start=1):
        AVG_DATA = {}
        for t in terms:
            AVG_DATA['k%s%s' % (drx, t)] = []
        run_list = [str(i) for i in sorted([int(i) for i in DATA])]
        for idx, run in enumerate(run_list, start=1):
            for trm in AVG_DATA:
                AVG_DATA[trm].append(DATA[run][trm])
        for trm in AVG_DATA:
            AVG_DATA[trm] = np.average(AVG_DATA[trm], axis=0)

        ax = fig.add_subplot(1, 3, plt_idx)
        legend = []
        for trm in AVG_DATA:
            ax.plot(DATA['1']['time'], AVG_DATA[trm])
            legend.append(trm)
        ax.legend(legend, loc=2, frameon=False)
        ax.set_xlabel(xlabel)
        ax.set_ylabel(ylabel)
        ax.set_ylim(ylim)
        ax.set_xlim(xlim)
    if save is not None:
        plt.savefig(save, transparent=True, bbox_inches='tight', dpi=dpi)

def plot_volume(DATA, V_IDEAL=80*80*80, time_conv=1/1000,
                figsize=(20, 5), dpi=300, hspace=0.42, wspace=0.3, ncol=5,
                xlabel='Time (ps) | NPT', ylabel='Box volume (A3)',
                ylim=(None, None), xlim=(None, None), save=None):
    """
    Plot NPT volume.
    V_IDEAL -> ideal simulation box volume.
    time_conv -> Time conversion from timestep to ps.
    """
    fig = plt.figure(figsize=figsize, dpi=dpi)
    fig.subplots_adjust(hspace=hspace, wspace=wspace)
    run_list = [str(i) for i in sorted([int(i) for i in DATA])]
    nrow = np.ceil(len(run_list) / ncol)

    for idx, run in enumerate(run_list, start=1):
        ax = fig.add_subplot(nrow, ncol, idx)
        t, v, v_avg = DATA[run]['v_time'], DATA[run]['v'], DATA[run]['v_avg']
        t = [i * time_conv for i in t]
        ax.plot(t, v)
        ax.plot([t[0], t[-1]], [v_avg] * 2, 'k--')
        ax.plot([t[0], t[-1]], [V_IDEAL] * 2, 'r--')
        ax.text((t[-1] - t[0]) * 0.1, min(v) * 1.001, '$V_{avg}$: %.1f | %.2f %%' % (v_avg, v_avg / V_IDEAL * 100))
        ax.ticklabel_format(style='sci', axis='y', scilimits=(0,0))
        ax.set_xlabel(xlabel)
        ax.set_ylabel(ylabel)
        ax.set_ylim(ylim)
        ax.set_xlim(xlim)
        ax.set_title(run)
    if save is not None:
        plt.savefig(save, transparent=True, bbox_inches='tight', dpi=dpi)

def plot_thermo(THERMO, variable='temp', xlabel='Time (ps)', ylabel='',
                figsize=(20, 5), dpi=300, hspace=0.45, wspace=0.2, ncol=5,
                legend_ncol=2, legend_loc=1, add_line=None,
                ylim=(None, None), xlim=(None, None), save=None):
    """
    Plot thermo data for breathing mof.
    variable : variable to plot
    """
    fig = plt.figure(figsize=figsize, dpi=dpi)
    fig.subplots_adjust(hspace=hspace, wspace=wspace)
    run_list = [str(i) for i in sorted([int(i) for i in THERMO])]
    nrow = np.ceil(len(run_list) / ncol)
    fixes = list(THERMO[run_list[0]].keys())
    legend = list(THERMO[run_list[0]].keys())
    for idx, run in enumerate(run_list, start=1):
        ax = fig.add_subplot(nrow, ncol, idx)
        for fix in fixes:
            ax.plot(THERMO[run][fix]['time'], THERMO[run][fix][variable])
        if add_line is not None:
            ax.plot(ax.get_xlim(), [add_line, add_line], 'k--')
            legend += [str(round(add_line, 1))]
        ax.set_title('%s (%s)' % (run, variable))
        ax.set_xlabel(xlabel)
        ax.set_ylabel(ylabel)
        ax.set_ylim(ylim)
        ax.set_xlim(xlim)
        if idx == 1:
            ax.legend(legend, loc=legend_loc, ncol=legend_ncol, frameon=False)
    if save is not None:
        plt.savefig(save, transparent=True, bbox_inches='tight', dpi=dpi)


def plot_kest(k_data, time, kest=None, legend=[], title='',
              figsize=(5, 3), dpi=300, hspace=0.45, wspace=0.2,
              xlabel='Time (ps)', ylabel='k (W / mK)',
              ylim=(None, None), xlim=(None, None), save=None):
    """
    Plot k for breathing mof.
    k_data : list
        List of thermal conductivity results with same time data.
    time : list
        Time data.
    kest : dict or None
        {'k': list, 't': list, 'kest': float}
    legend : list
        List of labels for k data.
    terms : k contribution by total, bonds, angles
    """
    fig = plt.figure(figsize=figsize, dpi=dpi)
    fig.subplots_adjust(hspace=hspace, wspace=wspace)
    ax = fig.add_subplot(1, 1, 1)
    for idx, k in enumerate(k_data, start=1):
        ax.plot(time, k, alpha=0.9)
        ax.set_title(title)
        ax.set_xlabel(xlabel)
        ax.set_ylabel(ylabel)
        ax.set_ylim(ylim)
        ax.set_xlim(xlim)
    if kest is not None:
        ax.plot(kest['t'], kest['k'], c='r')
        ax.text(sum(kest['t']) / len(kest['t']), sum(kest['t']) / len(kest['t']), round(kest['kest'], 2))
        legend.append('k_est')
    ax.legend(legend, loc=2, frameon=False)
    if save is not None:
        plt.savefig(save, transparent=True, bbox_inches='tight', dpi=dpi)
