# -*- coding: utf-8 -*-
"""
Created on Fri Dec  8 21:46:29 2017

@author: hartz
"""
import matplotlib.pyplot as plt

#def plot_all(data):
   # x=data[0]
   # ...import all other fitting, plotting, res. fkts...
   
       
def plot(data, comment_list, figure_comments, save=False, text_coordinates=[0,0]):
    fig, ax = plt.subplots()
    for data_set in range(len(data)-1):
        ax.plot(data[0,1:], data[data_set+1][1:], '-')
        
    ax.text(text_coordinates[0], text_coordinates[1], figure_comments.comment)
    ax.legend(data[1:, 0], loc = 'lower right', title = figure_comments.legend_name)
    #legend = ax.legend(loc='upper center', shadow=True, fontsize='x-large')
    plt.xlabel(figure_comments.x_name)
    plt.ylabel(figure_comments.y_name)
    plt.title=comment_list.sample_name +' %s' %comment_list.structure_name
    fig.savefig(comment_list.save_name +'_all_data.pdf', format='pdf')