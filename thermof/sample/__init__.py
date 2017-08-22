"""
Sample input files for predicting thermal conductivity of porous crystals using Lammps
"""
import os


sample_dir = os.path.abspath(os.path.dirname(__file__))
# Lammps input file with thermal flux measured in single direction
single_inp_path = os.path.join(sample_dir, 'in_single.cond.sample')        # Single MOF
# Lammps input file with thermal flux measured in three directions
single_inp3_path = os.path.join(sample_dir, 'in3_single.cond.sample')      # Single MOF
ipmof_inp3_path = os.path.join(sample_dir, 'in3_ipmof.cond.sample')        # Interpenetrated MOF
# Lammps structure files
single_data_path = os.path.join(sample_dir, 'lammps_single.data.sample')   # Single MOF
ipmof_data_path = os.path.join(sample_dir, 'lammps_ipmof.data.sample')     # Interpenetrated MOF
# Job submission file for Frank
qsub_path = os.path.join(sample_dir, 'lammps_qsub.sh.sample')

samples = dict(ideal_mof=dict(inp=single_inp3_path, data=single_data_path, qsub=qsub_path),
               ideal_interpenetrated_mof=dict(inp=ipmof_inp3_path, data=ipmof_data_path, qsub=qsub_path))
