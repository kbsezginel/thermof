# Date: February 2017
# Author: Kutay B. Sezginel
"""
Visualize Lammps output files of thermal conductivity measurements
"""
import os
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from thermof.read import average_k, estimate_k
from thermof.parameters import plot_parameters


def plot_thermal_conductivity(plot_data, parameters=plot_parameters['k']):
    """Plot thermal conductivity vs time

    Args:
        - plot_data (dict): Plot data as dictionary with x, y, legend keys
        - parameters (dict): Plot parameters (see parameters.py)

    Returns:
        - None
    """
    plt.figure(figsize=parameters['size'], dpi=parameters['dpi'])
    legend = plot_data['legend'].copy()
    if parameters['cmap'] is not None:
        colormap = matplotlib.cm.get_cmap(parameters['cmap'])
    lim = parameters['limit']
    for i, y in enumerate(plot_data['y'], start=1):
        if parameters['cmap'] is not None:
            color = colormap(i / len(plot_data['y']))
            plt.plot(plot_data['x'][lim[0]:lim[1]], y[lim[0]:lim[1]], c=color, lw=parameters['lw'])
        else:
            plt.plot(plot_data['x'][lim[0]:lim[1]], y[lim[0]:lim[1]], lw=parameters['lw'])
    if parameters['avg']:
        y_avg = average_k(plot_data['y'])
        plt.plot(plot_data['x'][lim[0]:lim[1]], y_avg[lim[0]:lim[1]], '--k', lw=parameters['lw'])
        legend.append('Average')
    if parameters['title'] is not None:
        plt.title(parameters['title'], fontsize=parameters['fontsize'] + 4)
    plt.xticks(fontsize=parameters['fontsize'])
    plt.yticks(fontsize=parameters['fontsize'])
    plt.ylabel(parameters['ylabel'], fontsize=parameters['fontsize'] + 2)
    plt.xlabel(parameters['xlabel'], fontsize=parameters['fontsize'] + 2)
    plt.legend(legend, loc=parameters['legendloc'], ncol=parameters['ncol'], fontsize=parameters['fontsize'])
    if parameters['save'] is not None:
        plt.savefig(parameters['save'], dpi=parameters['dpi'], transparent=True, bbox_inches='tight')
    if parameters['show']:
        plt.show()


def plot_framework_distance(dist_data, parameters=plot_parameters['f_dist']):
    """Plots distance histogram

    Args:
        - hist_data (dict): Histogram data as dictionary with x, y, legend keys
        - parameters (dict): Plot parameters (see parameters.py)

    Returns:
        - None (shows the plot)
    """
    fig = plt.figure(figsize=parameters['size'], dpi=parameters['dpi'])
    fig.subplots_adjust(hspace=parameters['space'][0], wspace=parameters['space'][1])

    lim = (1 - parameters['grid_size'] / parameters['grid_limit']) / 2
    dx = (1 - 2 * lim) * 10
    dy = (1 - 2 * lim) * 10
    n_bins = int(parameters['grid_limit'] / parameters['bin_size'])

    for i, reldist in enumerate(dist_data, start=1):
        heatmap, xedges, yedges = np.histogram2d(reldist['x'], reldist['y'], bins=n_bins)
        extent = [xedges[0], xedges[-1], yedges[0], yedges[-1]]
        H = heatmap.T

        ax = fig.add_subplot(parameters['subplot'][0], parameters['subplot'][1], i, title=reldist['title'])
        ax.set_xlim(0 + lim, 1 - lim)
        ax.set_ylim(0 + lim, 1 - lim)
        if not parameters['ticks']:
            ax.set_xticklabels([])
            ax.set_yticklabels([])

        cmap = plt.get_cmap(parameters['cmap'])
        cmap.set_under(color='white')

        # Show histogram
        plt.imshow(H, interpolation='nearest', extent=extent, cmap=cmap,
                   vmin=parameters['vmin'], vmax=parameters['vmax'])

    if parameters['cbar'] is not None:
        cbar_ax = fig.add_axes(parameters['cbar'])
        plt.colorbar(cax=cbar_ax)
    if parameters['save'] is not None:
        plt.savefig(parameters['save'], dpi=parameters['dpi'], transparent=True, bbox_inches='tight')
    if parameters['show']:
        plt.show()


