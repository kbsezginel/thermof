"""
Parameters for reading and plotting thermal flux
"""
import pprint
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
            setattr(self, par, par_set[par].copy())

    def show(self, par=None):
        """ Show parameters and values """
        if par is None:
            for p in sorted(vars(self)):
                print('\n%-7s %s' % (p, '-' * 20))
                pprint.pprint(getattr(self, p))
        else:
            for v in sorted(getattr(self, par)):
                print('%-25s: %s' % (v, getattr(self, par)[v]))
