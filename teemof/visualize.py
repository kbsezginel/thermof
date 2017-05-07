# Visualize Lammps output files of thermal conductivity measurements
# Date: Februay 2017
# Author: Kutay B. Sezginel
import matplotlib
import matplotlib.pyplot as plt
from teemof.read import avg_kt


def plot_runs(runs_data, time, runs_id, limit=2000, title=None, size=(20, 10), fontsize=14, dpi=300, avg=True, cmap=None, save=None):
    """ Plot kt vs time for a list of runs """
    plt.figure(figsize=size, dpi=dpi)
    lgnd = runs_id
    if cmap is not None:
        colormap = matplotlib.cm.get_cmap(cmap)
    for i, rd in enumerate(runs_data, start=1):
        if cmap is not None:
            color = colormap(i / len(runs_data))
            plt.plot(time[:limit], rd[:limit], c=color)
        else:
            plt.plot(time[:limit], rd[:limit])

    if avg:
        runs_avg_kt = avg_kt(runs_data)
        plt.plot(time[:limit], runs_avg_kt[:limit], '--k', linewidth=2)
        lgnd.append('Average')
    if title is not None:
        plt.title(title, fontsize=fontsize + 4)
    plt.xticks(fontsize=fontsize)
    plt.yticks(fontsize=fontsize)
    plt.ylabel('kt', fontsize=fontsize + 2)
    plt.xlabel('Time', fontsize=fontsize + 2)
    plt.legend(lgnd, loc=(1.05, 0), fontsize=fontsize)
    if save is not None:
        plt.savefig(save, dpi=dpi, transparent=True, bbox_inches='tight')
    plt.show()


def plot_directions(runs_data, time, runs_id, limit=2000, title=None, size=(20, 10), fontsize=14, dpi=300, avg=True, save=None):
    """ Plot multiple run data according to directions """
    plt.figure(figsize=size, dpi=dpi)
    dirs = (['X', 'Y', 'Z'])
    colors = ['r', 'g', 'b']
    lgnd = []
    for direction in range(3):
        clr = colors[direction]
        drc = dirs[direction]
        for i in range(int(len(runs_data) / 3)):
            kt = runs_data[direction][:limit]
            plt.plot(time[:limit], kt, clr)
            direction += 3
            lgnd.append('%s-%s' % (drc, runs_id[i]))

    if avg:
        runs_avg_kt = avg_kt(runs_data)
        plt.plot(time[:limit], runs_avg_kt[:limit], '--k', linewidth=2)
        lgnd.append('Average')

    if title is not None:
        plt.title(title, fontsize=fontsize + 4)
    plt.xticks(fontsize=fontsize)
    plt.yticks(fontsize=fontsize)
    plt.ylabel('kt', fontsize=fontsize + 2)
    plt.xlabel('Time', fontsize=fontsize + 2)
    plt.legend(lgnd, loc=(1.05, 0), fontsize=fontsize)
    if save is not None:
        plt.savefig(save, dpi=dpi, transparent=True, bbox_inches='tight')
    plt.show()
