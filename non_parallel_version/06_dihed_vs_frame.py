# Import necessary libraries
import matplotlib.pyplot as plt  # For plotting the data
from pymol import cmd            # For working with PyMOL commands
import numpy as np

# Define a function to plot dihedral vs frame number
def dihed_vs_frame(object_1, atom1_1, atom1_2, atom1_3, atom1_4 ):
    # Initialize an empty list to store distances
    dihedral_1 = []
    
    # Loop through each frame of the molecular structure
    for i in range(pymol.cmd.count_states(object_1)):
        # Set the current frame to the i-th frame
        pymol.cmd.frame(i + 1)
        
        # Calculate the dihedral between atom1_1, atom1_2, atom1_3, atom1_4 in the current frame
        dihedral1 = pymol.cmd.get_dihedral(atom1_1 + ' & ' + object_1, atom1_2 + ' & ' + object_1, atom1_3 + ' & ' + object_1, atom1_4 + ' & ' + object_1)
        
        if dihedral1 < 0:
            dihedral1 = dihedral1 + 360
        else:
            dihedral1 = dihedral1


        # Append the calculated dihedral to the dihedral_1 list
        dihedral_1.append(dihedral1)
        print(i)

    # Create x and y data for the plot
    x1 = range(len(dihedral_1))  # Frame numbers will be on the x-axis
    y1 = dihedral_1             # dihedral will be on the y-axis 

    # Save the table dist vs frame in the current directory, using numpy
    np.savetxt('dihed_vs_frame.txt', np.column_stack([x1, y1]), fmt='%d %f', header='Frame Dihedral')


    # Plot the data
    plt.figure()
    plt.plot(x1, y1, label=object_1, color='royalblue', linewidth=2)
    plt.xlabel('Frame', fontsize=12)
    plt.ylabel('Dihedral', fontsize=12)
    plt.title('Dihedral vs Frame', fontsize=16)
    plt.legend(fontsize=10)
    plt.grid(True, linestyle='--', linewidth=0.5, alpha=0.7)
    plt.tick_params(axis='both', which='major', labelsize=10)
    plt.tight_layout()  # Adjust the spacing for better layout
    plt.show()  # Display the plot

# Print the usage of the function
print("USAGE: dihed_vs_frame('object_name', 'atom1', 'atom2', 'atom3', 'atom4')")
