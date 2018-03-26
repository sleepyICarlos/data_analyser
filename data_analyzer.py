# -*- coding: utf-8 -*-
"""
Created on Mon Mar 26 14:46:37 2018

@author: hartz
"""
#%% 
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
from numpy.polynomial.polynomial import polyval

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
