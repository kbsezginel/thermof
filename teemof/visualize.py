# Date: February 2017
# Author: Kutay B. Sezginel
"""
Visualize Lammps output files of thermal conductivity measurements
"""
import os
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from teemof.read import average_k
from teemof.parameters import plot_parameters


def plot_thermal_conductivity(plot_data, parameters=plot_parameters['k']):
    """Plot thermal conductivity vs time

    Args:
        - plot_data (dict): Plot data as dictionary with x, y, legend keys
        - parameters (dict): Plot parameters (see parameters.py)

    Returns:
        - None
    """
    plt.figure(figsize=parameters['size'], dpi=parameters['dpi'])
    if parameters['cmap'] is not None:
        colormap = matplotlib.cm.get_cmap(parameters['cmap'])
    lim = parameters['limit']
    for i, y in enumerate(plot_data['y'], start=1):
        if parameters['cmap'] is not None:
            color = colormap(i / len(plot_data['y']))
            plt.plot(plot_data['x'][lim[0]:lim[1]], y[lim[0]:lim[1]], c=color)
        else:
            plt.plot(plot_data['x'][lim[0]:lim[1]], y[lim[0]:lim[1]])
    if parameters['avg']:
        y_avg = average_k(plot_data['y'])
        plt.plot(plot_data['x'][lim[0]:lim[1]], y_avg[lim[0]:lim[1]], '--k', linewidth=2)
        plot_data['legend'].append('Average')
    if parameters['title'] is not None:
        plt.title(parameters['title'], fontsize=parameters['fontsize'] + 4)
    plt.xticks(fontsize=parameters['fontsize'])
    plt.yticks(fontsize=parameters['fontsize'])
    plt.ylabel(parameters['ylabel'], fontsize=parameters['fontsize'] + 2)
    plt.xlabel(parameters['xlabel'], fontsize=parameters['fontsize'] + 2)
    plt.legend(plot_data['legend'], loc=(1.05, 0), ncol=parameters['ncol'], fontsize=parameters['fontsize'])
    if parameters['save'] is not None:
        plt.savefig(parameters['save'], dpi=parameters['dpi'], transparent=True, bbox_inches='tight')
    plt.show()


def plot_runs(runs_data, time, runs_id, limit=(0, 2000), title=None, size=(20, 10), fontsize=14, dpi=300, avg=True, cmap=None, save=None, ncol=1):
    """ Plot kt vs time for a list of runs """
    plt.figure(figsize=size, dpi=dpi)
    lgnd = runs_id
    if cmap is not None:
        colormap = matplotlib.cm.get_cmap(cmap)
    for i, rd in enumerate(runs_data, start=1):
        if cmap is not None:
            color = colormap(i / len(runs_data))
            plt.plot(time[limit[0]:limit[1]], rd[limit[0]:limit[1]], c=color)
        else:
            plt.plot(time[limit[0]:limit[1]], rd[limit[0]:limit[1]])

    if avg:
        runs_avg_kt = average_k(runs_data)
        plt.plot(time[limit[0]:limit[1]], runs_avg_kt[limit[0]:limit[1]], '--k', linewidth=2)
        lgnd.append('Average')
    if title is not None:
        plt.title(title, fontsize=fontsize + 4)
    plt.xticks(fontsize=fontsize)
    plt.yticks(fontsize=fontsize)
    plt.ylabel('kt', fontsize=fontsize + 2)
    plt.xlabel('Time', fontsize=fontsize + 2)
    plt.legend(lgnd, loc=(1.05, 0), ncol=ncol, fontsize=fontsize)
    if save is not None:
        plt.savefig(save, dpi=dpi, transparent=True, bbox_inches='tight')
    plt.show()


def plot_directions(runs_data, time, runs_id, limit=(0, 2000), title=None, size=(20, 10), fontsize=14, dpi=300, avg=True, save=None, ncol=1):
    """ Plot multiple run data according to directions """
    plt.figure(figsize=size, dpi=dpi)
    dirs = (['X', 'Y', 'Z'])
    colors = ['r', 'g', 'b']
    lgnd = []
    for direction in range(3):
        clr = colors[direction]
        drc = dirs[direction]
        for i in range(int(len(runs_data) / 3)):
            kt = runs_data[direction][limit[0]:limit[1]]
            plt.plot(time[limit[0]:limit[1]], kt, clr)
            direction += 3
            lgnd.append('%s-%s' % (drc, runs_id[i]))

    if avg:
        runs_avg_kt = average_k(runs_data)
        plt.plot(time[limit[0]:limit[1]], runs_avg_kt[limit[0]:limit[1]], '--k', linewidth=2)
        lgnd.append('Average')

    if title is not None:
        plt.title(title, fontsize=fontsize + 4)
    plt.xticks(fontsize=fontsize)
    plt.yticks(fontsize=fontsize)
    plt.ylabel('kt', fontsize=fontsize + 2)
    plt.xlabel('Time', fontsize=fontsize + 2)
    plt.legend(lgnd, loc=(1.05, 0), ncol=ncol, fontsize=fontsize)
    if save is not None:
        plt.savefig(save, dpi=dpi, transparent=True, bbox_inches='tight')
    plt.show()


def plot_distance_hist(hist_data, subplot=(2, 5), size=(14, 6), space=(0.2, 0.1), grid_size=10,
                       bin_size=1, vmax=25, vmin=0.01, colormap='YlOrRd', grid_limit=10,
                       ticks=False, cbar=[0.92, 0.135, 0.02, 0.755], save=None, dpi=500,
                       selections=None):
    """ Plots distance histogram for each run of a given trial """
    fig = plt.figure(figsize=size)
    fig.subplots_adjust(hspace=space[0], wspace=space[1])

    lim = (1 - grid_size / grid_limit) / 2
    dx = (1 - 2 * lim) * 10
    dy = (1 - 2 * lim) * 10
    n_bins = int(grid_limit / bin_size)

    # Selecting part of the data by the third element which corresponds to title
    if selections is not None:
        new_dist_data = []
        for d in hist_data:
            if d[3] in selections:
                new_dist_data.append(d)
        hist_data = sorted(new_dist_data, key=lambda x: x[3])

    for i, trial in enumerate(hist_data, start=1):
        x, y, z, title, sort_par = trial
        heatmap, xedges, yedges = np.histogram2d(x, y, bins=n_bins)
        extent = [xedges[0], xedges[-1], yedges[0], yedges[-1]]
        H = heatmap.T

        ax = fig.add_subplot(subplot[0], subplot[1], i, title=title)
        ax.set_xlim(0 + lim, 1 - lim)
        ax.set_ylim(0 + lim, 1 - lim)
        if not ticks:
            ax.set_xticklabels([])
            ax.set_yticklabels([])

        cmap = plt.get_cmap(colormap)
        cmap.set_under(color='white')

        # Show histogram
        plt.imshow(H, interpolation='nearest', extent=extent, cmap=cmap, vmin=vmin, vmax=vmax)

    if cbar is not None:
        cbar_ax = fig.add_axes(cbar)
        plt.colorbar(cax=cbar_ax)
    if save is not None:
        plt.savefig(save, dpi=dpi, transparent=True, bbox_inches='tight')
    plt.show()
