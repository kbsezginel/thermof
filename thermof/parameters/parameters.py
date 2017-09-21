"""
Parameters for reading and plotting thermal flux
"""


class Parameters:
    def __init__(self, par_dict=None):
        if par_dict is not None:
            self.set(par_dict)

    def __repr__(self):
        return "<Parameter set: %i parameters>" % (len(vars(self).keys()))

    def set(self, par_dict):
        """ Set parameters from given dictionary """
        for par in par_dict.keys():
            setattr(self, par, par_dict[par])

    def show(self):
        """ Show parameters and values """
        for v in sorted(vars(self)):
            print('%-25s: %s' % (v, getattr(self, v)))
