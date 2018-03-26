# -*- coding: utf-8 -*-
"""
Created on Mon Mar 26 11:35:04 2018

@author: hartz
"""
#%%
"""Define some classes containing information on the data saving location
sample set than can carry all analysis quantities important for our photocurrent
analysis"""

import numpy as np
import os


save_folder = "Z:\sciebo\promotion\6_LogsDataAnalysis\1_data\IHT_probe_station\MA-0084\python"






#%%
def set_path(folder, office = True):
    if office:
        folder = "Z:\sciebo" + folder
    else:
        folder = "D:\documents\sciebo" + folder
    return folder

#%%
class sample_set():
    def __init__(self, folders=[], names=[], T_anneal=[], structure="Stripes", implanted= True):
        self.folders = folders
        self.names   = names
        self.structure = structure
        self.T_anneal= T_anneal
        self.figure_comment = data_set_fig_comment("all", structure, "variable temperatures", implanted=implanted)
        if implanted:
            self.implanted=implanted
        else:
            self.implanted=False
        self.data =[]
        self.I_max=[]
        self.G=[]
        self.G_err=[]
        self.R=[]
        self.R_err=[]
        self.A=[]
        self.A_err=[]
        self.circ=[]
        self.circ_err=[]

undoped, doped = sample_set(), sample_set()

class data_set():
    def __init__(self, folder, sample_set, sample_name, T_anneal, office=True):
        folder = set_path(folder)
        structure = sample_set.structure
        implanted=sample_set.implanted
        export_name = sample_name +" " + structure
        data = import_data(folder)
        figure_comment = fig_comment(sample_name, structure, T_anneal, implanted=implanted)
        self.sample_name = sample_name
        self.save_name = "sample %s %d °C anneal %s" %(sample_name, T_anneal , structure)
        self.export_name = export_name
        self.folder = folder
        self.data = data
        self.T_anneal = T_anneal
        self.sample_name = sample_set
        self.figure_comment=figure_comment
        sample_set.folders.append(folder)
        sample_set.names.append(sample_name)
        sample_set.T_anneal.append(T_anneal)
        sample_set.data.append(data)

#%%
def fig_comment(sample_name, structure, T_anneal, implanted=True):
    if implanted:
        figure_comment ="sample %s %s\n1 $\mu$m ZnSe + 170 nm Al ($ex-situ$)\nAl+Cl implantation at 1 keV\nafter annealing at %d °C for 3 min" %(sample_name, structure, T_anneal)
    else:
        figure_comment ="sample %s %s\n1 $\mu$m ZnSe + 170 nm Al ($ex-situ$)\nno implantation\nafter annealing at %d °C for 3 min" %(sample_name, structure, T_anneal)
    return figure_comment

def data_set_fig_comment(sample_name, structure, T_anneal, implanted=True):
    if implanted:
        figure_comment ="sample %s %s\n1 $\mu$m ZnSe + 170 nm Al ($ex-situ$)\nAl+Cl implantation at 1 keV\nafter annealing at %s for 3 min" %(sample_name, structure, T_anneal)
    else:
        figure_comment ="sample %s %s\n1 $\mu$m ZnSe + 170 nm Al ($ex-situ$)\nno implantation\nafter annealing at %s for 3 min" %(sample_name, structure, T_anneal)
    return figure_comment

#%%
def import_data(folder, end_name=".txt", separator="_", office=True):
    data, voltages, values, zdata, files =[], [], [], [], []     #pad distance: any param read from file name
    measurement_counter = 0
    measurement_description = []
    for file in os.listdir(folder):
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


#%%
"""define data location and put it in one data_struct"""
D1_folder = "\ZnSe\M12-0084\IHT Probestation\D1\Stripes\data"
D2_folder = "\ZnSe\M12-0084\IHT Probestation\D2\Stripes\data"
D4_folder = "\ZnSe\M12-0084\IHT Probestation\D4\Stripes\data"
D6_folder = "\ZnSe\M12-0084\IHT Probestation\D6\Stripes\data"

UD1_folder = "\ZnSe\M12-0084\IHT Probestation\\UD1\Stripes\data"
UD2_folder ="\ZnSe\M12-0084\IHT Probestation\\UD2\Stripes\data"
UD3_folder = "\ZnSe\M12-0084\IHT Probestation\\UD3\Stripes\data"
UD4_folder = "\ZnSe\M12-0084\IHT Probestation\\UD4\Stripes\data"

undoped, doped = sample_set([], [], [], implanted=False), sample_set([], [], [], implanted=True)

D1 = data_set(D1_folder, doped, "D1", 250)
D2 = data_set(D2_folder, doped, "D2", 300)
D4 = data_set(D1_folder, doped, "D4", 250)
D6 = data_set(D1_folder, doped, "D6", 20)
UD1 = data_set(D1_folder, undoped, "UD1", 20)
UD2 = data_set(D1_folder, undoped, "UD2", 250)
UD3 = data_set(D1_folder, undoped, "UD3", 350)
UD4 = data_set(D1_folder, undoped, "UD4", 250)
#now we have: doped.data[0]==D1.data
print("imported doped samples successfully:\n%s \n"  
      "imported undoped samples successfully:\n%s" %(doped.names, undoped.names))

