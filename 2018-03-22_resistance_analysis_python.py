# -*- coding: utf-8 -*-
"""
Created on Mon Nov 20 15:31:57 2017

@author: hartz
"""
import numpy as np
import os
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
from numpy.polynomial.polynomial import polyval

"""this script is optimized for reading in data taken from hysteretic sweeps taken with IHT Probe station, 
402 data points in total (201 per sweep direction, 0.1 V spacing)"""


D1_data_folder = "D:\documents\sciebo\ZnSe\M12-0084\IHT Probestation\D1\Stripes\data" #path for home office, for D1
D2_data_folder = "D:\documents\sciebo\ZnSe\M12-0084\IHT Probestation\D2\Stripes\data" #path for home office, for D1
D4_data_folder = "D:\documents\sciebo\ZnSe\M12-0084\IHT Probestation\D4\Stripes\data" #path for home office, for D1
D6_data_folder = "D:\documents\sciebo\ZnSe\M12-0084\IHT Probestation\D6\Stripes\data"
#"Z:\sciebo\ZnSe\M12-0084\IHT Probestation\D1\Stripes\data" #path for office
save_folder = "Z:\sciebo\promotion\6_LogsDataAnalysis\1_data\IHT_probe_station\0084\doped_stripes\python"

start_name = "7-3-18"
sample_name = "D "
structure_name= "Stripes"
save_name = "sample " + sample_name+ " 250° anneal "+structure_name
figure_comment ="sample "+ sample_name+ " Stripes" + "\n1 $\mu$m ZnSe + 170 nm Al ($ex-situ$)\nAl+Cl doped\nafter annealing at 250°C for 3 min"
x_label="bias voltage (V)"
y_label="photocurrent (nA)"
separator = "_"
file_identifier = structure_name
export_name = sample_name +" " + structure_name
end_name = ".txt" #or ".dat"
plot_fit_output= False
save = False
#%%
"""data import
generates a data struct with all available information on data poits
in 3 dim space (x,y, +one z per x,y data set)"""

def import_data(folder):
    data, voltages, values, zdata, files =[], [], [], [], []     #pad distance: any param read from file name
    measurement_counter = 0
    measurement_description = []
    for file in os.listdir(folder):
        #if file.startswith(start_name):
            if file.endswith(end_name):
                contents = file.split(separator)    
                l = len(contents)
                measurement_counter += 1
                zdata_value = measurement_counter
                measurement_description.append(contents[l-2]+" "+ contents[l-1].split(".")[0])
                
    
                zdata.append(zdata_value)
                files.append(file)
                new_value=np.genfromtxt(folder+"\\"+file,usecols=0, skip_header=1).astype(float)
                new_value*= 1e9             #convert from mA to nA
                values.append(np.concatenate((np.array([zdata_value]),new_value)))       # skip_header: skips device names, usecol: uses 2nd column (current)
    
    values.sort(key=lambda x: x[0])
    #values=np.array(values)*1e6 #convert to nA 
    zdata.sort()
    file_list = files
    print("%d files imported successfully:" %(len(files)) )
    print(files)
    voltages = np.concatenate((np.array([0]),np.genfromtxt(folder+"\\"+files[0],usecols=1, skip_header = 1))) 
    data = np.vstack((voltages,values))
    data_labels= measurement_description
    return data, file_list, data_labels

#%% #plotting
def plot(data, data_labels, axes_labels = ["x_param (X)", "y_param (Y)"], text_pos=[-10, 40]):
    fig, ax = plt.subplots()
    ax.set_ylabel(axes_labels[0]), ax.set_xlabel(axes_labels[1])
    x=data[0][1:]  
    ax.text(text_pos[0], text_pos[1], figure_comment)
    for i in np.arange(len(data)-1):
        ax.plot(x, data[i+1][1:], "-", linewidth=0.5)
        ax.legend(data_labels, fontsize=6, loc = "best")
    
    plt.title(save_name)
        
    if save:
        fig.savefig(save_name +"_data.pdf", format="pdf")
        

