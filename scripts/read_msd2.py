"""
Reads mean squared displacement for a list of trials and saves results to a yaml file
"""
import os
import yaml
from thermof.trajectory import Trajectory
from thermof.read import read_run_info
# --------------------------------------------------------------------------------------------------
main = ''
box1_atoms = [234, 298, 226, 290, 233, 297, 225, 289]
box2_atoms = [3818, 3882, 3810, 3874, 3817, 3881, 3809, 3873]
ipbox_atoms = box1_atoms + box2_atoms
results_file = '%s-MSD-results.yaml' % os.path.basename(main)


def msd(coordinates, unit_cell, reference_frame=0):
    n_frames, n_atoms = np.shape(coordinates)[:2]
    ref_coordinates = coordinates[reference_frame]
    displacement = np.zeros((n_frames, 3))
    for frame_idx, frame in enumerate(coordinates):
        d_tot = np.zeros((3, ))
        for atom_idx, (atom, ref_atom) in enumerate(zip(frame, ref_coordinates)):
            d = np.zeros((3, ))
            for i in range(3):
                d[i] = atom[i] - ref_atom[i]
                if d[i] > unit_cell[i] * 0.5:
                    d[i] = d[i] - unit_cell[i]
                elif d[i] <= -unit_cell[i] * 0.5:
                    d[i] = d[i] + unit_cell[i]
            d_tot += d ** 2
        displacement[frame_idx] = d_tot / n_atoms
    return np.sum(np.average(displacement, axis=0))


# --------------------------------------------------------------------------------------------------
trial_list = [os.path.join(main, i) for i in os.listdir(main) if os.path.isdir(os.path.join(main, i))]
results = dict(msd1=[], msd2=[], msd=[], sigma=[], epsilon=[], trial=[])

for trial_index, trial in enumerate(trial_list, start=1):
    trial_name = os.path.basename(trial)
    print('\n%i / %i | %s #################################' % (trial_index, len(trial_list), trial_name), flush=True)
    if trial_name not in ['S6.00-E0.80', 'S6.00-E1.00']:
        run_list = [os.path.join(trial, i) for i in os.listdir(trial) if os.path.isdir(os.path.join(trial, i))]
        msd1_avg, msd2_avg, msd_avg = [], [], []
        for run in run_list:
            traj_file = os.path.join(run, 'traj.xyz')
            traj = Trajectory(read=traj_file)

            traj_box1 = traj.subdivide(atoms=box1_atoms)
            msd1 = msd(traj_box1.coordinates, [80, 80, 80])
            msd1_avg.append(msd1)

            traj_box2 = traj.subdivide(atoms=box2_atoms)
            msd2 = msd(traj_box2.coordinates, [80, 80, 80])
            msd2_avg.append(msd1)

            traj_ipbox = traj.subdivide(atoms=ipbox_atoms)
            msdip = msd(traj_ipbox.coordinates, [80, 80, 80])
            msd_avg.append(msdip)

        results['msd1'].append(sum(msd1_avg) / len(msd1_avg))
        results['msd2'].append(sum(msd2_avg) / len(msd2_avg))
        results['msd'].append(sum(msd_avg) / len(msd_avg))
        print('MSD1: %.2f (%i) | MSD2: %.2f (%i) MSD: %.2f (%i)'
              % (results['msd1'][-1], len(msd1_avg), results['msd2'][-1], len(msd2_avg), results['msd'][-1], len(msd_avg)))
    else:
        results['msd1'].append(None)
        results['msd2'].append(None)
        results['msd'].append(None)

    run_info = read_run_info(run)
    results['sigma'].append(run_info['sigma'])
    results['epsilon'].append(run_info['epsilon'])
    results['trial'].append(os.path.basename(trial))

with open(results_file, 'w') as rfile:
    yaml.dump(results, rfile)
