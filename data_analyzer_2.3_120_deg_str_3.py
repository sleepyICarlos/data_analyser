# -*- coding: utf-8 -*-
"""
Created on Fri Dec  8 19:52:36 2017

@author: hartz
"""
import data_reader
import python_pptx as ppt
import plot_fit_lib as plot

#to do (10.12.2017)
#planned: read_plot_data_series(data), with class data containing the following attributes: 
#data.comment_list
#data.import_parameters (automated selection between .dat and .csv files desirable, and the skip header fkt automated, skipp all stringlinke entries.)

export_directory= 'E:\\python_export'

save= False #optional True/ False
pptx_export= False

#define all the variables we have in our experiment
current= data_reader.observable('current', 0, 'A')
pad_distance= data_reader.observable('pad distance', 0, 'um')
voltage= data_reader.observable('voltage', 0, 'V')
resistance= data_reader.observable('contact resistance', 0, 'GOhm')


#combine all observables
UI_data=[voltage, current, pad_distance]



#sample 2.3 after 120°C hotplate
def read_plot_data_series(i):        #structure index i
    file_read_comments=data_reader.comment_list('E:\\sciebo\\ZnSe\\M12-0088\\2.3\\Aachen PS\\120Chotplate 2h\\structure %s' %str(i),
                                                '2.3', 
                                                's',
                                                '.dat', 
                                                'structure',
                                                '_',
                                                '2.3_after_2_h120°C')
    import_parameters= data_reader.import_parameters(0,1,2, [1,1e6,1], ',', '.dat')
    mydata_specs =data_reader.data_specs(file_read_comments, UI_data)
    mydata_2_3_after_anneal = data_reader.import_2D_data(mydata_specs, import_parameters)


#plotting
    fig_comments = data_reader.fig_comments('structure %s' %str(i), UI_data)
    plot.plot(mydata_2_3_after_anneal, file_read_comments, fig_comments, text_coordinates=[0,15])

for i in range(3):
    read_plot_data_series(i+3)


#sample 2.3 after 250°C annealing
def read_plot_data_series_after_anneal(i):        #structure index i
    file_read_comments=data_reader.comment_list('E:\\sciebo\\ZnSe\\M12-0088\\2.3\\Aachen PS\\2-3 hours 90Chotplate',
                                                '2.3', 
                                                's',
                                                '.dat', 
                                                'structure',
                                                '_',
                                                '2.3_after_2_h120°C')
    import_parameters= data_reader.import_parameters(0,1,2, [1,1e6,1], ',', '.dat')
    mydata_specs =data_reader.data_specs(file_read_comments, UI_data)
    mydata_2_3_after_anneal = data_reader.import_2D_data(mydata_specs, import_parameters)


#plotting
    fig_comments = data_reader.fig_comments('structure %s' %str(i), UI_data)
    plot.plot(mydata_2_3_after_anneal, file_read_comments, fig_comments, text_coordinates=[0,15])

read_plot_data_series_after_anneal(1)


#to do:fix double existance of .csv ending(@ comment list,+ @data import)
#for samples 3.3/ 3.4
def read_plot_data_series_IHT():        #structure index i
    file_read_comments=data_reader.comment_list('E:\\sciebo\\ZnSe\\M12-0088\\3.4 before anneal (IHT)\\struktur 2',
                                                '3.4', 
                                                'sample3.4',
                                                '.csv', 
                                                '2017-12-07',
                                                '_',
                                                '3.4_before annealing')
    import_parameters= data_reader.import_parameters(0,1,2, [1,1,1], ',', '.csv')
    mydata_specs =data_reader.data_specs(file_read_comments, UI_data)
    mydata_3_4_before_anneal = data_reader.import_2D_data(mydata_specs, import_parameters)


#plotting
    fig_comments = data_reader.fig_comments('structure %s' %str(i), UI_data)
    plot.plot(mydata_3_4_before_anneal, file_read_comments, fig_comments, text_coordinates=[0,15])

read_plot_data_series_IHT()
#read_plot_data_series_IHT(0)