#%%
def plot_zoom(data, number_of_points, sweep_direction, legend="", text_coordinates=[-1, 0.05]):
    fig, ax = plt.subplots()
    #define data, adjust number of points for up- down sweep resp.
    x=data[0][1:]
    l = int(number_of_points/2)
    if sweep_direction==0:    
        x_0 = int(len(x)/4)+1
    else:
        x_0 = int(len(x)*3/4)+1
    x_1 = int(x_0-l-1)
    x_2= int(x_0+l)
    x=x[x_1:x_2]
    for i in np.arange(len(data)-1):
        ax.plot(x, data[i+1][x_1:x_2], "-", linewidth=0.5)

    #labeling
    if sweep_direction==0:
        zoom_save_name= save_name + "_up-sweep"
        comment= figure_comment+"\nup-sweep"
    else:
        zoom_save_name= save_name + "_down-sweep"
        comment= figure_comment+"\ndown_sweep" 

    ax.text(text_coordinates[0], text_coordinates[1], comment)
    ax.legend(legend, loc = "lower right")
    ax.set_xlabel(x_label)
    ax.set_ylabel("current (nA)")
    #plt.title("ZnSe sample x.x")
    if save:
        fig.savefig(zoom_save_name +"_zoom.pdf", format="pdf")

#%% data analysis
""" my fitting function for extracting the slope around 0 V,
polynomial of deg 3."""

def poly_3(x, a, b, c, d):
    result = a * x**3 + b*x**2 +c*x +d
    return result

def poly_5(x, a, b, c, d, e, f):
    result = a * x**5 + b*x**4 +c * x**3 + d*x**2 +e*x +f
    return result

def poly_7(x, a, b, c, d, e, f, g, h):
    result = a * x**7 + b*x**6 +c * x**5 + d*x**4 +e * x**3 + f*x**2 +g*x +h
    return result

class func():
    def __init__(self, name, degree):
        self.name = name
        self.degree = degree
        
    def _return(self):
        return polyval(self.x, self.coeff)

def set_func(N):#comment: eventually I could also use polynomial from a library
    #, if implemented correctly
    if N== 3:
        return poly_3
    if N==5:
        return poly_5
    if N==7:
        return poly_7
#%% 
    
"""fits my fit function to the data, returns data which is called by
'compute_conductances(...)' later."""
def fit_with_errors(data, fit_deg, i_data, fit_points, sweep_direction, legend, output = plot_fit_output):        #fit_points == number of fitpoints, # sweep_direction== 0, 1 for up and downsweep, respectively
    #fitting
    fit_points=int(fit_points/2)-1
    voltages=data[0][1:]
    #identify values around 0 V
    if sweep_direction==0:
        x_length = int(len(voltages)/4+1)
        x_index_1, x_index_2= x_length-fit_points, x_length+fit_points
    else:
        x_length = int(len(voltages)*3/4)
        x_index_1, x_index_2= x_length-fit_points-1, x_length+fit_points+2
    
    x=voltages[x_index_1:x_index_2]  #define data
    y=data[i_data][x_index_1:x_index_2]
    
    func = set_func(fit_deg)
    popt, pcov = curve_fit(func, x, y)
    
    perr = np.sqrt(np.diag(pcov))
    slope, slope_error =popt[2], perr[2]#to do , N-1 for poly_N
    #plotting
    if output:
        fig, ax = plt.subplots()
        ax.plot(x, func(x, *popt), "g-", label = "fit")
        ax.plot(x, y, "b.", label = "y-data")
        ax.legend(loc="best")
        comment= "slope "+ str(round(slope, 5)) +" nA/V \n R = " + str(round(1/slope, 0)) +" G$\Omega$"
        i_label=int(data[i_data][0])-1
        print("label_index %d"  %(i_label))
        plt.title(save_name+", " +legend[i_label]) 
        plt.text(0,0, comment)
        ax.set_xlabel(x_label)
        ax.set_ylabel("current (nA)")
        plt.show()
        
        if save:
            fig.savefig(save_name + legend[i_label] + "_lin_fit.pdf", format="pdf")
            
    return slope, slope_error


