# -*- coding: utf-8 -*-
"""
Created on Mon Aug 26 17:38:04 2019

@author: Yijun.Wan
"""

def read_json(json_file_path):
    
    import json
    with open(json_file_path) as json_file:
        dic = json.load(json_file)
    
    return dic



def read_data(path_dic):
    
    import pandas as pd
    import os

    data = path_dic
    save_folder_path = data['save_folder_path']
    extract_output_name =  data['extract_output_name']
    lookup_file_path = data['lookup_file_path']
    full_lookup_file_path = data['full_lookup_file_path']
    other_info_file_path = data['other_info_file_path']
    data_folder_path = data['data_folder_path']
    
    extract_output_path = os.path.join(save_folder_path , extract_output_name)
    
    ## load data
    lookup = pd.read_csv(lookup_file_path, usecols = ['Alphabets', 'alphabets'])
    full_lookup = pd.read_csv(full_lookup_file_path, usecols = ['small versions', 'small_lower_clean'])
    df_other_info = pd.read_csv(other_info_file_path)
    
    files = os.listdir(data_folder_path)
    files_list = [pd.read_csv(os.path.join(data_folder_path, file_name)) for file_name in files]
    df = pd.concat(files_list, axis=0, ignore_index= True)
    
    
    
    
    return df, lookup, full_lookup, df_other_info, extract_output_path