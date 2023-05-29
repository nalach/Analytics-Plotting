#!python
import os
import math
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import numpy as np

plt.style.use('sty-plot')

xrd_folder_path = os.path.join("Sample_data","XRD","Stacked")
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

#print(len(samples))

fig = plt.figure(figsize=(7,8))

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

wavelengths = []

with open(os.path.join(xrd_folder_path, 'Wavelengths.txt'), "r") as f:
    for line in f:
        line = line.replace('\n', '')
        wavelengths.append(float(line))

output_wavelength = input("Choose output wavelength [Ag / Cu / Mo]:")

if output_wavelength == "Ag":
    output_wavelength = 0.5594
    x_min = 1.5
    x_max = 25
elif output_wavelength == "Cu":
    output_wavelength = 1.5406
    x_min = 4.5
    x_max = 90
elif output_wavelength == "Mo":
    output_wavelength = 0.7093
    x_min = 2
    x_max = 30

for i in range(len(samples)):
    x_values_1_over_d = list(map(lambda x: 2 * math.sin(x/360*math.pi) / wavelengths[i], samples[i]["data"][0]))    # 1/d as x-value
    x_values_sin_term = list(map(lambda x: output_wavelength/2 * x, x_values_1_over_d))  # calculate term for sin-1
    x_values = list(map(lambda x: 2 * math.asin(x) * 180/math.pi, x_values_sin_term))   # lambda same for all
    #x_values = samples[i]["data"][0]    # same wavelength on default
    graph[i].plot(x_values, samples[i]["data"][1], label=labels[i], color='blue')

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

    #ax.set_xlim(0.06,0.65)
    ax.set_xlim(x_min,x_max)

    ax.legend(frameon=False)
    # change fontsize of legend:
    #  ax.legend(fontsize=18)  or  ax.legend(prop={'size':18})
    # change fontweight of legend:
    #  ax.legend(prop={'weight':'bold'})

    counter += 1


plt.tight_layout()
plt.ylabel('Intensity (a.u.)', labelpad=-20)
plt.subplots_adjust(left  = 0)

plt.savefig("Sample_data/XRD/Stacked.png")
plt.show()
