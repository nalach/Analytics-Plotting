#!python
import os
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap

plt.style.use('sty-plot')

# --------------------------------------------------------------
# coloring of scatter plot depending on synthesis method
def method_color(methods):
    values = []
    classes = []
    colors_list = []
    for method in methods:
        if method == "CVT":
            values.append(0)
            if 'CVT' not in classes:
                classes.append('CVT')
            if 'red' not in colors_list:
                colors_list.append('red')
        elif method == "Hydroth":
            values.append(1)
            if 'Hydrothermal' not in classes:
                classes.append('Hydrothermal')
            if 'blue' not in colors_list:
                colors_list.append('blue')
        elif method == "K-Deint":
            values.append(2)
            if 'K Deintercalation' not in classes:
                classes.append('K Deintercalation')
            if 'green' not in colors_list:
                colors_list.append('green')
        elif method =="Festk":
            values.append(3)
            if 'Solid State Synthesis' not in classes:
                classes. append('Solid State Synthesis')
            if 'blue' not in colors_list:
                colors_list.append('blue')
    #classes = ['CVT', 'Hydrothermal', 'K Deintercalation', 'Solid State Synthesis']
    #colors = ListedColormap(['red', 'green', 'blue', 'green'])
    colors = ListedColormap(colors_list)
    return {'values': values, 'classes': classes, 'colors': colors}


# --------------------------------------------------------------
# path of data and data handling
lat_param_folder_path = os.path.join("Sample_data","Lattice_parameters")
file_names = [filename for filename in os.listdir(lat_param_folder_path) if os.path.isfile(os.path.join(lat_param_folder_path, filename)) and filename.split('.')[-1] == 'csv']
file_names.sort()

substitutions = []

for filename in file_names:
    subst_rows = {}
    with open(os.path.join(lat_param_folder_path, filename), "r") as f:
        row_name = ""
        sample_index = []
        sample_intended = []
        x_index = 0
        a_index = 0
        c_index = 0
        vol_index = 0
        method_index = 0
        x_subst = []
        lat_a = []
        lat_c = []
        lat_vol = []
        synth_method = []
        file_name = filename.split('_')[0]
        for line in f:
            line = line[:-1]
            line_elements = []
            if len(line.split(";")) > 1:
                line_elements = line.split(";")
            elif len(line.split(",")) > 1:
                line_elements = line.split(",")
            else:
                row_name = line
                continue
            if line_elements[0] == "sample":
                i = 0
                for element in line_elements:
                    if element == "x":
                        x_index = i
                    elif element == "method":
                        method_index = i
                    elif element == "a":
                        a_index = i
                    elif element == "c":
                        c_index = i
                    elif element == "volume":
                        vol_index = i
                    i += 1
                continue
            else:
                sample_info = line_elements[0]
                if sample_info.split(".")[-1] == "inp":
                    sample_info = sample_info.split(".")[0]
                if sample_info.split("_")[1].isdigit():
                    sample_index.append("_".join(sample_info.split("_")[0:2]))
                    sample_intended.append("_".join(sample_info.split("_")[2:]))
                else:
                    sample_index.append(sample_info.split("_")[0])
                    sample_intended.append("_".join(sample_info.split("_")[1:]))
                if method_index > 0:
                    synth_method.append(line_elements[method_index])
                x_subst.append(float(line_elements[x_index]))
                lat_a.append(float(line_elements[a_index]))
                lat_c.append(float(line_elements[c_index]))
                lat_vol.append(float(line_elements[vol_index]))
        if synth_method != []:
            subst_rows = {'file_name': file_name, 'row_name': row_name, 'sample_index': sample_index, 'sample_intended': sample_intended, 'x_subst': x_subst, 'method': synth_method, 'lat_a': lat_a, 'lat_c': lat_c, 'lat_vol': lat_vol}
        else:
            subst_rows = {'file_name': file_name, 'row_name': row_name, 'sample_index': sample_index, 'sample_intended': sample_intended, 'x_subst': x_subst, 'lat_a': lat_a, 'lat_c': lat_c, 'lat_vol': lat_vol}
        substitutions.append(subst_rows)


