#!python
import os
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import numpy as np

plt.style.use('sty-plot')

def read_graphs_file(file_path):
    line_number = 0
    data = []
    with open(file_path, "r") as f:
        for line in f:
            if line_number != 0:
                if line_number == 1:
                    labels = line[:-1].split(",")
                else:
                    numeric_data = [float(element) for element in line[:-1].split(",")]
                    if numeric_data[2] != 0:
                        data.append(numeric_data)
            line_number += 1

    labels[0] = U'2 ${\U0001D703}$ (°)'
    labels[1] = "Y$_{\mathrm{obs}}$"
    labels[2] = "Y$_{\mathrm{calc}}$"
    labels[3] = "Difference"

    x_values = [row[0] for row in data]
    y_obs = [row[1] for row in data]
    y_calc = [row[2] for row in data]
    diff = [row[3] for row in data]

    if max(y_obs) < max(y_calc):
        maximum = max(y_calc)
    else:
        maximum = max(y_obs)
    
    y_obs = [element/maximum for element in y_obs]
    y_calc = [element/maximum for element in y_calc]
    diff = [element/maximum for element in diff]

    return (x_values, y_obs, y_calc, diff, labels)

def plot_sample(x_values, y_obs, y_calc, diff, labels, tickfiles, sample_name):
    plt.figure(figsize=(8,6))
    ax = plt.axes()
    plt.plot(x_values, y_obs, color='blue', marker='o', markersize=4, markeredgewidth=1, linestyle='none', markerfacecolor='none')
    plt.plot(x_values, y_calc, color='red', linewidth=2)
    plt.plot(x_values, diff, color='grey', linewidth=1)
    tick_y = -0.15
    for tickfile in tickfiles:
        plt.plot(tickfile["data"], [tick_y]*len(tickfile["data"]), marker='|', linestyle='none')
        tick_y -= 0.08

    # hfont = {'fontname':'Comic Sans MS'}

    ax.set_xlabel(labels[0])
    # ax.set_xlabel(labels[0], **hfont)
    ax.set_ylabel('Intensity (a.u.)', labelpad=10)

    ax.xaxis.set_major_locator(ticker.MultipleLocator(5))
    ax.xaxis.set_minor_locator(ticker.MultipleLocator(2.5))

    ax.tick_params(
        axis='x',          # changes apply to the x-axis
        which='both',      # both major and minor ticks are affected
        bottom=True,      # ticks along the bottom edge are off
        top=False,         # ticks along the top edge are off
        labelbottom=True)  # labels along the bottom edge are off

    ax.tick_params(
        axis='both',          # changes apply to both axis
        which='major',      # major ticks are affected
        length=5)          # length in points

    ax.tick_params(
        axis='both',          # changes apply to both axis
        which='minor',      # major ticks are affected
        length=3)          # length in points

    ax.tick_params(
        axis='y',          # changes apply to the y-axis
        which='both',      # both major and minor ticks are affected
        right=False,      # ticks along the bottom edge are off
        left=False,         # ticks along the top edge are off
        labelleft=False) # labels along the bottom edge are off

    ax.legend(labels[1:], frameon=False)

    plt.xlim(x_values[0],x_values[-1])
    plt.tight_layout()

    plt.savefig(sample_name + '.png')
    plt.show()

xrd_folder_path = os.path.join("Sample_data","XRD")
file_names = [filename for filename in os.listdir(xrd_folder_path) if os.path.isfile(os.path.join(xrd_folder_path, filename))]
file_names = [''.join(filename.split('.')[:-1]) for filename in file_names if filename.split('.')[-1]=='txt']
file_names.sort()
samples = []
for filename in file_names:
    if filename.split('_')[0] not in samples:
        samples.append(filename.split('_')[0])

for sample in samples:
    tickfiles = []
    for filename in file_names:
        if filename.split('_')[0] == sample:
            if filename.split('_')[-1] == 'Graphs':
                x_values, y_obs, y_calc, diff, labels = read_graphs_file(os.path.join(xrd_folder_path, filename + '.txt'))
            if filename.split('_')[-1] == 'Ticks':
                with open(os.path.join(xrd_folder_path, filename + '.txt'), 'r') as tickfile:
                    tick_xs = []
                    for line in tickfile:
                        tick_xs.append(float(line.split()[0]))
                    tickfiles.append({"name": filename.split('_')[-2], "data": tick_xs})
            if filename.split('_')[-1] == 'TicksLabels':
                with open(os.path.join(xrd_folder_path, filename + '.txt'), 'r') as ticklabelfile:
                    tick_labels = []
                    for line in ticklabelfile:
                        tick_labels.append(line.replace('\n', ''))
    for tick_label in tick_labels:
        labels.append(tick_label)
    plot_sample(x_values, y_obs, y_calc, diff, labels, tickfiles, sample)