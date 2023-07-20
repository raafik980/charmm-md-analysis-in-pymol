import matplotlib.pyplot as plt
from pymol import cmd
from multiprocessing import Pool, cpu_count
import numpy as np
from tqdm import tqdm

# Define a function to calculate distance for a single frame
def calculate_distance(frame_number, object_1, atom1_1, atom1_2):
    cmd.frame(frame_number)
    distance1 = cmd.get_distance(atom1_1 + ' & ' + object_1, atom1_2 + ' & ' + object_1)
    return distance1

# Define the process_distance function outside of dist_vs_frame
def process_distance(args):
    return calculate_distance(*args)

# Define a function to plot distance vs frame number
def dist_vs_frame(object_1, atom1_1, atom1_2, num_process=1):
    # Initialize an empty list to store distances
    distances_1 = []

    # Calculate total number of frames
    total_frames = cmd.count_states(object_1)

    # Set default number of processes if not specified
    if num_process == 1:
        num_process = min(cpu_count(), total_frames)  # Use the number of CPU cores or total_frames, whichever is smaller

    # Create a list of frame numbers to process
    frames_to_process = range(1, total_frames + 1)

    # Create a list of arguments for the process_distance function
    args_list = [(frame_number, object_1, atom1_1, atom1_2) for frame_number in frames_to_process]

    # Create a pool of workers for multiprocessing
    with Pool(processes=num_process) as pool, tqdm(total=len(args_list), desc="Calculating Distances") as pbar:
        # Use multiprocessing to calculate distances for each frame
        for distance in pool.imap_unordered(process_distance, args_list):
            distances_1.append(distance)
            pbar.update(1)  # Update the progress bar

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
print("USAGE: dist_vs_frame('object_name', 'atom1', 'atom2', num_process=1)")
