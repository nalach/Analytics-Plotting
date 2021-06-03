#!python
import os
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import numpy as np

plt.style.use('sty-plot')

xrd_folder_path = os.path.join("Sample_data","XRD")
file_names = [filename for filename in os.listdir(xrd_folder_path) if os.path.isfile(os.path.join(xrd_folder_path, filename))]
file_names = [filename for filename in file_names if filename.split('.')[-1]=='xy']
file_names.sort()

samples = []

for filename in file_names:
    with open(os.path.join(xrd_folder_path, filename), "r") as f:
        x_values = []
        y_values = []
        for line in f:
            if line.split():
                x_values.append(float(line.split()[0]))
                y_values.append(float(line.split()[1]))
    sample = {"name": filename.split('_')[1], "data": (x_values, y_values)}
    samples.append(sample)

fig = plt.figure(figsize=(8,8))

gs = fig.add_gridspec(len(samples), hspace=0)

graph = gs.subplots(sharex=True)

fig.add_subplot(111, frameon=False)
# hide tick and tick label of the big axis
plt.tick_params(labelcolor='none', which='both', top=False, bottom=False, left=False, right=False)

delta = u'${\u0394}$'

labels = []

with open(os.path.join(xrd_folder_path, 'Labels.txt'), "r") as f:
    for line in f:
        line = line.replace('\n', '')
        # line = line.replace(line[line.find('°C') - 1], '')
        labels.append(line)


for i in range(len(samples)):
    graph[i].plot(samples[i]["data"][0], samples[i]["data"][1], label=samples[i]["name"] + ', ' + labels[i], color='blue')

counter = 0

for ax in graph:
    #ax.set(xlabel=U'2 ${\U0001D703}$ (°)', ylabel='Intensity (a.u.)')
    ax.set(xlabel=U'2 ${\U0001D703}$ (°)')
    ax.label_outer()
    ax.xaxis.set_major_locator(ticker.MultipleLocator(5))
    ax.xaxis.set_minor_locator(ticker.MultipleLocator(2.5))

    ax.tick_params(
        axis='x',          # changes apply to the x-axis
        which='both',      # both major and minor ticks are affected
        bottom=True,      # ticks along the bottom edge are off
        top=False,         # ticks along the top edge are off
        labelbottom=counter == len(samples)-1)  # labels along the bottom edge are off

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

    ax.set_xlim(3,45)
    ax.legend(frameon=False)

    counter += 1


plt.tight_layout()
plt.ylabel('Intensity (a.u.)', labelpad=-20)
plt.subplots_adjust(left  = 0)

plt.savefig('Test.png')
plt.show()
