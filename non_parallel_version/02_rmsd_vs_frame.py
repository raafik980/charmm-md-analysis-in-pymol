# Import necessary libraries
import matplotlib.pyplot as plt  # For plotting the data
from pymol import cmd            # For working with PyMOL commands

# Define a function to plot RMSD vs frame number
def RMSD_vs_frame(object_1, stride=1):
    # Initialize an empty list to store RMSDs
    RMSDs = []
    pymol.cmd.create('ref', object_1, 1, 0)
    
    # Loop through each frame of the molecular structure
    for i in range(1, pymol.cmd.count_states(object_1) + 1 , stride):
        # Set the current frame to the i-th frame
        pymol.cmd.frame(i)

        
        
        # Calculate the RMSD between object_1 and object_2 in the current frame
        #cmd.align(object_1, 'ref',i,1)
        RMSD = pymol.cmd.rms_cur(object_1, 'ref', i, 0)
        
        # Append the calculated RMSD to the RMSDs list
        RMSDs.append(RMSD)
        print(i)

    # Create x and y data for the plot
    x1 = range(1, pymol.cmd.count_states(object_1) + 1, stride)  # Frame numbers will be on the x-axis
    y1 = RMSDs                                                   # RMSDs will be on the y-axis

    # Plot the data
    plt.figure()
    plt.plot(x1, y1, label=object_1, color='royalblue', linewidth=2)
    plt.xlabel('Frame', fontsize=12)
    plt.ylabel('Distance', fontsize=12)
    plt.title('Distance vs Frame', fontsize=16)
    plt.legend(fontsize=10)
    plt.grid(True, linestyle='--', linewidth=0.5, alpha=0.7)
    plt.tick_params(axis='both', which='major', labelsize=10)
    plt.tight_layout()  # Adjust the spacing for better layout
    plt.show()  # Display the plot

# Usage: RMSD_vs_frame('object_name', stride=1)
print("USAGE: RMSD_vs_frame('object_name', stride=5)")