#%% 
def process_data(data, fit_deg, fit_points, legend, axes_labels = ["x_param (X)", "y_param (Y)"], output = False):
    z=data.transpose()[0][1:]
    R=[]
    R_err= []
    slope=[]    #conductance here
    slope_err =[]
    for i in range(np.shape(data)[0]):
        if i>=1:
            slope_up  =  fit_with_errors(data, fit_deg, i, fit_points, 0, legend, output)
            slope_down = fit_with_errors(data, fit_deg, i, fit_points, 1, legend, output)
            R.append(np.abs(1/slope_up[0]))
            R.append(np.abs(1/slope_down[0]))
            R_err.append(np.abs(1/slope_up[0]**2*slope_up[1]))
            R_err.append(np.abs(1/slope_down[0]**2*slope_down[1]))
            slope.append(slope_up[0])
            slope.append(slope_down[0])
            slope_err.append(slope_up[1])
            slope_err.append(slope_down[1])

    #reshape variables
    R= np.reshape(R, (len(z),2))
    R_err= np.reshape(R_err, (len(z),2))
    slope = np.reshape(slope, (len(z), 2))
    slope_err= np.reshape(slope_err, (len(z),2))
    
    z=np.transpose(z)
    R=np.vstack((z, np.transpose(R)))
    R_err=np.vstack((z, np.transpose(R_err)))
    slope=np.vstack((z, np.transpose(slope)))
    slope_err=np.vstack((z, np.transpose(slope_err)))
    
    #plot resistances
    if output:
        fig, ax = plt.subplots()
        ax.set_xlabel(axes_labels[0])
        ax.set_ylabel(axes_labels[1])
        ax.legend(legend, loc = "lower right")
        plt.plot(R[1], ".", label="up-sweep"),plt.plot(R[2], ".", label="down-sweep")  
    
    return R , R_err, slope, slope_err
        
#%% 
def plot_I_max(conductance_data, data, zdata):
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
#%%               
#def plot_I_max_normalized(conductance_data, data, zdata):
#    fig, ax = plt.subplots()
#    I_min = data.transpose()[1]
#    I_max=data.transpose()[-1]
#    I_max=(I_min+I_max)/2*-1
#    I_max=I_max[1:]/I_max[1+1]
#    ax.plot(conductance_data[0], I_max, "o") 
#    plt.xlabel("measurement number") #plt.xlabel("contact spacing (um)")
#    plt.ylabel("averaged current at -10 V (nA)")  
#    plt.title(save_name+" maximal current")
#    if save:
#        fig.savefig(save_name + "_maximal_current.pdf", format="pdf") 
#        
#def plot_conductance_normalized(conductance_data, zdata):
#    fig, ax = plt.subplots()
#    ax.plot(conductance_data[0], conductance_data[1]/conductance_data[1][0], "o")   
#    ax.plot(conductance_data[0], conductance_data[2]/conductance_data[1][0], "o")
#    ax.legend(["up-sweep","down-sweep"], loc = "upper left")  
#    plt.xlabel("measurement number") #plt.xlabel("contact spacing (um)")
#    plt.ylabel("conductance (1/GOhm)")  
#    plt.title(save_name+" conductances")
#    if save:
#        fig.savefig(save_name + "_conductances.pdf", format="pdf")  
 
#%%  
def export_data(dataset, conductance_data, resistance_data):
    np.savetxt(export_name+"_conductances.csv", conductance_data)
    np.savetxt(export_name+"_data.csv",dataset)
    np.savetxt(export_name+"_resistances.csv",resistance_data)
#%% 
def plot_resistance_results(resistance_data, resistance_error_data):
    fig = plt.figure(0)
    x = resistance_data[0]
    y1, y1_err = resistance_data[1], resistance_error_data[1]
    y2, y2_err = resistance_data[2], resistance_error_data[2]
    plt.errorbar(x, y1, yerr=y1_err, label ="up-sweep", marker=".", linestyle="None")
    plt.errorbar(x, y2, yerr=y2_err, label ="down-sweep", marker=".", linestyle="None")
    plt.ylim(0, 250)
    plt.xlabel("measurement number") #plt.xlabel("contact spacing (um)")
    plt.ylabel("R (G$\Omega$)")
    plt.title(save_name+", R")

    if save:
        fig.savefig(save_name + " G.pdf", format="pdf")

