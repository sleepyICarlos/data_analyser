# -*- coding: utf-8 -*-
"""
Created on Mon Nov 20 15:31:57 2017

@author: hartz
"""
import numpy as np
import os
import matplotlib.pyplot as plt

folder = "D:\documents\sciebo\ZnSe\M12-0084\IHT Probestation\D1\Stripes\data"
start_name = "3-2-18"
sample_name = "D1 "
structure_name= "Stripes"
save_name = "sample " + sample_name+ " 250° anneal "+structure_name
figure_comment ="sample "+ sample_name+ " Stripes" + "\n1 um ZnSe + 170 nm Al (ex-situ)\nAl+Cl doped\nafter annealing at 250°C, 3 min"
x_label="bias voltage (V)"
separator = "_"
file_identifier = structure_name
export_name = sample_name +" " + structure_name
end_name = ".txt" #"or ".dat"
save = True

files= []
pad_distance = []
values = []
resistances=[]
conductances=[]

#def read_data():
#    data=[], voltages=[]
measurement_counter = 0
measurement_description = []
for file in os.listdir(folder):
    if file.startswith(start_name):
        if file.endswith(end_name):
            contents = file.split(separator)    
            l = len(contents)
            measurement_counter += 1
            pad_distance_value = measurement_counter
            measurement_description.append(contents[l-2]+" "+ contents[l-1].split(".")[0])
            

            pad_distance.append(pad_distance_value)
            files.append(file)
            new_value=np.genfromtxt(folder+"\\"+file,usecols=0, skip_header=1).astype(float)
            new_value*= 1e9             #convert from mA to nA
            values.append(np.concatenate((np.array([pad_distance_value]),new_value)))       # skip_header: skips device names, usecol: uses 2nd column (current)

values.sort(key=lambda x: x[0])
#values=np.array(values)*1e6 #convert to nA 
pad_distance.sort()
print(files)
voltages = np.concatenate((np.array([0]),np.genfromtxt(folder+"\\"+files[0],usecols=1, skip_header = 1))) 
data = np.vstack((voltages,values))


#plotting
def plot(voltages, data_set, figure_comment, text_coordinates, label_coordinates):
    fig, ax = plt.subplots()
    for data_set in np.arange(len(files)):
        ax.plot(voltages[1:], values[data_set][1:], "-")
        
    ax.text(text_coordinates[0], text_coordinates[1],figure_comment)
    ax.text(label_coordinates[0], label_coordinates[1],"measurement nr.")
    ax.legend(measurement_description, loc = "lower right")
    #legend = ax.legend(loc="upper center", shadow=True, fontsize="x-large")
    plt.xlabel(x_label)
    plt.ylabel("current (nA)")
    ax.legend(measurement_description, loc = "lower right")
    if save:
        fig.savefig(save_name +"_all_data.pdf", format="pdf")
    
def plot_zoom(x_data, data, save_name, figure_comment, number_of_points, text_coordinates, label_coordinates, sweep_direction):
    fig, ax = plt.subplots()
    #define data, adjust number of points 
    number_of_points=int(number_of_points/2)
    if sweep_direction==0:    
        x_length = int(len(x_data)/4)
        x_index_1, x_index_2= x_length-number_of_points, x_length+number_of_points+3
        x=x_data[x_index_1:x_index_2]
        save_name+="_up_sweep"
        figure_comment+="\nup_sweep"
        for i in np.arange(len(data)-1):
            ax.plot(x, data[i+1][x_index_1:x_index_2], "-")
    else:
        x_length = int(len(x_data)*3/4)
        x_index_1, x_index_2= x_length-number_of_points-1, x_length+number_of_points+2
        x=x_data[x_index_1:x_index_2]
        save_name+="_down_sweep"
        figure_comment+="\ndown_sweep"        
        for i in np.arange(len(data)-1):
            ax.plot(x, data[i+1][x_index_1:x_index_2], "-")

    ax.text(text_coordinates[0], text_coordinates[1],figure_comment)
    ax.text(label_coordinates[0], label_coordinates[1],"pad distance (um)")
    ax.legend(pad_distance, loc = "lower right")
    #legend = ax.legend(loc="upper center", shadow=True, fontsize="x-large")
    plt.xlabel(x_label)
    plt.ylabel("current (nA)")
    #plt.title("ZnSe sample x.x")
    if save:
        fig.savefig(save_name +"_zoom.pdf", format="pdf")

