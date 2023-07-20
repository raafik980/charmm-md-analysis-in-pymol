import matplotlib.pyplot as plt
from pymol import cmd
from multiprocessing import Pool, cpu_count
from tqdm import tqdm  # Import tqdm for progress bar

# Define a function to calculate RMSD for a single frame
def calculate_rmsd(frame_number, object_1, reference_object):
    cmd.frame(frame_number)
    cmd.align(object_1, reference_object, frame_number, 1)
    return cmd.rms(object_1, reference_object, frame_number, 1)

# Define the process_frame function outside of RMSD_vs_frame
def process_frame(args):
    return calculate_rmsd(*args)

# Define a function to plot RMSD vs frame number
def RMSD_vs_frame(object_1, stride=1, num_process=1):
    # Initialize an empty list to store RMSDs
    RMSDs = []
    reference_object = 'ref'
    cmd.create(reference_object, object_1, 1, 1)
    
    # Calculate total number of frames
    total_frames = cmd.count_states(object_1)
    
    # Set default number of processes if not specified
    if num_process == 1:
        num_process = min(cpu_count(), total_frames)  # Use the number of CPU cores or total_frames, whichever is smaller

    # Create a list of frame numbers to process
    frames_to_process = range(1, total_frames + 1, stride)

    # Create a list of arguments for the process_frame function
    args_list = [(frame_number, object_1, reference_object) for frame_number in frames_to_process]

    # Create a pool of workers for multiprocessing
    with Pool(processes=num_process) as pool, tqdm(total=len(args_list), desc="Calculating RMSD") as pbar:
        # Use multiprocessing to calculate RMSD for each frame
        for rmsd in pool.imap_unordered(process_frame, args_list):
            RMSDs.append(rmsd)
            pbar.update(1)  # Update the progress bar

    # Create x and y data for the plot
    x1 = frames_to_process    # Frame numbers will be on the x-axis
    y1 = RMSDs                # RMSDs will be on the y-axis

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
    

# Usage: RMSD_vs_frame('object_name', stride=1, num_process=1)
print("USAGE: RMSD_vs_frame('object_name', stride=5, num_process=4)")
