"""
LAMMPS helper functions.
"""

def change_input_variables(source_input, dest_input, variables):
    """ Change LAMMPS input variables
    variables : dict {'var_name': value}"""
    with open(source_input, 'r') as inp_src:
        input_lines = inp_src.readlines()
    var_names = list(variables.keys())
    for i, line in enumerate(input_lines):
        for v in var_names:
            if '%s equal' % v in line:
                input_lines[i] = 'variable        %s equal %s\n' % (v, str(variables[v]))
    with open(dest_input, 'w') as inp_dest:
        for line in input_lines:
            inp_dest.write(line)
    return None


def change_job_name(source_input, dest_input, job_name=None):
    """ Change job name for Lammps slurm submission """
    with open(source_input, 'r') as inp_src:
        input_lines = inp_src.readlines()
    for i, line in enumerate(input_lines):
        if '--job-name' in line:
            input_lines[i] = '#SBATCH --job-name=%s\n' % job_name
    with open(dest_input, 'w') as inp_dest:
        for line in input_lines:
            inp_dest.write(line)
    return None

def check_sim_finished(outfile):
    with open(outfile, 'r') as f:
        lines = f.readlines()
    fin, time = False, None
    if len(lines) > 0:
        if 'Total wall time' in lines[-1]:
            fin, time = True, lines[-1].split()[3]
    return fin, time