def fit_linear_zoom(x_data, y_data, measurement_index, fit_points, sweep_direction):        #fit_points == number of fitpoints, # sweep_direction== 0, 1 for up and downsweep, respectively
    #fitting
    fit_points=int(fit_points/2)-1
    fig, ax = plt.subplots()
    #identify values around zero
    if sweep_direction==0:
        x_length = int(len(voltages)/4)
        x_index_1, x_index_2= x_length-fit_points, x_length+fit_points+3
    else:
        x_length = int(len(voltages)*3/4)
        x_index_1, x_index_2= x_length-fit_points-1, x_length+fit_points+2
    
    x=x_data[x_index_1:x_index_2]  #define data
    y=y_data[measurement_index][x_index_1:x_index_2]
    
    #linear fit through zero
    y_fit_parameters=np.polyfit(x, y, 1)
    slope=y_fit_parameters[0]
    y_fit= np.polyval(y_fit_parameters, x)
    ax.plot(x, y_fit, "-")
    ax.plot(x, y, "o")
     
    #labeling
    comment= "slope "+ str(round(slope, 5)) +" nA/V \n R = " + str(round(1/slope, 0)) +" GOhm"
    plt.title(save_name+", " +str(y_data[measurement_index][0]) + " um") 
    plt.text(0,-0.03, comment)
    plt.xlabel(x_label)
    plt.ylabel("current (nA)")
    if save:
        fig.savefig(save_name + str(y_data[measurement_index][0]) + " um"+"_lin_fit.pdf", format="pdf")
    return 1/slope


def fit_all_resistances(fit_points, resistances , conductances ,pad_distance):
    fit_points-=2
    resistances=[]
    conductances=[]
    for measurement in range(np.shape(data)[0]):
        if measurement>=1:
            R_up  = fit_linear_zoom(voltages, data, measurement, fit_points, 0)
            R_down= fit_linear_zoom(voltages, data, measurement, fit_points, 1)
            resistances.append(R_up)
            resistances.append(R_down)
            conductances.append(1/R_up)
            conductances.append(1/R_down)
    resistance_data=[]
    conductance_data=[]
    resistances= np.reshape(resistances, (len(pad_distance),2))
    conductances = np.reshape(conductances, (len(pad_distance), 2))
    pad_distance=np.transpose(pad_distance)
    resistance_data=np.vstack((pad_distance, np.transpose(resistances)))
    conductance_data=np.vstack((pad_distance, np.transpose(conductances)))
    #plot resistances
    fig, ax = plt.subplots()
    plt.xlabel("measurement nr.")
    plt.ylabel("resistance (GOhm)")
    ax.legend(measurement_description, loc = "lower right")
    plt.plot(resistance_data[1]),plt.plot(resistance_data[2])  
    return resistance_data, conductance_data
    
def plot_results(resistance_data, pad_distance):
    fig, ax = plt.subplots()
    ax.plot(resistance_data[0], resistance_data[1], "o")   
    ax.plot(resistance_data[0], resistance_data[2], "o")
    ax.legend(["up-sweep","down-sweep"], loc = "upper left")  
    plt.xlabel("measurement number") #plt.xlabel("contact spacing (um)")
    plt.ylabel("resistance (GOhm)")  
    plt.title(save_name+" resistances")
    if save:
        fig.savefig(save_name + "_resistances.pdf", format="pdf")
        
def plot_conductance_results(conductance_data, pad_distance):
    fig, ax = plt.subplots()
    ax.plot(conductance_data[0], conductance_data[1], "o")   
    ax.plot(conductance_data[0], conductance_data[2], "o")
    ax.legend(["up-sweep","down-sweep"], loc = "upper left")  
    plt.xlabel("measurement number") #plt.xlabel("contact spacing (um)")
    plt.ylabel("conductance (1/GOhm)")  
    plt.title(save_name+" conductances")
    if save:
        fig.savefig(save_name + "_conductances.pdf", format="pdf")  
        
       
def plot_I_max(conductance_data, data, pad_distance):
    fig, ax = plt.subplots()
    I_min = data.transpose()[1]
    I_max=data.transpose()[-1]
    I_max=(I_min+I_max)/2*-1
    I_max=I_max[1:]
    ax.plot(conductance_data[0], I_max, "o") 
    plt.xlabel("measurement number") #plt.xlabel("contact spacing (um)")
    plt.ylabel("averaged current at -10 V (nA)")  
    plt.title(save_name+" maximal current")
    if save:
        fig.savefig(save_name + "_maximal_current.pdf", format="pdf") 
        
       
