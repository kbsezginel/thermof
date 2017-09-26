"""
Parameters for reading and plotting thermal flux
"""
import os
import yaml
import pprint
from copy import deepcopy
from .default import default_parameters


class Parameters:
    def __init__(self, par_set=None):
        if par_set is not None:
            self.set(par_set)
        else:
            self.set(default_parameters.copy())

    def __repr__(self):
        return "<Parameter set: %i parameters>" % (len(vars(self).keys()))

    def set(self, par_set):
        """ Set parameters from given dictionary """
        for par in par_set:
            setattr(self, par, deepcopy(par_set[par]))

    def show(self, par=None):
        """ Show parameters and values """
        if par is None:
            for p in sorted(vars(self)):
                print('\n%-7s %s' % (p, '-' * 20))
                pprint.pprint(getattr(self, p))
        else:
            for v in sorted(getattr(self, par)):
                print('%-25s: %s' % (v, getattr(self, par)[v]))

    def save(self, parameters=['thermof', 'lammps', 'job'], savedir=None, verbose=True):
        """ Save parameters as dictionary """
        simpar = {par: self.__dict__[par] for par in parameters}
        if savedir is None:
            savedir = os.getcwd()
        par_file = os.path.join(savedir, 'simpar.yaml')
        with open(par_file, 'w') as par:
            yaml.dump(simpar, par, default_flow_style=False)
        print('Simulation parameters saved -> %s' % par_file) if verbose else None
