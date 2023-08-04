# Import necessary libraries
import matplotlib.pyplot as plt  # For plotting the data
from pymol import cmd            # For working with PyMOL commands
import numpy as np

def domain_cmass_dist_vs_frame(object_name, sele_ref, sele_target):
    target_ref = []
    for i in range(pymol.cmd.count_states(object_name)):
        pymol.cmd.frame(i+1)
        com1 = pymol.cmd.centerofmass(sele_ref)
        com2 = pymol.cmd.centerofmass(sele_target)
        target_ref_i = np.sqrt((com1[0]-com2[0])**2 + (com1[1]-com2[1])**2 + (com1[2]-com2[2])**2)
        target_ref.append(target_ref_i)
        print(i)
    
        # Create x and y data for the plot
    
    x1 = range(len(target_ref))  # Frame numbers will be on the x-axis
    x1 = [(i+1)/50 for i in x1]  #rescale the x-axis to ns (50 frames per ns)
    y1 = target_ref              # Distances will be on the y-axis

    # Save the table dist vs frame in the current directory, using numpy
    np.savetxt('cmass_dist_vs_frame.txt', np.column_stack([x1, y1]), fmt='%f %f')

    # Plot the data
    plt.figure()
    plt.plot(x1, y1, label=object_name, color='royalblue', linewidth=2)
    plt.xlabel('Time(ns)', fontsize=12)
    plt.ylabel('CMass Distance', fontsize=12)
    plt.title('CMass Distance vs Time(ns)', fontsize=16)
    plt.legend(fontsize=10)
    plt.grid(True, linestyle='--', linewidth=0.5, alpha=0.7)
    plt.tick_params(axis='both', which='major', labelsize=10)
    plt.tight_layout()  # Adjust the spacing for better layout
    plt.show()  # Display the plot

# Print the usage of the function
print("USAGE: domain_cmass_dist_vs_frame('object_name', 'sele_ref', 'sele_target')")
print("EXAMPLE: domain_cmass_dist_vs_frame( ' pdt ', '  ( /pdt/PROA/P ) and ( name  N+CA+C+O ) and  ( resi 3-5 or resi 12-23 or resi 81-85 or resi 105-110  ) ',  ' (  /pdt/PROA/P ) and ( name N+CA+C+O )  and  ( resi 117-167  ) ' ) ")
print("EXAMPLE: domain_cmass_dist_vs_frame( ' pdt ', '  ( /pdt/PROA/P ) and ( name  N+CA+C+O ) and  ( resi 3-5 or resi 12-23 or resi 81-85 or resi 105-110  ) ', ' ( /pdt/PROA/P ) and ( name  N+CA+C+O )  and  ( resi 31-55  )' ) ")
#print("EXAMPLE: domain_cmass_dist_vs_frame( ' pdt ', ' (  /pdt/PROA/P ) and ( name N+CA+C+O )  and  ( resi 166-167  ) ', ' ( /pdt/PROA/P ) and ( name  N+CA+C+O )  and  ( resi 55-57  )' ) ")
#print("EXAMPLE: domain_cmass_dist_vs_frame( ' rct ', ' ( /pdt/PROA/P ) and ( name  N+CA+C+O )  and  ( resi 55-57  )',  ' (  /rct/PROA/P ) and ( name N+CA+C+O )  and  ( resi 6-11  ) ' ) ")

