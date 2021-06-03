#!python
import os
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import numpy as np
import math

plt.style.use('sty-plot')

tga_folder_path = os.path.join("Sample_data","TGA-DSC")
file_names = [filename for filename in os.listdir(tga_folder_path) if os.path.isfile(os.path.join(tga_folder_path, filename)) and filename.split('.')[-1]=='txt']
file_names.sort()
sample_names = [''.join(''.join(filename.split('_')[-2:]).split(".")[:-1]) for filename in file_names]

for filename in file_names:
    with open(os.path.join(tga_folder_path, filename), 'r') as file:
        state = 0
        segment_1 = []
        segment_2 = []
        for line in file:
            line = line.replace(' ', '')[:-1]
            if line[0:2] == "##":
                state = 1
            if state == 1:
                if line[-1:] == '1':
                    segment_1.append(line)
                elif line[-1:] == '2':
                    segment_2.append(line)
    heating = {'temperature': [], 'time': [], 'mass': []}
    holding = {'time': [], 'mass': []}
    for line in segment_1:
        heating['temperature'].append(float(line.split(';')[0]))
        heating['time'].append(float(line.split(';')[1]))
        heating['mass'].append(float(line.split(';')[3]))
    for line in segment_2:
        holding['time'].append(float(line.split(';')[1]))
        holding['mass'].append(float(line.split(';')[3]))
    

delta = u'${\u0394}$'

plt.figure(figsize=(8,6))
ax = plt.axes()

legend_names = [delta + '$T$ / ' + delta + '$t$ = 10 °C / min', '$T$ = 200 °C']

plt.plot(heating['time'], heating['mass'], label=legend_names[0], color='blue', linewidth=3)
plt.plot(holding['time'], holding['mass'], label=legend_names[1], color='red', linewidth=3)

ax.set_xlabel("$t$ (min)")
ax.set_ylabel("$m$ (%)")

ax.xaxis.set_major_locator(ticker.MultipleLocator(10))
ax.xaxis.set_minor_locator(ticker.MultipleLocator(5))
ax.yaxis.set_major_locator(ticker.MultipleLocator(2))
ax.yaxis.set_minor_locator(ticker.MultipleLocator(1))

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
    left=True,         # ticks along the top edge are off
    labelleft=True) # labels along the bottom edge are off

ax.legend(frameon=False)

plt.ylim(85,)

plt.tight_layout()

plt.savefig("TGA_NL033.png")
plt.show()



