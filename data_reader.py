# -*- coding: utf-8 -*-
"""
Created on Fri Dec  8 17:55:23 2017

@author: hartz
"""
import os
import numpy as np    #do I really need np for the for loop? [np.arange(...)]

class observable:
    def __init__(self, name, value, unit):
        self.name= name
        self.value=value
        self.unit = unit

class fig_comments:
    def __init__(self, comment, observables):
        self.comment=comment
        self.x_name= observables[0].name +' (%s)' %observables[0].unit
        self.y_name= observables[1].name +' (%s)' %observables[1].unit
        self.legend_name = observables[2].name +' (%s)' %observables[2].unit
        
class comment_list:
    def __init__(self, folder_name, sample_name, file_start_name, file_end_name, structure_name, file_name_separator, save_name):
        self.folder_name=folder_name        
        self.sample_name= sample_name
        self.file_start_name= file_start_name
        self.file_end_name= file_end_name
        self.name_list=[]
        self.file_name_separator= file_name_separator
        self.structure_name= structure_name
        self.save_name= save_name

class data_specs:
    def __init__(self, comment_list, observables, data=[]):
        self.folder= comment_list.folder_name
        self.start_name= comment_list.file_start_name
        self.end_name= comment_list.file_end_name
        self.file_name_separator= comment_list.file_name_separator    
        self.identifier= comment_list.structure_name
        self.x= observables[0]
        self.y= observables[1]
        self.y= observables[2]
        #to do: check, if this potentially causes problems
        self.data=data
        
        #self.x.name=observables.name                       #do I really need this or can this be "inherited??!
        
class import_parameters:
    def __init__(self, x_column_index, y_column_index, skip_header, converting_factors, separator, file_format):
        self.skip_header= skip_header
        self.x_column_index= x_column_index
        self.y_column_index = y_column_index
        self.separator = separator 
        self.format=file_format                     #kw arg, default ',' must not hbe handeled to the fkt.
        self.converting_factors= converting_factors
        
def import_2D_data(data_specs, import_parameters):           #not very slim definition...
    #x_converting_factor, y_converting_factor, z_converting_factor =converting_factors[0], converting_factors[1], converting_factors[2]
    y_converting_factor = import_parameters.converting_factors[1]    
    x_values, y_values, z_values, files =[], [], [], [] 
    start_name= data_specs.start_name                         #clear start values
    folder= data_specs.folder
    end_name= data_specs.end_name
    separator= data_specs.file_name_separator    
    x_index= import_parameters.x_column_index  
    y_index= import_parameters.y_column_index 
    skip= import_parameters.skip_header


    if y_converting_factor!=1:                       #to do!, choose good implementation method
        for file in os.listdir(folder):                         #scan data files
            if file.startswith(start_name):                     #select measurement series (start, end , identifier)
                if file.endswith(end_name):
                    contents = file.split(separator)       
                    for i in np.arange(len(contents)):
                        if contents[i] == data_specs.identifier:
                            z_val = int(contents[i+1])
                            break
                    z_values.append(z_val)
                    files.append(file)
                    new_y_value=np.genfromtxt(folder+'\\'+file, usecols=y_index, skip_header=skip).astype(float)
                    new_y_value*= y_converting_factor            #convert from mA to nA
                    y_values.append(np.concatenate((np.array([z_val]),new_y_value)))       # skip_header: skips device names, usecol: uses 2nd column (current)
    
    else:
        for file in os.listdir(folder):                         #scan data files
            if file.startswith(start_name):                     #select measurement series (start, end , identifier)
                if file.endswith(end_name):
                    contents = file.split(separator)       
                    for i in np.arange(len(contents)):
                        if contents[i] == data_specs.identifier:
                            z_val = int(contents[i+1])
                            break
        
                    z_values.append(z_val)
                    files.append(file)
                    new_y_value=np.genfromtxt(data_specs.folder+'\\'+file, usecols=y_index, skip_header=skip).astype(float)
                    y_values.append(np.concatenate((np.array([z_val]),new_y_value)))
    
    y_values.sort(key=lambda x: x[0])
    #values=np.array(values)*1e6 #convert to nA 
    z_values.sort()
    x_values = np.concatenate((np.array([0]),np.genfromtxt(folder+'\\'+files[0], usecols= x_index, skip_header = skip))) 
    data = np.vstack((x_values,y_values))
    return data
    
