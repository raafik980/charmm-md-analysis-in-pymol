# Description: This script calculates the distance between the center of mass of the core and the center of mass of the domains.
# Plot the distribution of distances between the center of mass of the core and the center of mass of the domains.

import numpy as np
import pymol
import matplotlib.pyplot as plt
from scipy.stats import gaussian_kde

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


def cmass_dist_distribution(object_name, sele_core, sele_dom1, sele_dom2 ):
	dom1_core = []
	dom2_core = []
	for i in range(pymol.cmd.count_states(object_name)):
		pymol.cmd.frame(i+1)
		com1 = pymol.cmd.centerofmass(sele_core)
		com2 = pymol.cmd.centerofmass(sele_dom1)
		com3 = pymol.cmd.centerofmass(sele_dom2)
		dom1_core_i = np.sqrt((com1[0]-com2[0])**2 + (com1[1]-com2[1])**2 + (com1[2]-com2[2])**2)
		dom2_core_i = np.sqrt((com1[0]-com3[0])**2 + (com1[1]-com3[1])**2 + (com1[2]-com3[2])**2)
		dom1_core.append(dom1_core_i)
		dom2_core.append(dom2_core_i)
		print(i)
	
	#save the table dist vs frame in the current directory, using numpy
	np.savetxt('cmass_dist_distribution.txt', np.column_stack([dom1_core, dom2_core]), fmt='%f %f', header='dom1_core dom2_core')

	plot_contour(dom1_core, dom2_core)
	return dom1_core,dom2_core


print("USAGE: cmass_dist_distribution('object_name', 'core_selection', 'domain1_selection', 'domain2_selection' )")

print("EXAMPLE: cmass_dist_distribution( ' traj ', '  ( /traj/PROA/P ) and ( name  N+CA+C+O ) and  ( resi 3-23 or resi 81-85 or resi 109-115  ) ',  ' (  /traj/PROA/P ) and ( name N+CA+C+O )  and  ( resi 129-159  ) ', ' ( /traj/PROA/P ) and ( name  N+CA+C+O )  and  ( resi 33-55  )' ) ")
