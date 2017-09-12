"""
Tests trajectory stretch method.
"""
import os
import numpy as np
from thermof import Trajectory

mof_trial_dir = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'ideal-mof-trial')
ipmof_trial_dir = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'ip-mof-trial')


def test_trajectory_subdivide_method_returns_same_trajectory_without_kwargs():
    """ Test trajectory class subdivision method for non-interpenetrated ideal MOF with no kwargs """
    traj = Trajectory(read=os.path.join(mof_trial_dir, 'Run1', 'traj.xyz'))
    div_traj = traj.subdivide()
    assert traj == div_traj


def test_trajectory_subdivide_method_example_case():
    """ Test trajectory class subdivision for non-interpenetrated ideal MOF example case """
    traj = Trajectory(read=os.path.join(mof_trial_dir, 'Run1', 'traj.xyz'))
    div_traj = traj.subdivide(atoms=list(range(10, 20)), frames=list(range(5, 10)), dimensions=[1, 2])
    assert (div_traj.n_frames, div_traj.n_atoms, div_traj.n_dimensions) == (5, 10, 2)
    assert div_traj.atoms == [frame[10:20] for frame in traj.atoms[5:10]]
    assert np.allclose(div_traj.coordinates[0][0], traj.coordinates[5][10][1:])
    assert np.allclose(div_traj.coordinates[4][3], traj.coordinates[9][13][1:])
