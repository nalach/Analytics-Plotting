#!python
import os
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import numpy as np
import math

plt.style.use('sty-plot')

def parse_dat(file):
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
        

ppms_folder_path = os.path.join("Sample_data","PPMS")
folder_names = [foldername for foldername in os.listdir(ppms_folder_path) if not os.path.isfile(os.path.join(ppms_folder_path, foldername))]
folder_names.sort()

samples = []

for foldername in folder_names:
    sample_folder_path = os.path.join(ppms_folder_path, foldername)
    file_names = [filename for filename in os.listdir(sample_folder_path) if os.path.isfile(os.path.join(sample_folder_path, filename)) and filename.split('.')[-1] == 'DAT']
    
    isotherms = []
    zfc_fc = {}
    for filename in file_names:
        with open(os.path.join(sample_folder_path, filename), "r") as f:
            if "MVSH" in filename:
                file_content = parse_dat(f)
                temperature_legend = filename.split('_')[filename.split('_').index("MVSH")+1]
                isotherms.append({"temperature_legend": temperature_legend, "file_content": file_content})
            elif "ZFC" in filename:
                zfc_fc = parse_dat(f)
     
    samples.append({'sample_name': foldername, 'isotherms': isotherms, 'zfc_fc': zfc_fc})

for sample in samples:
    plt.figure(figsize=(8,6))
    ax = plt.axes()
    colors = ["red", "black"]
    i = 0

    for isotherm in sample['isotherms']:
        moment_korr = np.array(isotherm['file_content']['data'][2])-(1.48*(10**-7)-(9.06*(10**-9)*np.array(isotherm['file_content']['data'][1])))
        #y = moment_korr*isotherm['file_content']['molar_mass']/(isotherm['file_content']['mass']*6.02214076*9.2740100783*0.1)
        y = moment_korr*isotherm['file_content']['density']/(isotherm['file_content']['mass']/1000)
        x = np.array(isotherm['file_content']['data'][1])/1000

        if i == 0:
            isotherm_y_max = y.max()

        plt.plot(x, y, color = colors[i], label = isotherm['temperature_legend'], linewidth=1, marker='o', markersize=3, markeredgewidth=1)

        i =+ 1

    ax.set_xlabel("$H$ (kOe)")
    #ax.set_ylabel("$M$ ($\mu_{\mathrm{B}}$ / f.u.)")
    ax.set_ylabel("$M$ (Oe)")

    ax.xaxis.set_major_locator(ticker.MultipleLocator(10))
    ax.xaxis.set_minor_locator(ticker.MultipleLocator(5))

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

    # if isotherm_y_max < 10:
    #     plt.ylim(-10,10)
    #     ax.yaxis.set_major_locator(ticker.MultipleLocator(2))
    #     ax.yaxis.set_minor_locator(ticker.MultipleLocator(1))
    # elif isotherm_y_max < 30:
    #     #plt.ylim(-9,9)
    #     ax.yaxis.set_major_locator(ticker.MultipleLocator(4))
    #     ax.yaxis.set_minor_locator(ticker.MultipleLocator(2))
    # elif isotherm_y_max < 100:
    #     ax.yaxis.set_major_locator(ticker.MultipleLocator(20))
    #     ax.yaxis.set_minor_locator(ticker.MultipleLocator(10))
    # else:
    #     ax.yaxis.set_major_locator(ticker.MultipleLocator(100))
    #     ax.yaxis.set_minor_locator(ticker.MultipleLocator(50))

    plt.tight_layout()

    plt.savefig("Sample_data/PPMS/" + sample["sample_name"] + "_Isotherms.svg")
    plt.show()



    plt.figure(figsize=(8,6))
    ax = plt.axes()

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

    moment_korr = np.array(zfc_fc['data'][2])-(1.48*(10**-7)-(9.06*(10**-9)*np.array(zfc_fc['data'][1])))
    y = 4*math.pi*moment_korr*zfc_fc['density']/(zfc_fc['mass']/1000*np.array(zfc_fc['data'][1]))
    zfc_y = y[:index]
    fc_y = y[index:]

    magnetic_field = zfc_fc['data'][1][1]
    magnetic_field = round(magnetic_field)

    plt.plot(zfc_x, zfc_y, color = "red", label = "ZFC " + str(magnetic_field) + " Oe", linewidth=1, marker='o', markersize=3, markeredgewidth=1)
    plt.plot(fc_x, fc_y, color = "black", label = "FC " + str(magnetic_field) + " Oe", linewidth=1, marker='o', markersize=3, markeredgewidth=1)

    ax.set_xlabel("$T$ (K)")
    ax.set_ylabel("$4\mathrm{\pi}\chi_{\mathrm{V}}$")

    for i in range(len(zfc_x)):
        if zfc_x[i] > 20:
            break

    if zfc_y[i] < -0.1:
        plt.xlim(0,60)
        ax.xaxis.set_major_locator(ticker.MultipleLocator(10))
        ax.xaxis.set_minor_locator(ticker.MultipleLocator(5))
    else:
        plt.xlim(0,20)
        ax.xaxis.set_major_locator(ticker.MultipleLocator(2))
        ax.xaxis.set_minor_locator(ticker.MultipleLocator(1))

    if zfc_y.min() > -0.2:
        plt.ylim(-0.2,)
        ax.yaxis.set_major_locator(ticker.MultipleLocator(0.05))
        ax.yaxis.set_minor_locator(ticker.MultipleLocator(0.025))
    elif zfc_y.min() > -0.5:
        plt.ylim(-0.5,)
        ax.yaxis.set_major_locator(ticker.MultipleLocator(0.1))
        ax.yaxis.set_minor_locator(ticker.MultipleLocator(0.05))
    elif zfc_y.min() > -1:
        plt.ylim(-1,)
        ax.yaxis.set_major_locator(ticker.MultipleLocator(0.2))
        ax.yaxis.set_minor_locator(ticker.MultipleLocator(0.1))
    # elif zfc_y.min() > -1.5:
    #     ax.yaxis.set_major_locator(ticker.MultipleLocator(0.2))
    #     ax.yaxis.set_minor_locator(ticker.MultipleLocator(0.1))
    # elif zfc_y.min() > -2.5:
    #     ax.yaxis.set_major_locator(ticker.MultipleLocator(0.4))
    #     ax.yaxis.set_minor_locator(ticker.MultipleLocator(0.2))
    # else:
    #     ax.yaxis.set_major_locator(ticker.MultipleLocator(0.5))
    #     ax.yaxis.set_minor_locator(ticker.MultipleLocator(0.25))

    # ax.xaxis.set_major_locator(ticker.MultipleLocator(10))
    # ax.xaxis.set_minor_locator(ticker.MultipleLocator(5))
    # ax.yaxis.set_major_locator(ticker.MultipleLocator(0.2))
    # ax.yaxis.set_minor_locator(ticker.MultipleLocator(0.1))

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

    ax.legend(frameon=False, loc='lower right')

    # for i in range(len(zfc_x)):
    #     if zfc_x[i] > 20:
    #         break

    # if zfc_y[i] < -0.1:
    #     plt.xlim(0,100)
    # else:
    #     plt.xlim(0,20)

    # if zfc_y.min() > -1:
    #     plt.ylim(-1,)

    plt.savefig("Sample_data/PPMS/" + sample["sample_name"] + "_ZFC-FC.svg")
    plt.show()


    