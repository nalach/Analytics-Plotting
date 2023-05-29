#!python
import os
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
#from adjustText import adjust_text

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
        c_a_ratio = []
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
        c_a_ratio = [x/y for x, y in zip(lat_c, lat_a)]
        if synth_method != []:
            subst_rows = {'file_name': file_name, 'row_name': row_name, 'sample_index': sample_index, 'sample_intended': sample_intended, 'x_subst': x_subst, 'method': synth_method, 'lat_a': lat_a, 'lat_c': lat_c, 'c_a_ratio': c_a_ratio, 'lat_vol': lat_vol}
        else:
            subst_rows = {'file_name': file_name, 'row_name': row_name, 'sample_index': sample_index, 'sample_intended': sample_intended, 'x_subst': x_subst, 'lat_a': lat_a, 'lat_c': lat_c, 'c_a_ratio': c_a_ratio, 'lat_vol': lat_vol}
        substitutions.append(subst_rows)

# --------------------------------------------------------------
# calculate, plot and output composition
for substitution in substitutions:
    # determine y-values for plots
    param_list = ['lat_a', 'lat_c', 'c_a_ratio', 'lat_vol']
    param_x_values_dict = {}
    for param in param_list:
        # --------------------------------------------------------------
        # calculate linear function, determine and save composition
        slope = (substitution[param][-1] - substitution[param][0]) / (substitution['x_subst'][-1] - substitution['x_subst'][0])
        y_val = substitution[param][0] - slope * substitution['x_subst'][0]

        # determine and save composition
        param_x_values = []
        for element in substitution[param]:
            x_value = (element - y_val) / slope
            x_value = round(x_value, 2)
            param_x_values.append(x_value)
        param_x_values_dict[param] = param_x_values


        # plot determined composition        
        plt.figure(figsize=(8,6))
        #plt.figure()
        ax = plt.axes()

        if 'method' in substitution:
            color_method = method_color(substitution['method'])
            scatter = plt.scatter(param_x_values_dict[param], substitution[param], c=color_method['values'], cmap=color_method['colors'], s=50)
            if (substitution[param][-1]-substitution[param][0]) < 0:
                plt.legend(handles=scatter.legend_elements()[0], labels=color_method['classes'], fontsize=15, frameon=False, markerscale=0.7, bbox_to_anchor=(0.02, 0.02), loc='lower left')
            else:
                plt.legend(handles=scatter.legend_elements()[0], labels=color_method['classes'], fontsize=15, frameon=False, markerscale=0.7, bbox_to_anchor=(0.02, 0.98), loc='upper left')
            #plt.legend(handles=scatter.legend_elements()[0], labels=color_method['classes'], fontsize=15, frameon=False, markerscale=0.7, bbox_to_anchor=(0.02, 0.02), loc='lower left')
            # for x, y, c, method_title in zip(param_x_values_dict[param], substitution[param], colors, substitution['method']):
            #     plt.scatter(x, y, color=c, label=method_title)
            # ax.legend()
        else:
            scatter = plt.scatter(param_x_values_dict[param], substitution[param], c='blue', s=50)
            #plt.plot(param_x_values_dict[param], substitution[param], color = "blue", marker='o', markersize=8, markeredgewidth=1, linestyle='none')
        plt.plot([param_x_values_dict[param][0], param_x_values_dict[param][-1]], [substitution[param][0], substitution[param][-1]], color='black', linewidth=1)

        plt.title(substitution['row_name'], fontsize=24, weight='bold')
        ax.set_xlabel("$x_{det}$") # Label of x-axis
        if param == 'lat_a': # Label of y-axis
            ax.set_ylabel("$a$ ($\mathrm{\AA}$)") 
        elif param == 'lat_c':
            ax.set_ylabel("$c$ ($\mathrm{\AA}$)")
        elif param == 'c_a_ratio':
            ax.set_ylabel("$c/a$")
        elif param == 'lat_vol':
            ax.set_ylabel("$V$ ($\mathrm{\AA}^3$)")

        i = 0
        for x, y in zip(param_x_values_dict[param], substitution[param]):
            plt.annotate(substitution['sample_index'][i], (x,y), textcoords="offset points", xytext=(8,0), fontsize=10)
            # if 'method' in substitution:
            #     plt.annotate(substitution['method'][i], (x,y), textcoords="offset points", xytext=(8,-10), fontsize=10)
            i += 1
        # texts = []
        # for x, y, s in zip(param_x_values_dict[param], substitution[param], substitution['sample_index']):
        #     texts.append(plt.text(x, y, s))
        # adjust_text(texts, arrowprops=dict(arrowstyle="->", color='r', lw=0.5))

        plt.savefig(os.path.join("Sample_data","Lattice_parameters", "Determined", substitution['file_name'] + '_' + param + '.svg'))
        plt.show()
    
    # --------------------------------------------------------------
    # output determined compositions
    with open(os.path.join("Sample_data","Lattice_parameters", "Determined", substitution['file_name'] + '_Determined.csv'), 'w') as f:
        f.write('Sample;x_' + param_list[0] + ';x_' + param_list[1] + ';x_' + param_list[2] + ';x_' + param_list[3] + '\n')
        i = 0
        for i in range(len(param_x_values_dict[param_list[0]])):
            line = substitution['sample_index'][i] + ';' + str(param_x_values_dict[param_list[0]][i]) + ';' + str(param_x_values_dict[param_list[1]][i]) + ';' + str(param_x_values_dict[param_list[2]][i]) + ';' + str(param_x_values_dict[param_list[3]][i]) + '\n'
            f.write(line)

    