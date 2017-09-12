"""
Tests trajectory stretch method.
"""
import os
import numpy as np
from thermof import Trajectory

mof_trial_dir = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'ideal-mof-trial')
ipmof_trial_dir = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'ip-mof-trial')


def test_trajectory_subdivide_method_returns_same_trajectory_without_kwargs():
    """ Test trajectory class stretch method for non-interpenetrated ideal MOF """
    traj = Trajectory(read=os.path.join(mof_trial_dir, 'Run1', 'traj.xyz'))
    div_traj = traj.subdivide()
    assert traj == div_traj
