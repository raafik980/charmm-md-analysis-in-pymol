# Import necessary libraries
import matplotlib.pyplot as plt  # For plotting the data
from pymol import cmd            # For working with PyMOL commands
import numpy as np

# Define a function to plot distance vs frame number
def dist_vs_frame(object_1, atom1_1, atom1_2):
    # Initialize an empty list to store distances
    distances_1 = []
    
    # Loop through each frame of the molecular structure
    for i in range(pymol.cmd.count_states(object_1)):
        # Set the current frame to the i-th frame
        pymol.cmd.frame(i + 1)
        
        # Calculate the distance between atom1_1 and atom1_2 in the current frame
        distance1 = pymol.cmd.get_distance(atom1_1 + ' & ' + object_1, atom1_2 + ' & ' + object_1)
        
        # Append the calculated distance to the distances_1 list
        distances_1.append(distance1)
        print(i)

    # Create x and y data for the plot
    x1 = range(len(distances_1))  # Frame numbers will be on the x-axis
    y1 = distances_1              # Distances will be on the y-axis

    # Save the table dist vs frame in the current directory, using numpy
    np.savetxt('dist_vs_frame.txt', np.column_stack([x1, y1]), fmt='%d %f', header='Frame Distance')


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

# Print the usage of the function
print("USAGE: dist_vs_frame('object_name', 'atom1', 'atom2')")