def plot_I_max_normalized(conductance_data, data, pad_distance):
    fig, ax = plt.subplots()
    I_min = data.transpose()[1]
    I_max=data.transpose()[-1]
    I_max=(I_min+I_max)/2*-1
    I_max=I_max[1:]/I_max[1+1]
    ax.plot(conductance_data[0], I_max, "o") 
    plt.xlabel("measurement number") #plt.xlabel("contact spacing (um)")
    plt.ylabel("averaged current at -10 V (nA)")  
    plt.title(save_name+" maximal current")
    if save:
        fig.savefig(save_name + "_maximal_current.pdf", format="pdf") 
        
def plot_conductance_normalized(conductance_data, pad_distance):
    fig, ax = plt.subplots()
    ax.plot(conductance_data[0], conductance_data[1]/conductance_data[1][0], "o")   
    ax.plot(conductance_data[0], conductance_data[2]/conductance_data[1][0], "o")
    ax.legend(["up-sweep","down-sweep"], loc = "upper left")  
    plt.xlabel("measurement number") #plt.xlabel("contact spacing (um)")
    plt.ylabel("conductance (1/GOhm)")  
    plt.title(save_name+" conductances")
    if save:
        fig.savefig(save_name + "_conductances.pdf", format="pdf")  
        
def plot_all_normalized(conductance_data, data, pad_distance, norm_index, 
                        legend_txt, text_coordinates):  #norm_index mind 1, data == raw U-I data
    fig, ax = plt.subplots()
    
    # define data, select starting and ending points, average 2 values for 
    #I_min/I_max, define I_0, G_0 for normalizing the data
    I_min_1 = data.transpose()[1]
    I_min_2=data.transpose()[-1]
    I_min=(I_min_1+I_min_2)/2
    I_min=I_min[1:]
    I_0= np.abs(I_min[norm_index])
    I_min=np.abs(I_min_1[1:]/I_0)

    
    l=int(np.floor(np.shape(data)[1]/2))
    I_max_1 = data.transpose()[l]
    I_max_2=data.transpose()[l+1]
    I_max=(I_max_1+I_max_2)/2
    I_max=I_max[1:]
    I_max=I_max_1[1:]/I_0
    
    
    #normalizing
    I_min_norm_deviation=I_min/conductance_data[1]
    I_max_norm_deviation=I_max/conductance_data[2]
    I_min_norm_deviation=I_min_norm_deviation/np.average(I_min_norm_deviation)
    I_max_norm_deviation=I_max_norm_deviation/np.average(I_max_norm_deviation)
    
    G_0=conductance_data[1][norm_index]
    conversion_factor= I_0/G_0
    x=conductance_data[0]
    
    
    #plotting
    ax.plot(x, I_max, ".", x, I_min, ".")#, "o", "x") 
    ax.plot(conductance_data[0], conductance_data[1]/G_0, ".")   
    ax.plot(conductance_data[0], conductance_data[2]/G_0, ".")
    figure_comment = r'conversion factor = %d A * $\Omega$' % conversion_factor
    ax.text(text_coordinates[0], text_coordinates[1],figure_comment)
    ax.legend(legend_txt, loc = "upper left")  
    plt.xlabel("measurement number") #plt.xlabel("contact spacing (um)")
    plt.ylabel("current, conductance (normalized)")  
    plt.title(save_name+"\nI, G normalized")
    if save:
        fig.savefig(save_name + "_I_G_norm.pdf", format="pdf")  
        
def save_data():
    np.savetxt(export_name+"_conductances.csv", conductance_data)
    np.savetxt(export_name+"_data.csv",data)
    np.savetxt(export_name+"_resistances.csv",resistance_data)

  
plot(voltages, data, figure_comment, [-5,1], [0, -1])
plot_zoom(voltages, data, save_name, figure_comment, 5,  [-0.4,0], [0, 0], 1)
plot_zoom(voltages, data, save_name, figure_comment, 5,  [-0.4,0], [0, 0], 0)
resistance_data, conductance_data =fit_all_resistances(15, resistances, conductances, pad_distance)
plot_results(resistance_data, pad_distance)
plot_conductance_results(conductance_data, pad_distance)
plot_conductance_normalized(conductance_data, pad_distance)
plot_I_max(conductance_data, data, pad_distance)
plot_I_max_normalized(conductance_data, data, pad_distance)
plot_all_normalized(conductance_data, data, pad_distance, 18, ["|I$_\mathrm{min}$|", "|I$_\mathrm{max}$|", "G, up-sweep","G, down-sweep"], [0,0])
#plot_all_normalized(conductance_data, data, pad_distance, 18)
if save:
    save_data()
