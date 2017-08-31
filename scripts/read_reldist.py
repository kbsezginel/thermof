"""
Reads relative distance btw frameworks for a list of trials and saves results to a yaml file
"""
import os
import yaml
from thermof.parameters import plot_parameters
from thermof.read import read_framework_distance

# --------------------------------------------------------------------------------------------------
main = ''
results_file = '%s-reldist-results.yaml' % os.path.basename(main)
run_list_file = '%s-run-list.yaml' % os.path.basename(main)
# --------------------------------------------------------------------------------------------------

run_list = [os.path.join(main, i, 'Run1') for i in os.listdir(main) if os.path.isdir(os.path.join(main, i))]
dist_data = read_framework_distance(run_list, plot_parameters['f_dist'])

with open(results_file, 'w') as rfile:
    yaml.dump(dist_data, rfile)

with open(run_list_file, 'w') as rlfile:
    yaml.dump(run_list, rlfile)
