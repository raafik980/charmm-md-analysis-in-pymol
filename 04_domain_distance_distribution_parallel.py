# Description: This script calculates the distance between the center of mass of the core and the center of mass of the domains.
# Plot the distribution of distances between the center of mass of the core and the center of mass of the domains.

import numpy as np
import pymol
import matplotlib.pyplot as plt
from scipy.stats import gaussian_kde
import multiprocessing as mp
from tqdm import tqdm

def plot_contour(dom1_core, dom2_core):
	dom1_core = np.array(dom1_core)
	dom2_core = np.array(dom2_core)
	xy = np.vstack([dom1_core, dom2_core])
	kde = gaussian_kde(xy)
	z = kde(xy)
	fig, ax = plt.subplots()
	sc = ax.scatter(dom1_core, dom2_core , c=z, s=20, cmap='copper_r')  # Updated color map to 'viridis' for better readability
	ax.set_xlabel('Core to Domain 1')
	ax.set_ylabel('Core to Domain 2')
	ax.set_title('Core to Domain Distance Distribution')  # Added a title to the plot
	fig.colorbar(sc, label='Density')  # Added a label for the colorbar

    # Adding grid lines
	ax.grid(True, linestyle='--', linewidth=0.5, alpha=0.7)
	plt.show()

def process_frame(frame, object_name, sele_core, sele_dom1, sele_dom2):
    pymol.cmd.frame(frame)
    com1 = pymol.cmd.centerofmass(sele_core)
    com2 = pymol.cmd.centerofmass(sele_dom1)
    com3 = pymol.cmd.centerofmass(sele_dom2)
    dom1_core_i = np.sqrt((com1[0]-com2[0])**2 + (com1[1]-com2[1])**2 + (com1[2]-com2[2])**2)
    dom2_core_i = np.sqrt((com1[0]-com3[0])**2 + (com1[1]-com3[1])**2 + (com1[2]-com3[2])**2)
    return dom1_core_i, dom2_core_i

def cmass_dist_distribution(object_name, sele_core, sele_dom1, sele_dom2, num_processes=2):
    num_states = pymol.cmd.count_states(object_name)

    # Create a list of frames to be processed
    frames_to_process = [(i + 1, object_name, sele_core, sele_dom1, sele_dom2) for i in range(num_states)]

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

        dom1_core = []
        dom2_core = []
        for result in results:
            dom1_core_i, dom2_core_i = result.get()
            dom1_core.append(dom1_core_i)
            dom2_core.append(dom2_core_i)

    # Convert the lists to numpy arrays
    dom1_core = np.array(dom1_core)
    dom2_core = np.array(dom2_core)

    # Save the data to files in the current directory, using numpy
    np.savetxt('dom1_core_distribution.txt', dom1_core, fmt='%f', header='Domain 1 Core Distance')
    np.savetxt('dom2_core_distribution.txt', dom2_core, fmt='%f', header='Domain 2 Core Distance')

    plot_contour(dom1_core, dom2_core)


    return dom1_core, dom2_core

print("USAGE: cmass_dist_distribution('object_name', 'core_selection', 'domain1_selection', 'domain2_selection', num_processes=2 )")
print("EXAMPLE: cmass_dist_distribution( ' traj ', '  ( /traj/PROA/P ) and ( name  N+CA+C+O ) and  ( resi 3-23 or resi 81-85 or resi 109-115  ) ',  ' (  /traj/PROA/P ) and ( name N+CA+C+O )  and  ( resi 129-159  ) ', ' ( /traj/PROA/P ) and ( name  N+CA+C+O )  and  ( resi 33-55  )', num_processes=2 ) ")