"""
Functions to help initialize Lammps simulations
"""
import os


def read_lines(file_name):
    """ Read lines from given file and return as list """
    with open(file_name, 'r') as fobj:
        lines = fobj.readlines()
    return lines


def write_lines(file_name, lines):
    """ Write given list of lines to given file """
    if os.path.exists(file_name):
        os.remove(file_name)
    with open(file_name, 'w') as fobj:
        for line in lines:
            fobj.write(line)
