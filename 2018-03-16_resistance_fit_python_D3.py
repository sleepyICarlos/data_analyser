# -*- coding: utf-8 -*-
'''
Created on Mon Nov 20 15:31:57 2017

@author: hartz
'''
import numpy as np
import os
import matplotlib.pyplot as plt

folder = '\\janeway\User AG Bluhm\Hartz\sciebo\promotion\6_LogsDataAnalysis\1_data\IHT_probe_station\2018-03-15_photocurrent_experiments\D3\Areas'
start_name = 'D3'
structure_name= 'Areas'
save_name = 'sample ' + sample_name+ ' 350° anneal '+structure_name
figure_comment ='sample '+ sample_name+ structure_name + '\n1 um ZnSe 44nm Al in-situ\n Al+Cl doped\nbefore annealing at 250°C, 3 min'
x_label='bias voltage (V)'
separator = '_'
file_identifier = 'Areas'
export_name = sample_name +' ' + structure_name
end_name = '.txt' #'or '.dat'

files= []
pad_distance = []
values = []
resistances=[]

#def read_data():
#    data=[], voltages=[]
for file in os.listdir(folder):
    if file.endswith(end_name):
            contents = file.split(separator)       
            for i in np.arange(len(contents)):
                if contents[i] == file_identifier:
                    pad_distance_value = int(contents[i+1])
                    break

            pad_distance.append(pad_distance_value)
            files.append(file)
            new_value=np.genfromtxt(folder+'\\'+file,usecols=1, skip_header=2).astype(float)
            new_value*= 1e6             #convert from mA to nA
            values.append(np.concatenate((np.array([pad_distance_value]),new_value)))       # skip_header: skips device names, usecol: uses 2nd column (current)

values.sort(key=lambda x: x[0])
#values=np.array(values)*1e6 #convert to nA 
pad_distance.sort()
voltages = np.concatenate((np.array([0]),np.genfromtxt(folder+'\\'+files[0],usecols=0, skip_header = 2))) 
data = np.vstack((voltages,values))


#plotting
def plot(voltages, data_set, figure_comment, text_coordinates, label_coordinates):
    fig, ax = plt.subplots()
    for data_set in np.arange(len(files)):
        ax.plot(voltages[1:], values[data_set][1:], '-')
        
    ax.text(text_coordinates[0], text_coordinates[1],figure_comment)
    ax.text(label_coordinates[0], label_coordinates[1],'measurement nr.')
    ax.legend(pad_distance, loc = 'lower right')
    #legend = ax.legend(loc='upper center', shadow=True, fontsize='x-large')
    plt.xlabel(x_label)
    plt.ylabel('current (nA)')
    fig.savefig(save_name +'_all_data.pdf', format='pdf')
    
def plot_zoom(x_data, data, save_name, figure_comment, number_of_points, text_coordinates, label_coordinates, sweep_direction):
    fig, ax = plt.subplots()
    #define data, adjust number of points 
    number_of_points=int(number_of_points/2)
    if sweep_direction==0:    
        x_length = int(len(x_data)/4)
        x_index_1, x_index_2= x_length-number_of_points, x_length+number_of_points+3
        x=x_data[x_index_1:x_index_2]
        save_name+='_up_sweep'
        figure_comment+='\nup_sweep'
        for i in np.arange(len(data)-1):
            ax.plot(x, data[i+1][x_index_1:x_index_2], '-')
    else:
        x_length = int(len(x_data)*3/4)
        x_index_1, x_index_2= x_length-number_of_points-1, x_length+number_of_points+2
        x=x_data[x_index_1:x_index_2]
        save_name+='_down_sweep'
        figure_comment+='\ndown_sweep'        
        for i in np.arange(len(data)-1):
            ax.plot(x, data[i+1][x_index_1:x_index_2], '-')

    ax.text(text_coordinates[0], text_coordinates[1],figure_comment)
    ax.text(label_coordinates[0], label_coordinates[1],'pad distance (um)')
    ax.legend(pad_distance, loc = 'lower right')
    #legend = ax.legend(loc='upper center', shadow=True, fontsize='x-large')
    plt.xlabel(x_label)
    plt.ylabel('current (nA)')
    #plt.title('ZnSe sample x.x')
    fig.savefig(save_name +'_zoom.pdf', format='pdf')

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
    ax.plot(x, y_fit, '-')
    ax.plot(x, y, 'o')
     
    #labeling
    comment= 'slope '+ str(round(slope, 5)) +' nA/V \n R = ' + str(round(1/slope, 0)) +' GOhm'
    plt.title(save_name+', ' +str(y_data[measurement_index][0]) + ' um') 
    plt.text(0,-0.03, comment)
    plt.xlabel(x_label)
    plt.ylabel('current (nA)')
    fig.savefig(save_name + str(y_data[measurement_index][0]) + ' um'+'_lin_fit.pdf', format='pdf')
    return 1/slope


def fit_all_resistances(fit_points, resistances ,pad_distance):
    fit_points-=2
    resistances=[]
    for measurement in range(np.shape(data)[0]):
        if measurement>=1:
            resistances.append(fit_linear_zoom(voltages, data, measurement, fit_points, 0))
            resistances.append(fit_linear_zoom(voltages, data, measurement, fit_points, 1))
    resistance_data=[]
    resistances= np.reshape(resistances, (len(pad_distance),2))
    pad_distance=np.transpose(pad_distance)
    resistance_data=np.vstack((pad_distance, np.transpose(resistances)))
    #plot resistances
    fig, ax = plt.subplots()
    plt.xlabel('measurement nr.')
    plt.ylabel('resistance (GOhm)')
    plt.plot(resistance_data[1]),plt.plot(resistance_data[2])  
    return resistance_data
    
def plot_results(resistance_data, pad_distance):
    fig, ax = plt.subplots()
    ax.plot(resistance_data[0], resistance_data[1], 'o')   
    ax.plot(resistance_data[0], resistance_data[2], 'o')
    #ax.legend(up_sweep, down_sweep, loc = 'lower right')    
    plt.xlabel('contact spacing (um)')
    plt.ylabel('resistance (GOhm)')  
    plt.title(save_name+' resistances')
    fig.savefig(save_name + '_resistances.pdf', format='pdf')

plot(voltages, data, figure_comment, [-5,1], [0, -1])
plot_zoom(voltages, data, save_name, figure_comment, 5,  [-0.4,0], [0, 0], 1)
plot_zoom(voltages, data, save_name, figure_comment, 5,  [-0.4,0], [0, 0], 0)
resistance_data=fit_all_resistances(15, resistances, pad_distance)
plot_results(resistance_data, pad_distance)

np.savetxt(export_name+'_data.csv',data)
np.savetxt(export_name+'_resistances.csv',resistance_data)