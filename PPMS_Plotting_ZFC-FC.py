#!python
import os
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import numpy as np
import math

plt.style.use('sty-plot')

def parse_dat(file):
    # ----------------------------------------------------------------------
    # File parsing: Read in file and return corresponding data
    state = 0   # 0 = header
    temperature_list = []
    magnetic_field_list = []
    moment_list = []
    moment_err_list = []
    for line in file:
        line = line[:-1]
        if line == "[Data]":
            state = 1
            continue
        if state == 0:
            if "SAMPLE_COMMENT" in line:
                density = float(line.split(',')[1])
            if "SAMPLE_MASS" in line:
                mass = float(line.split(',')[1])
            if "SAMPLE_MOLECULAR_WEIGHT" in line:
                molar_mass = float(line.split(',')[1])
        else:
            if line[0] == ',':
                if "" not in line.split(',')[2:6]:
                    temperature, magnetic_field, moment, moment_err = [float(element) for element in line.split(',')[2:6]]
                    temperature_list.append(temperature)
                    magnetic_field_list.append(magnetic_field)
                    moment_list.append(moment)
                    moment_err_list.append(moment_err)
    return {'density': density, 'mass': mass, 'molar_mass': molar_mass, 'data': [temperature_list, magnetic_field_list, moment_list, moment_err_list]}
    # ----------------------------------------------------------------------

ppms_folder_path = os.path.join("Sample_data","PPMS") # <<-- INPUT: Adjust folder names if not identical to "Sample_data\PPMS"
folder_names = [foldername for foldername in os.listdir(ppms_folder_path) if not os.path.isfile(os.path.join(ppms_folder_path, foldername))]
folder_names.sort()

samples = []

# ----------------------------------------------------------------------
# Go through folders and read in data from ZFC/FC DAT-files for different samples
for foldername in folder_names:
    sample_folder_path = os.path.join(ppms_folder_path, foldername)
    file_names = [filename for filename in os.listdir(sample_folder_path) if os.path.isfile(os.path.join(sample_folder_path, filename)) and filename.split('.')[-1] == 'DAT']
    
    zfc_fc = {}
    for filename in file_names:
        if "ZFC" in filename:
            with open(os.path.join(sample_folder_path, filename), "r") as f:
                zfc_fc = parse_dat(f)

    samples.append({'sample_name': foldername, 'zfc_fc': zfc_fc})
# ----------------------------------------------------------------------

# ----------------------------------------------------------------------
# For every sample, plot the data
for sample in samples:
    plt.figure(figsize=(6,5))
    ax = plt.axes()

    # ----------------------------------------------------------------------
    # Split x-values corresponding to ZFC and FC curves
    zfc_fc = sample['zfc_fc']
    prev_temp = 0
    index = 0
    for temp in zfc_fc['data'][0]:
        if temp-prev_temp < 0:
            break
        else:
            index += 1
            prev_temp = temp
    zfc_x = zfc_fc['data'][0][:index]
    fc_x = zfc_fc['data'][0][index:]
    # ----------------------------------------------------------------------

    # ----------------------------------------------------------------------
    # Calculate corresponding y-values
    moment_korr = np.array(zfc_fc['data'][2])-(1.48*(10**-7)-(9.06*(10**-9)*np.array(zfc_fc['data'][1])))
    y = 4*math.pi*moment_korr*zfc_fc['density']/(zfc_fc['mass']/1000*np.array(zfc_fc['data'][1]))
    zfc_y = y[:index]
    fc_y = y[index:]

    magnetic_field = zfc_fc['data'][1][1]
    magnetic_field = round(magnetic_field)
    # ----------------------------------------------------------------------

    # ----------------------------------------------------------------------
    # The actual plotting and style
    plt.plot(zfc_x, zfc_y, color = "red", label = "ZFC " + str(magnetic_field) + " Oe", linewidth=1, marker='o', markersize=3, markeredgewidth=1)
    plt.plot(fc_x, fc_y, color = "black", label = "FC " + str(magnetic_field) + " Oe", linewidth=1, marker='o', markersize=3, markeredgewidth=1)

    ax.set_xlabel("$T$ (K)") # Label of x-axis
    ax.set_ylabel("$4\mathrm{\pi}\chi_{\mathrm{V}}$") # Label of y-axis

    # ----------------------------------------------------------------------
    # Criterion for plotting ranges of x and y values
    # Might be customized based on data ranges
    for i in range(len(zfc_x)):
        if zfc_x[i] > 20:
            break

    # Depending on criterion above, the upper and lower limits of x and y as well as the locators on the axes are set
    if zfc_y[i] < -0.1:
        plt.xlim(0,60)
        ax.xaxis.set_major_locator(ticker.MultipleLocator(10))
        ax.xaxis.set_minor_locator(ticker.MultipleLocator(5))
    else:
        plt.xlim(0,20)
        ax.xaxis.set_major_locator(ticker.MultipleLocator(2))
        ax.xaxis.set_minor_locator(ticker.MultipleLocator(1))

    # if zfc_y.min() > -0.6:
    #     plt.ylim(-0.6,)
    #     ax.yaxis.set_major_locator(ticker.MultipleLocator(0.1))
    #     ax.yaxis.set_minor_locator(ticker.MultipleLocator(0.05))
    # elif zfc_y.min() > -1:
    #     plt.ylim(-1,)
    #     ax.yaxis.set_major_locator(ticker.MultipleLocator(0.2))
    #     ax.yaxis.set_minor_locator(ticker.MultipleLocator(0.1))
    # elif zfc_y.min() > -1.5:
    #     ax.yaxis.set_major_locator(ticker.MultipleLocator(0.2))
    #     ax.yaxis.set_minor_locator(ticker.MultipleLocator(0.1))
    # elif zfc_y.min() > -2.5:
    #     ax.yaxis.set_major_locator(ticker.MultipleLocator(0.4))
    #     ax.yaxis.set_minor_locator(ticker.MultipleLocator(0.2))
    # else:
    #     ax.yaxis.set_major_locator(ticker.MultipleLocator(0.5))
    #     ax.yaxis.set_minor_locator(ticker.MultipleLocator(0.25))


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
        left=True,         # ticks along the left edge are on
        labelleft=True) # labels along the left edge are on

    ax.legend(frameon=False, loc='lower right') # Parameters for legend

    plt.savefig("Sample_data/PPMS/" + sample["sample_name"] + "_ZFC-FC.svg")
    plt.show()