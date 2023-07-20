# Description: This script plots the distribution of angles vs distances for a given object and a given set of atoms.

import numpy as np
import pymol
import matplotlib.pyplot as plt
from scipy.stats import gaussian_kde

def plot_contour(distances, angles):
    distances = np.array(distances)
    angles = np.array(angles)
    xy = np.vstack([distances, angles])
    kde = gaussian_kde(xy)
    z = kde(xy)

    fig, ax = plt.subplots()
    sc = ax.scatter(distances, angles, c=z, s=20, cmap='viridis_r')  # Updated color map to 'viridis' for better readability
    ax.set_xlabel('Distance')
    ax.set_ylabel('Angle')
    ax.set_title('Angle vs. Distance Distribution')  # Added a title to the plot
    fig.colorbar(sc, label='Density')  # Added a label for the colorbar

    # Adding grid lines
    ax.grid(True, linestyle='--', linewidth=0.5, alpha=0.7)

    plt.show()

def angle_vs_dist_distribution(object_name, atom1_angle, atom2_angle, atom3_angle, atom5, atom6):
    angles = []
    distances = []
    for i in range(pymol.cmd.count_states(object_name)):
        pymol.cmd.frame(i+1)
        distance_i = pymol.cmd.get_distance(atom5 + ' & ' + object_name, atom6 + ' & ' + object_name)
        angle = pymol.cmd.get_angle(atom1_angle + ' & ' + object_name, atom2_angle + ' & ' + object_name,
                                    atom3_angle + ' & ' + object_name)
        angles.append(angle)
        distances.append(distance_i)
        print(i)
    
	#save the table dist vs frame in the current directory, using numpy
    np.savetxt('angle_vs_dist_distribution.txt', np.column_stack([distances, angles]), fmt='%f %f', header='Distance Angle')

    plot_contour(distances, angles)
    return distances, angles

print("USAGE: angle_vs_dist_distribution('object_name','atom1_angle', 'atom2_angle', 'atom3_angle', 'atom1_distance', 'atom2_distance')")