def plot_thermo(thermo, parameters):
    """Plots thermo data for single run

    Args:
        - thermo_data (dict): Thermo data as read by read_thermo
        - parameters (dict): Thermo parameters (see parameters.py)

    Returns:
        - None (shows the plot)
    """
    if parameters['fix'] is None:
        parameters['fix'] = list(thermo.keys())
    if parameters['variable'] is None:
        parameters['variable'] = list(thermo[parameters['fix'][0]].keys())

    n_var = len(parameters['variable'])
    n_cols = parameters['n_columns']
    n_rows = int(np.ceil(n_var / n_cols))
    if parameters['size'] is None:
        parameters['size'] = [n_cols * 4 + 2, n_rows * 3]
    fig = plt.figure(figsize=parameters['size'], dpi=parameters['dpi'])
    fig.subplots_adjust(hspace=parameters['subplots_adjust'][0], wspace=parameters['subplots_adjust'][1])

    for i, y_axis in enumerate(parameters['variable'], start=1):
        ax = fig.add_subplot(n_rows, n_cols, i)
        for fix in parameters['fix']:
            if fix in parameters['colors']:
                plt.plot(thermo[fix]['step'], thermo[fix][y_axis], c=parameters['colors'][fix])
            else:
                plt.plot(thermo[fix]['step'], thermo[fix][y_axis])
            plt.ticklabel_format(style='sci', axis='both', scilimits=parameters['scilimits'], fontsize=parameters['fontsize'])
            plt.tick_params(axis='both', labelsize=parameters['fontsize'])
            plt.ylabel(y_axis, fontsize=parameters['fontsize'] + 2)
            plt.xlabel(parameters['xlabel'], fontsize=parameters['fontsize'] + 2)
    if parameters['title'] is not None:
        plt.suptitle(parameters['title'], fontsize=parameters['fontsize'] + 4)
    if parameters['legend'] is not None:
        plt.legend(parameters['fix'], frameon=False)
    if parameters['save'] is not None:
        plt.savefig(parameters['save'], dpi=parameters['dpi'], transparent=True, bbox_inches='tight')
    if parameters['show']:
        plt.show()


def subplot_thermal_conductivity(plot_data, parameters=plot_parameters['k_sub']):
    """Generate subplots of thermal conductivity

    Args:
        - plot_data (dict): Plot data as dictionary with x, y, legend keys
        - parameters (dict): Subplot parameters (see parameters.py)

    Returns:
        - None (shows the plot)
    """
    fig = plt.figure(figsize=parameters['size'], dpi=parameters['dpi'])
    fig.subplots_adjust(hspace=parameters['subplots_adjust'][0], wspace=parameters['subplots_adjust'][1])
    lim = parameters['limit']
    for i, pd in enumerate(plot_data['y'], start=1):
        ax = fig.add_subplot(parameters['subplot'][0], parameters['subplot'][1], i)
        plt.plot(plot_data['x'][lim[0]:lim[1]], pd[lim[0]:lim[1]], lw=parameters['lw'])
        if parameters['ylim'] is not None:
            plt.ylim(parameters['ylim'])
        plt.title(plot_data['legend'][i - 1], fontsize=parameters['fontsize'] + 4)
        if parameters['k_est']:
            kt = estimate_k(pd, plot_data['x'], t0=parameters['k_est_t0'], t1=parameters['k_est_t1'])
            sta, end = parameters['k_est_t0'] * 200, parameters['k_est_t1'] * 200
            plt.plot(plot_data['x'][sta:end], pd[sta:end], parameters['k_est_color'], lw=parameters['lw'])
            plt.text(parameters['k_est_loc'][0], parameters['k_est_loc'][1], 'k: %.3f W/m.K' % kt,
                     color=parameters['k_est_color'], bbox=dict(facecolor='white', alpha=0.7),
                     fontsize=parameters['fontsize'] + 2)
        plt.xticks(fontsize=parameters['fontsize'])
        plt.yticks(fontsize=parameters['fontsize'])
        plt.ylabel(parameters['ylabel'], fontsize=parameters['fontsize'] + 2)
        plt.xlabel(parameters['xlabel'], fontsize=parameters['fontsize'] + 2)
    if parameters['save'] is not None:
        plt.savefig(parameters['save'], dpi=parameters['dpi'], transparent=True, bbox_inches='tight')
    if parameters['show']:
        plt.show()
