#!python
import os
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import numpy as np

plt.style.use('sty-plot')

divers_folder_path = os.path.join("Sample_data","Divers")
file_names = [filename for filename in os.listdir(divers_folder_path) if os.path.isfile(os.path.join(divers_folder_path, filename))]
file_names = [filename for filename in file_names if filename.split('.')[-1]=='txt']

data_plots = []
delta = u'${\u0394}$'

for filename in file_names:
    with open(os.path.join(divers_folder_path, filename), "r") as f:
        x_values = []
        y_values = []
        line_number = 0
        for line in f:
            if line_number == 0:
                x_label = line.split(',')[0]
                if 'delta' in filename:
                    x_label = delta + x_label
                y_label = line.split(',')[1].replace('\n', '')
                x_label = x_label.replace(x_label[x_label.find('°C') - 1], '')
            else:
                if line.split():
                    x_values.append(float(line.split()[0]))
                    y_values.append(float(line.split()[1]))
            line_number += 1
    data_plot = {"name": filename.split('.')[0], "label": (x_label, y_label), "data": (x_values, y_values)}
    data_plots.append(data_plot)


fig, ax1 = plt.subplots(figsize=(8,6))
ax2 = ax1.twiny()

legend_names = [delta + '$T$ = 140 °C', '$T_{down}$ = 390 °C']

curve1, = ax1.plot(data_plots[1]["data"][0], data_plots[1]["data"][1], label=legend_names[0], color='blue', marker='o')
curve2, = ax2.plot(data_plots[0]["data"][0], data_plots[0]["data"][1], label=legend_names[1], color='red', marker='o')

curves = [curve1, curve2]

ax1.set_xlabel(data_plots[1]["label"][0], color='blue')
ax2.set_xlabel(data_plots[0]["label"][0], color='red')
ax1.set_ylabel(data_plots[1]["label"][1])

ax2.spines['bottom'].set_color('blue')
ax2.spines['top'].set_color('red')

ax1.xaxis.set_major_locator(ticker.MultipleLocator(20))
ax2.xaxis.set_major_locator(ticker.MultipleLocator(20))
ax1.xaxis.set_minor_locator(ticker.MultipleLocator(10))
ax2.xaxis.set_minor_locator(ticker.MultipleLocator(10))

ax1.tick_params(
    axis='x',          # changes apply to the x-axis
    which='both',      # both major and minor ticks are affected
    bottom=True,      # ticks along the bottom edge are off
    top=False,         # ticks along the top edge are off
    labelbottom=True,  # labels along the bottom edge are off
    colors='blue')

ax1.tick_params(
    axis='both',          # changes apply to both axis
    which='major',      # major ticks are affected
    length=5)          # length in points

ax1.tick_params(
    axis='both',          # changes apply to both axis
    which='minor',      # major ticks are affected
    length=3)          # length in points

ax1.tick_params(
    axis='y',          # changes apply to the y-axis
    which='both',      # both major and minor ticks are affected
    right=False,      # ticks along the bottom edge are off
    left=True,         # ticks along the top edge are off
    labelleft=True) # labels along the bottom edge are off

ax2.tick_params(
    axis='x',          # changes apply to the x-axis
    which='both',      # both major and minor ticks are affected
    bottom=False,      # ticks along the bottom edge are off
    top=True,         # ticks along the top edge are off
    labelbottom=False,  # labels along the bottom edge are off
    labeltop=True,
    colors='red')

ax2.tick_params(
    axis='x',          # changes apply to both axis
    which='major',      # major ticks are affected
    length=5)          # length in points

ax2.tick_params(
    axis='x',          # changes apply to both axis
    which='minor',      # major ticks are affected
    length=3)          # length in points

#ax1.legend(frameon=False)
ax2.legend(curves, [curve.get_label() for curve in curves], frameon=False, loc='lower left')

#plt.xlim(x_values[0],x_values[-1])
plt.tight_layout()

plt.savefig('DeltaT-T-Dependence.png')
plt.show()