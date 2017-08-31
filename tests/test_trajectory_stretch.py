"""
Tests trajectory stretch method.
"""
import os
import numpy as np
from thermof import Trajectory

mof_trial_dir = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'ideal-mof-trial')
ipmof_trial_dir = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'ip-mof-trial')


def test_trajectory_stretch_method():
    """ Test trajectory class stretch method for non-interpenetrated ideal MOF """
    traj = Trajectory(read=os.path.join(mof_trial_dir, 'Run1', 'traj.xyz'))
    xyz_stretch1 = traj.stretch(1)
    assert len(traj.xyz) == len(xyz_stretch1)
    xyz_stretch3 = traj.stretch(3)
    assert len(traj.xyz[0]) == len(xyz_stretch3[0])
    assert len(traj.xyz[-1]) == len(xyz_stretch3[-1])
    assert len(traj.xyz) * 3 == len(xyz_stretch3)


def test_trajectory_stretch_method_with_write(tmpdir):
    """ Test trajectory class stretch method for non-interpenetrated ideal MOF """
    ref_traj = os.path.join(mof_trial_dir, 'Run1', 'traj.xyz')
    traj = Trajectory(read=ref_traj)
    with open(ref_traj, 'r') as rt:
        ref_traj_lines = rt.readlines()
    temp_file = tmpdir.join('traj-temp.xyz')
    xyz_stretch = traj.stretch(2, temp_file.strpath)
    with open(temp_file.strpath, 'r') as tf:
        tmp_traj_lines = tf.readlines()
    assert len(tmp_traj_lines) == len(ref_traj_lines) * 2
