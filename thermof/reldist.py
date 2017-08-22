# Date: February 2017
# Author: Patrick Asinger and Kutay B. Sezginel
"""
Calculate relative distance between interpenetrated frameworks
"""
import os
import math


def reldist(traj_path, end=300000):
    segmentation = []
    x_axis_data = []
    MOF1_pt1_coords = []
    MOF1_pt2_coords = []
    MOF1_pt3_coords = []
    MOF1_pt4_coords = []
    MOF1_pt5_coords = []
    MOF1_pt6_coords = []
    MOF1_pt7_coords = []
    MOF1_pt8_coords = []
    MOF2_pt1_coords = []
    MOF2_pt2_coords = []
    MOF2_pt3_coords = []
    MOF2_pt4_coords = []
    MOF2_pt5_coords = []
    MOF2_pt6_coords = []
    MOF2_pt7_coords = []
    MOF2_pt8_coords = []
    equil_end_timestep = end
    equil_end_linenum = []
    with open(traj_path, 'r') as t:
        for l, line in enumerate(t):
            if '30 30 30' in line:
                MOF1_pt1_initial = l
            if '40 30 30' in line:
                MOF1_pt2_initial = l
            if '30 40 30' in line:
                MOF1_pt3_initial = l
            if '30 30 40' in line:
                MOF1_pt4_initial = l
            if '40 40 30' in line:
                MOF1_pt5_initial = l
            if '40 30 40' in line:
                MOF1_pt6_initial = l
            if '30 40 40' in line:
                MOF1_pt7_initial = l
            if '40 40 40' in line:
                MOF1_pt8_initial = l
            if '35 35 35' in line:
                MOF2_pt1_initial = l

            if 'Timestep' in line:
                segmentation.append(l)
                x_axis_data.append(line.split()[2])
                if float(line.split()[2]) > equil_end_timestep:
                    equil_end_linenum.append(l)
    with open(traj_path, 'r') as t:
        data = t.readlines()

    for i in segmentation:
        MOF1_pt1_coords.append(data[i+MOF1_pt1_initial-1].split()[1:])
        MOF1_pt2_coords.append(data[i+MOF1_pt2_initial-1].split()[1:])
        MOF1_pt3_coords.append(data[i+MOF1_pt3_initial-1].split()[1:])
        MOF1_pt4_coords.append(data[i+MOF1_pt4_initial-1].split()[1:])
        MOF1_pt5_coords.append(data[i+MOF1_pt5_initial-1].split()[1:])
        MOF1_pt6_coords.append(data[i+MOF1_pt6_initial-1].split()[1:])
        MOF1_pt7_coords.append(data[i+MOF1_pt7_initial-1].split()[1:])
        MOF1_pt8_coords.append(data[i+MOF1_pt8_initial-1].split()[1:])
        MOF2_pt1_coords.append(data[i+MOF2_pt1_initial-1].split()[1:])

    MOF1_xave = []
    MOF1_yave = []
    MOF1_zave = []
    MOF1_center_coords = []
    for i in range(len(MOF1_pt1_coords)):
        MOF1_xave.append((float(MOF1_pt1_coords[i][0]) + float(MOF1_pt2_coords[i][0]) + float(MOF1_pt3_coords[i][0]) + float(MOF1_pt4_coords[i][0]) + float(MOF1_pt5_coords[i][0]) + float(MOF1_pt6_coords[i][0]) + float(MOF1_pt7_coords[i][0]) + float(MOF1_pt8_coords[i][0])) / 8)
        MOF1_yave.append((float(MOF1_pt1_coords[i][1]) + float(MOF1_pt2_coords[i][1]) + float(MOF1_pt3_coords[i][1]) + float(MOF1_pt4_coords[i][1]) + float(MOF1_pt5_coords[i][1]) + float(MOF1_pt6_coords[i][1]) + float(MOF1_pt7_coords[i][1]) + float(MOF1_pt8_coords[i][1])) / 8)
        MOF1_zave.append((float(MOF1_pt1_coords[i][2]) + float(MOF1_pt2_coords[i][2]) + float(MOF1_pt3_coords[i][2]) + float(MOF1_pt4_coords[i][2]) + float(MOF1_pt5_coords[i][2]) + float(MOF1_pt6_coords[i][2]) + float(MOF1_pt7_coords[i][2]) + float(MOF1_pt8_coords[i][2])) / 8)
        MOF1_center_coords.append([MOF1_xave[i], MOF1_yave[i], MOF1_zave[i]])

    distance = []
    after_equil_distance = []
    for i in range(len(MOF1_pt1_coords)):
        distance.append(((float(MOF1_center_coords[i][0]) - float(MOF2_pt1_coords[i][0])) ** 2 +
                         (float(MOF1_center_coords[i][1]) - float(MOF2_pt1_coords[i][1])) ** 2 +
                         (float(MOF1_center_coords[i][2]) - float(MOF2_pt1_coords[i][2])) ** 2) ** 1 / 2)

    MOF_reldist = []
    for i in range(len(MOF1_pt1_coords)):
        MOF_reldist.append([((float(MOF2_pt1_coords[i][0]) - float(MOF1_pt1_coords[i][0])) / (float(MOF1_pt2_coords[i][0]) - float(MOF1_pt1_coords[i][0]))),
                            ((float(MOF2_pt1_coords[i][1]) - float(MOF1_pt1_coords[i][1])) / (float(MOF1_pt3_coords[i][1]) - float(MOF1_pt1_coords[i][1]))),
                            ((float(MOF2_pt1_coords[i][2]) - float(MOF1_pt1_coords[i][2])) / (float(MOF1_pt4_coords[i][2]) - float(MOF1_pt1_coords[i][0])))])
    x_coords = [i[0] for i in MOF_reldist]
    y_coords = [i[1] for i in MOF_reldist]
    z_coords = [i[2] for i in MOF_reldist]

    return x_coords, y_coords, z_coords
