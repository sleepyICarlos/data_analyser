# -*- coding: utf-8 -*-
"""
Created on Fri Dec  8 19:52:36 2017

@author: hartz
"""
import data_reader
import python_pptx as ppt
import plot_fit_lib

#define all the variables we have in our experiment
current= data_reader.observable('current', 0, 'A')
pad_distance= data_reader.observable('pad distance', 0, 'um')
voltage= data_reader.observable('voltage', 0, 'V')
resistance= data_reader.observable('contact resistance', 0, 'GOhm')


UI_data=[voltage, current, pad_distance]
import_param= data_reader.import_parameters(0,1,2, ',', '.csv')

a=import_param.x_column_index
b=import_param.format
c=import_param.y_column_index
d=import_param.separator


mydata_2_3_after_anneal =data_reader.data_set( 'E:\\sciebo\\ZnSe\\M12-0088\\2.3\Aachen PS\\120Chotplate 2h\\structure 3', 'sample2.3', 'dat', '_', 'structure', UI_data)
mydata_2_3_after_anneal = data_reader.import_2D_data(mydata_2_3_after_anneal, [1,1e6,1], import_param)

