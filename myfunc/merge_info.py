# -*- coding: utf-8 -*-
"""
Created on Mon Aug 26 17:45:07 2019

@author: Yijun.Wan
"""

def merge_info(initial_df, extracted_results, df_other_info):
    
    import pandas as pd
    from process_functions.py import text_split
    
    info = df_other_info
    df = extracted_results.merge(initial_df.reset_index()[['index', 'case_number', 'is_public', 'created_date',\
                                    'last_modified_date', 'comment']], 'left', left_on='c_id', right_on = 'index')
    dd = df[['case_number', 'small versions','confidence_level','is_public', 'created_date',\
                'last_modified_date', 'comment']].copy()
    
    txt_split2 =  dd['small versions'].apply(text_split)
    dd['Extracted_Product'] = list(txt_split2.apply(lambda x: x[0]))
    dd['Extracted_Product'] = dd['Extracted_Product'].fillna('not available')
    dd['Extracted_Digits'] = list(txt_split2.apply(lambda x: x[1]))

    dd.drop_duplicates(['case_number', 'Extracted_Product', 'Extracted_Digits', 'confidence_level'], inplace=True)

    dd.columns = ['case_number','Extracted Version','Confidence Level','is_public', 'created_date',\
                  'last_modified_date','comment','Extracted Product','Extracted Digits']
    
    dd1 = dd.merge(info[['case_number', 'account_name', 'FRR_SAP_number','product_family',\
                            'sub_product_family', 'sub_product_detail']], how='left',on = 'case_number').copy()
    
    dd1['created_date'] = pd.to_datetime(dd1['created_date'])
    dd1['last_modified_date'] = pd.to_datetime(dd1['last_modified_date'])
    
    dd1 = dd1.fillna('not available')
    dd1['Product_sub_rank'] = dd1.groupby(['FRR_SAP_number','Extracted Product','product_family', 'sub_product_family',\
                                           'sub_product_detail'])['created_date'].rank(ascending=False, method = 'dense')
    ## create new feature

    dd1['Product_sub_rank'] = dd1['Product_sub_rank'].astype(int)
    
    return dd1
