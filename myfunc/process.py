# -*- coding: utf-8 -*-
"""
Created on Mon Aug 26 17:43:15 2019

@author: Yijun.Wan
"""

def process(comments, full_lookup, lookup):
    
    import pandas as pd
    import re
    from process_functions.py import extract, extract_split, text_split, words_near, find_alphabets
    
    o1 = extract(comments)
    o1_break = extract_split(o1.index.values, o1['Matched Results'], o1['Matched Num'])
    
    ## high confidence
    ind_high = o1_break['clean_info'].isin(full_lookup['small_lower_clean'])
    high = o1_break[ind_high].copy()
    high['confidence_level'] = 'high confidence'
    high_dedup = high[~high.duplicated(['c_id','clean_info'], keep='first')].copy()
    high_a = pd.merge(high_dedup, full_lookup, how ='left', left_on = 'clean_info', right_on = 'small_lower_clean' )
    high_b = high_a[['c_id', 'small versions', 'confidence_level']].copy()
    
    
    
    ## medium confidence
    low = o1_break[~ind_high].copy()
    txt_split = low['extract_info'].apply(text_split)
    low['Alphabets'] = list(txt_split.apply(lambda x: x[0]))
    low['Digits'] = list(txt_split.apply(lambda x: x[1]))
    
    
    ### medium case1
    ind_med1 = low['Alphabets'].notnull()
    med1 = low[ind_med1].copy()
    med1['small versions'] = med1['Alphabets'].apply(lambda x: x.lstrip('.').rstrip('.')) + " " + med1['Digits'].apply(lambda x: re.sub('[^0-9]+$','', x))
    med1['confidence_level'] = 'medium confidence'
    med1_a = med1[['c_id', 'small versions', 'confidence_level']].copy()
                         
                         
    ### medium case2
    low2 = low[~ind_med1].copy()
    m2f = low2[~low2.duplicated(['c_id', 'Digits'], keep='first')].copy()                     
    m2f['comment'] = m2f['c_id'].map(comments.to_dict())
    
    m2f_words = m2f[['comment','extract_info']].apply(lambda x: words_near(*x, lower= False), axis=1)
    m2f_words.name = 'words near'
    mt1 = m2f_words.apply(lambda x: find_alphabets(x, lookup['alphabets'], lower=True))
    
    #### match product alphabets
    col_len = mt1.apply(lambda x:len(x))
    ind_map = col_len.apply(lambda x:x!=0)
    product_split = extract_split(mt1[ind_map].index.values, mt1[ind_map],\
                              col_len[ind_map])[['c_id', 'extract_info']]
    product_split.columns = ['id', 'product']
    
    map1 = pd.merge(product_split, m2f.reset_index(), how = 'left', \
                left_on ='id', right_on ='index')[['c_id','Digits','product']].copy()
    
    map2 = pd.merge(map1, lookup,how = 'left', left_on ='product',\
                    right_on='alphabets')[['c_id', 'Digits', 'Alphabets']].copy()
    map2['small versions'] = map2['Alphabets']+' '+ map2['Digits']
    
    ind_med2 = map2['small versions'].apply(lambda x: re.sub('[^a-z0-9.]','', x.lower())).isin(full_lookup['small_lower_clean'])
    med2 = map2[ind_med2][['c_id', 'small versions']].copy()
    med2['confidence_level'] = 'medium confidence'
    med = pd.concat([med1_a, med2], axis=0)
    
    ### low confidence
    low_no_mapping = m2f[~ind_map][['c_id', 'Digits']].copy()
    low_no_mapping.columns = ['c_id', 'small versions']
    low_mapping = map2[~ind_med2][['c_id', 'small versions']].copy()
    
    low3 = pd.concat([low_mapping, low_no_mapping], axis=0)
    low3['confidence_level'] ='low confidence'
    
    
    ver = pd.concat([high_b, med, low3], axis=0, ignore_index=True)
    ver.drop_duplicates(keep = 'first', inplace= False)
    ver_dedup = ver[~ver.duplicated(keep='first')]
    
    
    return ver_dedup
    