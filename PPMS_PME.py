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


ppms_folder_path = os.path.join("Sample_data","PPMS_PME")
folder_names = [foldername for foldername in os.listdir(ppms_folder_path) if not os.path.isfile(os.path.join(ppms_folder_path, foldername))]
folder_names.sort()

# samples = []

for foldername in folder_names:
    sample_folder_path = os.path.join(ppms_folder_path, foldername)
    file_name = input("Type filename for sample " + foldername + ":")

    with open(os.path.join(sample_folder_path, file_name), "r") as f:
        fc_pme = parse_dat(f)

#     samples.append({'sample_name': foldername, 'fc_pme': fc_pme})

# for sample in samples:
#     fc_pme = sample['fc_pme']
    index = 0
    index_list = []
    magnetic_fields_list = []
    magnetic_field = -1
    for mag_field in fc_pme['data'][1]:
        if mag_field != magnetic_field:
            index_list.append(index)
            mag_field_rounded = round(mag_field)
            magnetic_fields_list.append(mag_field_rounded)
            magnetic_field = mag_field
        index += 1

    moment_korr = np.array(fc_pme['data'][2])-(1.48*(10**-7)-(9.06*(10**-9)*np.array(fc_pme['data'][1])))
    y = 4*math.pi*moment_korr*fc_pme['density']/(fc_pme['mass']/1000*np.array(fc_pme['data'][1]))

    pme_x = []
    pme_y = []
    
    for i, element in enumerate(index_list):
        if i == (len(index_list)-1):
            x_y_index = len(y)
        else:
            x_y_index = index_list[i+1]
        x_list = fc_pme['data'][0][element:x_y_index-1]
        y_list = y[element:x_y_index-1]
        pme_x.append(x_list)
        pme_y.append(y_list)


    # ----------------------------------------------------------------------
    # 2D plot with different colors for every magnetic field
    plt.figure(figsize=(7,6))
    ax = plt.axes()

    color_list = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', '#8c564b', '#e377c2', '#7f7f7f', '#bcbd22', '#17becf']

    for i, field in enumerate(magnetic_fields_list):
        if field == 0:
            continue
        else:
            plt.plot(pme_x[i], pme_y[i], color=color_list[i], label = str(field) + ' Oe', linewidth=2)      #, marker='o', markersize=1, markeredgewidth=1
    
    ax.set_xlabel("$T$ (K)") # Label of x-axis
    ax.set_ylabel("$4\mathrm{\pi}\chi_{\mathrm{V}}$") # Label of y-axis

    plt.xlim(0,50)

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

    ax.legend(frameon=False, ncol=2) # Parameters for legend         loc='upper right', 

    plt.savefig("Sample_data/PPMS_PME/" + foldername + "_PME_2D_1.svg")
    plt.show()

    # ----------------------------------------------------------------------
    # 2D plot with color gradient for magnetic field
    plt.figure(figsize=(7,6))
    ax = plt.axes()

    color_list = ['#01097b', '#1b03c3', '#5202cf', '#750cad', '#9e1b74', '#c72f38', '#ea450d', '#fd5f04', '#ff872d', '#ffb578', '#ffdfc5']

    for i, field in enumerate(magnetic_fields_list):
        if field == 0:
            continue
        else:
            plt.plot(pme_x[i], pme_y[i], color=color_list[i], label = str(field) + ' Oe', linewidth=2)      #, marker='o', markersize=1, markeredgewidth=1
    
    ax.set_xlabel("$T$ (K)") # Label of x-axis
    ax.set_ylabel("$4\mathrm{\pi}\chi_{\mathrm{V}}$") # Label of y-axis

    plt.xlim(0,50)

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

    ax.legend(frameon=False, ncol=2) # Parameters for legend         loc='upper right', 

    plt.savefig("Sample_data/PPMS_PME/" + foldername + "_PME_2D_2.svg")
    plt.show()

    # ----------------------------------------------------------------------
    # 3D plot with color gradient for magnetic field
    ax = plt.figure().add_subplot(projection='3d')

    for i, field in enumerate(magnetic_fields_list):
        if field == 0:
            continue
        else:
            y_values = [field]*len(pme_x[i])
            ax.plot(pme_x[i], y_values, pme_y[i], color=color_list[i], label = str(field) + ' Oe')      #, linewidth=2, marker='o', markersize=1, markeredgewidth=1
    
    #ax.invert_yaxis()
    ax.set_xlim(0,50)
    ax.set_ylim(magnetic_fields_list[-1],0)

    ax.set_xlabel("$T$ (K)", labelpad=10) # Label of x-axis
    ax.set_ylabel("$H$ (Oe)", labelpad=10) # Label of y-axis
    ax.set_zlabel("$4\mathrm{\pi}\chi_{\mathrm{V}}$", labelpad=10) # Label of z-axis

    ax.legend(frameon=False, ncol=2)

    #plt.savefig("Sample_data/PPMS_PME/" + foldername + "_PME_3D.svg")
    plt.show()