# --------------------------------------------------------------
# plotting of different lattice parameters
for substitution in substitutions:
    if 'method' in substitution:
        color_method = method_color(substitution['method'])

    # --------------------------------------------------------------
    # lattice parameter a
    plt.figure(figsize=(8,6))
    ax = plt.axes()

    if 'method' in substitution:
        scatter = plt.scatter(substitution['x_subst'], substitution['lat_a'], c=color_method['values'], cmap=color_method['colors'], s=50)
        if (substitution['lat_a'][-1]-substitution['lat_a'][0]) < 0:
            plt.legend(handles=scatter.legend_elements()[0], labels=color_method['classes'], fontsize=15, frameon=False, markerscale=0.7, bbox_to_anchor=(0.02, 0.02), loc='lower left')
        else:
            plt.legend(handles=scatter.legend_elements()[0], labels=color_method['classes'], fontsize=15, frameon=False, markerscale=0.7, bbox_to_anchor=(0.02, 0.98), loc='upper left')
        # for x, y, c, method_title in zip(substitution['x_subst'], substitution['lat_a'], colors, substitution['method']):
        #     plt.scatter(x, y, color=c, label=method_title)
        # ax.legend()
    else:
        scatter = plt.scatter(substitution['x_subst'], substitution['lat_a'], c='blue', s=50)
        #plt.plot(substitution['x_subst'], substitution['lat_a'], color = "blue", marker='o', markersize=8, markeredgewidth=1, linestyle='none')
    plt.plot([substitution['x_subst'][0], substitution['x_subst'][-1]], [substitution['lat_a'][0], substitution['lat_a'][-1]], color='black', linewidth=1)

    plt.title(substitution['row_name'], fontsize=24, weight='bold')
    ax.set_xlabel("$x_{nom}$") # Label of x-axis
    ax.set_ylabel("$a$ ($\mathrm{\AA}$)") # Label of y-axis

    i = 0
    for x, y in zip(substitution['x_subst'], substitution['lat_a']):
        plt.annotate(substitution['sample_index'][i], (x,y), textcoords="offset points", xytext=(8,0), fontsize=10)
        # if 'method' in substitution:
        #     plt.annotate(substitution['method'][i], (x,y), textcoords="offset points", xytext=(8,-10), fontsize=10)
        i += 1

    plt.savefig(os.path.join("Sample_data","Lattice_parameters", substitution['file_name'] + '_' + 'a' + '.svg'))
    plt.show()

    # --------------------------------------------------------------
    # lattice parameter c
    plt.figure(figsize=(8,6))
    ax = plt.axes()

    if 'method' in substitution:
        scatter = plt.scatter(substitution['x_subst'], substitution['lat_c'], c=color_method['values'], cmap=color_method['colors'], s=50)
        if (substitution['lat_c'][-1]-substitution['lat_c'][0]) < 0:
            plt.legend(handles=scatter.legend_elements()[0], labels=color_method['classes'], fontsize=15, frameon=False, markerscale=0.7, bbox_to_anchor=(0.02, 0.02), loc='lower left')
        else:
            plt.legend(handles=scatter.legend_elements()[0], labels=color_method['classes'], fontsize=15, frameon=False, markerscale=0.7, bbox_to_anchor=(0.02, 0.98), loc='upper left')
    else:
        scatter = plt.scatter(substitution['x_subst'], substitution['lat_c'], c='blue', s=50)
    plt.plot([substitution['x_subst'][0], substitution['x_subst'][-1]], [substitution['lat_c'][0], substitution['lat_c'][-1]], color='black', linewidth=1)

    plt.title(substitution['row_name'], fontsize=24, weight='bold')
    ax.set_xlabel("$x_{nom}$") # Label of x-axis
    ax.set_ylabel("$c$ ($\mathrm{\AA}$)") # Label of y-axis

    i = 0
    for x, y in zip(substitution['x_subst'], substitution['lat_c']):
        plt.annotate(substitution['sample_index'][i], (x,y), textcoords="offset points", xytext=(8,0), fontsize=10)
        i += 1

    plt.savefig(os.path.join("Sample_data","Lattice_parameters", substitution['file_name'] + '_' + 'c' + '.svg'))
    plt.show()

    # --------------------------------------------------------------
    # ratio c:a
    plt.figure(figsize=(8,6))
    ax = plt.axes()

    c_a_ratio = [x/y for x, y in zip(substitution['lat_c'], substitution['lat_a'])]

    if 'method' in substitution:
        scatter = plt.scatter(substitution['x_subst'], c_a_ratio, c=color_method['values'], cmap=color_method['colors'], s=50)
        if (c_a_ratio[-1]-c_a_ratio[0]) < 0:
            plt.legend(handles=scatter.legend_elements()[0], labels=color_method['classes'], fontsize=15, frameon=False, markerscale=0.7, bbox_to_anchor=(0.02, 0.02), loc='lower left')
        else:
            plt.legend(handles=scatter.legend_elements()[0], labels=color_method['classes'], fontsize=15, frameon=False, markerscale=0.7, bbox_to_anchor=(0.02, 0.98), loc='upper left')
    else:
        scatter = plt.scatter(substitution['x_subst'], c_a_ratio, c='blue', s=50)
    plt.plot([substitution['x_subst'][0], substitution['x_subst'][-1]], [c_a_ratio[0], c_a_ratio[-1]], color='black', linewidth=1)

    plt.title(substitution['row_name'], fontsize=24, weight='bold')
    ax.set_xlabel("$x_{nom}$") # Label of x-axis
    ax.set_ylabel("$c/a$") # Label of y-axis

    i = 0
    for x, y in zip(substitution['x_subst'], c_a_ratio):
        plt.annotate(substitution['sample_index'][i], (x,y), textcoords="offset points", xytext=(8,0), fontsize=10)
        i += 1

    plt.savefig(os.path.join("Sample_data","Lattice_parameters", substitution['file_name'] + '_' + 'c-a' + '.svg'))
    plt.show()

    # --------------------------------------------------------------
    # Volume V
    plt.figure(figsize=(8,6))
    ax = plt.axes()

    if 'method' in substitution:
        scatter = plt.scatter(substitution['x_subst'], substitution['lat_vol'], c=color_method['values'], cmap=color_method['colors'], s=50)
        if (substitution['lat_vol'][-1]-substitution['lat_vol'][0]) < 0:
            plt.legend(handles=scatter.legend_elements()[0], labels=color_method['classes'], fontsize=15, frameon=False, markerscale=0.7, bbox_to_anchor=(0.02, 0.02), loc='lower left')
        else:
            plt.legend(handles=scatter.legend_elements()[0], labels=color_method['classes'], fontsize=15, frameon=False, markerscale=0.7, bbox_to_anchor=(0.02, 0.98), loc='upper left')
    else:
        scatter = plt.scatter(substitution['x_subst'], substitution['lat_vol'], c='blue', s=50)
    plt.plot([substitution['x_subst'][0], substitution['x_subst'][-1]], [substitution['lat_vol'][0], substitution['lat_vol'][-1]], color='black', linewidth=1)

    plt.title(substitution['row_name'], fontsize=24, weight='bold')
    ax.set_xlabel("$x_{nom}$") # Label of x-axis
    ax.set_ylabel("$V$ ($\mathrm{\AA}^3$)") # Label of y-axis

    i = 0
    for x, y in zip(substitution['x_subst'], substitution['lat_vol']):
        plt.annotate(substitution['sample_index'][i], (x,y), textcoords="offset points", xytext=(8,0), fontsize=10)
        i += 1

    plt.savefig(os.path.join("Sample_data","Lattice_parameters", substitution['file_name'] + '_' + 'vol' + '.svg'))
    plt.show()