#%%
def error_bar_plot(data, err, save_name=save_name, y_limits =[0, 100], data_label=["up-sweep", "down-sweep"], axes_label=["measurement number", "$R$ (G$\Omega$)"], markersize=5, capsize=3):
    fig, ax = plt.subplots()
    x = data[0]
    y1, y1_err = data[1], err[1]
    y2, y2_err = data[2], err[2]
    ax.errorbar(x, y1, yerr=y1_err, label=data_label[0], marker=".", linestyle="None", markersize=markersize, capsize=capsize)
    ax.errorbar(x, y2, yerr=y2_err, label=data_label[1], marker=".", linestyle="None", markersize=markersize, capsize=capsize)
    ax.set_ylim(y_limits)
    plt.legend(data_label)
    plt.title(save_name)
    
    if save:
        fig.savefig(save_name + ".pdf", format="pdf")
#%%
def plot_correlation(x, y, y_err, save_name, data_label=["data-label"], axes_label=["x-label", "y-label"], markersize=5, capsize=3):#y_limits =[0, 100], x_err may be None
    #interpret error as systematic, due to sweep speed. By reciproke addition of 
    #the error is reduced, maximal beeing the better one. Average I & G by taking the mean.
    x=(x[1]+x[2])/2
    y=(y[1]+y[2])/2
    y_err=1/(1/y_err[1]+1/y_err[2])
    plot_with_errorbars(x, y, y_err, save_name, data_label=data_label, axes_label=axes_label, markersize=markersize, capsize=capsize)
    
#%%
def plot_with_errorbars(x, y, y_err,
                        save_name, y_limits=None, 
                        data_label=["data-label"],
                        axes_label=["x-label", "y-label"], 
                        markersize=5, capsize=3):
    fig, ax = plt.subplots()
    #interpret error as systematic, due to sweep speed. By reciproke addition of 
    #the error is reduced, maximal beeing the better one.    
    ax.errorbar(x, y, yerr=y_err, label=data_label[0], marker=".", linestyle="None", markersize=markersize, capsize=capsize)
    if y_limits==None:
        ax.set_ylim(y_limits)
    plt.legend(data_label)
    plt.title(save_name)
    ax.set_xlabel(axes_label[0]), ax.set_ylabel(axes_label[1])
    
    if save:
        fig.savefig(save_name + " errorbar-plot.pdf", format="pdf")
        
#%%
"""Assign current I to x, conductance G with errors to y, and send those params
 to plot_correlation"""
 
def plot_G_I_correlation(data_sets, data_labels, fit_deg, fit_points, output=False):         #data_sets and data_labels have to be corresponding. each are multi-dimensional!!! Ideally each data set were a struct with something like sample name, data_labels, ...
    axes_label=["I at +/- 10 V", "$G$ (1/G$\Omega$)"]
    for i in range(len(data_sets)):
        x=data_sets[i]
        x=D1_data.transpose()
        x_len=int(np.shape(x)[0]/2)
        x0= x[0][1:]
        x1=-(x[1][1:]+x[-1][1:])/2
        x2=(x[x_len][1:]+x[x_len+1][1:])/2
        x=np.vstack((x0, x1, x2))
        (y, y_err)= (process_data(data_sets[i], fit_deg, fit_points, data_labels[i], output=output))[2:4]
        save_name_i = save_name+" data_set %s" %str(i)
        plot_correlation(x, y, y_err, save_name_i, data_label=data_labels[i], axes_label=axes_label, markersize=5, capsize=3)
        
#%%
def fit_N_points(data, N, labels, output= False):       #fits and plots slope at 0 V
    (x_data,
     x_error_data,
     y_data,
     y_error_data) = (process_data(data, 3, N, labels, output=output))
    
    error_bar_plot(x_data, x_error_data, save_name+" R, N_%d" %N)
#%%
""""                  IMPORT & PLOT DATA

Here the import, plotting, fitting happens with the helper functions
from above. Explicitely: 
    -import data and save it to export .csvs,
    -plot data and zoom in to 0 for up- down sweeps
    -fit data and show results"""
    
