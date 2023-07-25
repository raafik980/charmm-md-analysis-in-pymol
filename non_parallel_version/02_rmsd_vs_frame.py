# Import necessary libraries
import matplotlib.pyplot as plt  # For plotting the data
from pymol import cmd            # For working with PyMOL commands

# Define a function to plot RMSD vs frame number
def RMSD_vs_frame(object_1, stride=1):
    # Initialize an empty list to store RMSDs
    RMSDs = []
    
    # Create a reference object (frame 1) to compare with other frames
    pymol.cmd.create('ref', object_1, 1, 1)
    
    # Loop through each frame of the molecular structure
    for i in range(1, pymol.cmd.count_states(object_1) + 1, stride):
        # Set the current frame to the i-th frame
        pymol.cmd.frame(i)
        
        # Calculate the RMSD between object_1 and 'ref' (reference object) in the current frame
        RMSD = pymol.cmd.rms_cur(object_1, 'ref', i, 0)  # Matching by order (0), not by atom names (1)
        
        # Append the calculated RMSD to the RMSDs list
        RMSDs.append(RMSD)
        
        # Optional: Print the current frame number and RMSD value
        print("Frame:", i, "RMSD:", RMSD)
    
    # Plotting the RMSD values
    plt.plot(range(1, pymol.cmd.count_states(object_1) + 1, stride), RMSDs)
    plt.xlabel("Frame Number")
    plt.ylabel("RMSD")
    plt.title("RMSD vs Frame Number")
    plt.show()

# Usage: RMSD_vs_frame('object_name', stride=1)
print("USAGE: RMSD_vs_frame('protein selection', stride=5)")
