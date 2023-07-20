# Description: This script plots the distribution of angles vs distances for a given object and a given set of atoms.

import numpy as np
import pymol
import matplotlib.pyplot as plt
from scipy.stats import gaussian_kde
import multiprocessing as mp

def plot_contour(distances, angles):
    distances = np.array(distances)
    angles = np.array(angles)
    xy = np.vstack([distances, angles])
    kde = gaussian_kde(xy)
    z = kde(xy)

    fig, ax = plt.subplots()
    sc = ax.scatter(distances, angles, c=z, s=20, cmap='copper_r')  # Updated color map to 'viridis' for better readability
    ax.set_xlabel('Distance')
    ax.set_ylabel('Angle')
    ax.set_title('Angle vs. Distance Distribution')  # Added a title to the plot
    fig.colorbar(sc, label='Density')  # Added a label for the colorbar

    # Adding grid lines
    ax.grid(True, linestyle='--', linewidth=0.5, alpha=0.7)

    plt.show()

import numpy as np
import multiprocessing as mp
from tqdm import tqdm

import numpy as np
import multiprocessing as mp
from tqdm import tqdm

def process_frame(frame, object_name, atom1_angle, atom2_angle, atom3_angle, atom5, atom6):
    pymol.cmd.frame(frame)
    distance_i = pymol.cmd.get_distance(atom5 + ' & ' + object_name, atom6 + ' & ' + object_name)
    angle = pymol.cmd.get_angle(atom1_angle + ' & ' + object_name, atom2_angle + ' & ' + object_name,
                                atom3_angle + ' & ' + object_name)
    return distance_i, angle

def angle_vs_dist_distribution(object_name, atom1_angle, atom2_angle, atom3_angle, atom5, atom6, num_processes=2):
    num_states = pymol.cmd.count_states(object_name)

    # Create a list of frames to be processed
    frames_to_process = [(i + 1, object_name, atom1_angle, atom2_angle, atom3_angle, atom5, atom6) for i in range(num_states)]

    # Initialize the tqdm progress bar
    pbar = tqdm(total=num_states, desc='Processing frames')

    # Function to update the progress bar
    def update_bar(result):
        pbar.update(1)

    with mp.Pool(processes=num_processes) as pool:
        results = []
        for frame_data in frames_to_process:
            result = pool.apply_async(process_frame, args=frame_data, callback=update_bar)
            results.append(result)

        distances = []
        angles = []
        for result in results:
            distance_i, angle = result.get()
            distances.append(distance_i)
            angles.append(angle)

    # Save the table dist vs frame in the current directory, using numpy
    np.savetxt('angle_vs_dist_distribution.txt', np.column_stack([distances, angles]), fmt='%f %f', header='Distance Angle')

    plot_contour(distances, angles)
    return distances, angles


print("USAGE: angle_vs_dist_distribution('object_name','atom1_angle', 'atom2_angle', 'atom3_angle', 'atom1_distance', 'atom2_distance', num_processes=2)")