#define data set
D1_data, files, labels = import_data(D1_data_folder)
D2_data, files, labels = import_data(D2_data_folder)
D4_data, files, labels = import_data(D4_data_folder)
D6_data, files, labels = import_data(D6_data_folder)
data_implanted=[D1_data, D2_data, D4_data, D6_data]
data_implanted_labels= [["D1"], ["D2"], ["D4"], ["D6"]]

#plot(D6_data,
#     labels,
#     axes_labels=["photocurrent (nA)", "bias voltage (V)"],
#     text_pos=[-10, 30]) 

#plot_zoom(D1_data, 20, 0, labels), plot_zoom(D1_data, 20, 1, labels)



#%%


#axes_label=["x-label", "y-label"]



#%%
#labels=[labels]

plot_G_I_correlation([D1_data, D2_data], ["D1", "D2"], 3, 20)
        #G_R_axes_labels =["G (1/G$\Omega$)", "R (G$\Omega$)"]

#(resistance_data,
#     resistance_error_data,
#     conductance_data,
#     conductance_error_data) =   (process_data(D1_data, 3, 30, labels, axes_labels =["G (1/G$\Omega$)", "R (G$\Omega$)"], output=plot_fit_output))

#process_data(D1_data, 3, 30, labels, axes_labels =["G (1/G$\Omega$)", "R (G$\Omega$)"], output=plot_fit_output)

#for crating the plot landscapes in onenote
#for i in range(16):
#    i=10+2*i
#    print("number of fit_points= %d" %i )
#    fit_N_points(i)
#    

#plot_I_max_normalized(conductance_data, data, zdata)
#fit_N_points(D1_data, 30, labels)







#%% 
"""plot all min/max values of current and the corresponding conductance around 
0 V in one plot, show deviation from the normalization to conductance"""
#to to on 22-3-2018
def plot_all_normalized(conductance_data, data, zdata, norm_index, 
                        legend_txt, text_coordinates):  #norm_index mind 1, data == raw U-I data
    
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
    
    #normalizing I by comparing to an conductance value (that one of norm_index)
    I_min_norm=I_min/conductance_data[1]
    I_max_norm=I_max/conductance_data[2]
    I_min_norm=I_min_norm/np.average(I_min_norm)
    I_max_norm=I_max_norm/np.average(I_max_norm)
    #deviation in %
    I_min_norm_deviation=100-(I_min_norm)*100 
    I_max_norm_deviation=100-(I_max_norm)*100 

    G_0=conductance_data[1][norm_index]
    conversion_factor= I_0/G_0

    #plotting
    fig, ax= plt.subplots()
    x=conductance_data[0]
    ax.plot(x, I_max_norm_deviation, ".", x, I_min_norm_deviation, ".")
    ax.set_xlabel("measurement number"), ax.set_ylabel("deviation (%)")
    plt.ylim(-100, 100)
    plt.title(save_name+"\nrelative current deviation at 10 V from G-predicted values")
    if save:
        fig.savefig(save_name + "_I_deviation.pdf", format="pdf")  
        
    #plotting
    fig, ax = plt.subplots()
    ax.plot(x, I_max, ".", x, I_min, ".")#, "o", "x") 
    ax.plot(conductance_data[0], conductance_data[1]/G_0, ".")   
    ax.plot(conductance_data[0], conductance_data[2]/G_0, ".")
    figure_comment = r'conversion factor = %d A$\cdot \Omega$' % conversion_factor
    ax.text(text_coordinates[0], text_coordinates[1],figure_comment)
    ax.legend(legend_txt, loc = "upper left")  
    ax.set_xlabel("measurement number") #plt.xlabel("contact spacing (um)")
    ax.set_ylabel("current, conductance (normalized)")  
    plt.title(save_name+"\nI, G normalized to measurement %d" %(norm_index+1))
    if save:
        fig.savefig(save_name + "_I_G_norm.pdf", format="pdf") 
#%%
#plot_all_normalized(conductance_data, data, data[0], 10, ["|I$_\mathrm{min}$|", "|I$_\mathrm{max}$|", "G, up-sweep","G, down-sweep"], [1,2])
