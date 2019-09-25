# -*- coding: utf-8 -*-

if __name__ == '__main__':
    
    from _pycache_.process import process
    from _pycache_.merge_info import merge_info
    from _pycache_.transform import transform
    from _pycache_.read_data import read_json, read_data
    import pandas as pd

    
    ### file with all files' path
    json_file_path = r'..\path.txt'
    
    path_dic = read_json(json_file_path)
    
    df, lookup, full_lookup, df_other_info, extract_output_path = read_data(path_dic)

    ## remove rows with null value in 'comment' column
    df2 = df[df['comment'].notnull()]
    
    df_extracted = process(df2['comment'], full_lookup, lookup)
    df_final = merge_info(df2, df_extracted, df_other_info)
    
    df_final.to_csv(extract_output_path)
    