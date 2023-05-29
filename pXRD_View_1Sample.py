#!python
import os
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import numpy as np

plt.style.use('sty-plot')

xrd_folder_path = os.path.join("Sample_data","XRD","View") # <<-- INPUT: Adjust folder names if not identical to "Sample_data\XRD\View"
file_names = [filename for filename in os.listdir(xrd_folder_path) if os.path.isfile(os.path.join(xrd_folder_path, filename))]
file_names = [filename for filename in file_names if filename.split('.')[-1]=='xy'] # Only lists xy-files
file_names.sort()

samples = []

# ----------------------------------------------------------------------
# Go through files and read in data from xy-files for different samples
for filename in file_names:
    with open(os.path.join(xrd_folder_path, filename), "r") as f:
        x_values = []
        y_values = []
        for line in f:
            if line.split():
                x_values.append(float(line.split()[0]))
                y_values.append(float(line.split()[1]))
    sample = {"name": filename.split('.')[0], "data": (x_values, y_values)}
    samples.append(sample)
# ----------------------------------------------------------------------

# ----------------------------------------------------------------------
# For every sample, plot the data
for sample in samples:
    plt.figure(figsize=(8,5)) # Parameters for size of the figure
    ax = plt.axes()
    plt.plot(sample["data"][0], sample["data"][1], color='red', linewidth=1) # Parameters for actual plot
    
    ax.set_xlabel(U'2 ${\U0001D703}$ (°)') # Label for x-axis
    ax.set_ylabel('Intensity (a.u.)', labelpad=10) # Label for y-axis

    ax.xaxis.set_major_locator(ticker.MultipleLocator(10)) # Set locators for ticks on x-axis
    ax.xaxis.set_minor_locator(ticker.MultipleLocator(5))

    ax.tick_params(
        axis='x',          # changes apply to the x-axis
        which='both',      # both major and minor ticks are affected
        bottom=True,      # ticks along the bottom edge are on
        top=False,         # ticks along the top edge are off
        labelbottom=True)  # labels along the bottom edge are on

    ax.tick_params(
        axis='both',          # changes apply to both axis
        which='major',      # major ticks are affected
        length=5)          # length in points

    ax.tick_params(
        axis='both',          # changes apply to both axis
        which='minor',      # minor ticks are affected
        length=3)          # length in points

    ax.tick_params(
        axis='y',          # changes apply to the y-axis
        which='both',      # both major and minor ticks are affected
        right=False,      # ticks along the right edge are off
        left=False,         # ticks along the left edge are off
        labelleft=False) # labels along the left edge are off

    # Set range/limits for x and y values
    plt.xlim(x_values[0],x_values[-1])
    #plt.xlim(5, 30)
    #plt.ylim(min(sample["data"][1]), max(sample["data"][1][2:]))
    plt.tight_layout()

    plt.savefig('Sample_data/XRD/' + sample["name"] + '.svg')
    plt.show()