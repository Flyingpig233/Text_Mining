# -*- coding: utf-8 -*-
"""
Created on Mon Aug 26 17:40:43 2019

@author: Yijun.Wan
"""
def extract(series, regx = None):
    
    import re
    import pandas as pd
    
    # Input data need to be pd.Series
    
    ## define matching criteria
    if regx is None:
        
        regular_expression = r'.?[A-Z]{1}[A-Za-z]{1,}.[0-9]{1,2}[.][0-9]{1,2}[.0-9]*.?|[0-9]{1,2}[.]{1}[0-9]{1,2}[.]{1}[0-9]{1,2}'
    
    else:
        regular_expression = regx
    
    ## replace '()+' with white space
    n1 = [re.sub('[()+]', ' ', x) for x in series]
    ## delete unnecessary words
    n2 = [re.sub('\s[vV]ersion is|\s[vV]ersion|[vV]ersion', '', x) for x in n1]
    
    n3 = [re.sub('Notes|notes|Release|release|mapping|Mapping', '', x) for x in n2]
   
    
    
    # get a match object
    matches = pd.Series([re.findall(regular_expression ,str(x)) for x in n3], index = series.index)
    

    ind = [len(x)!=0 for x in matches]
    extracted = matches[ind]
    extracted.name = 'Matched Results'

    extract_final = pd.DataFrame(extracted)
    extract_final['Matched Num'] =  extract_final['Matched Results'].apply(len)
    
    return extract_final

def extract_split(index, matched, length):
    
    import re
    import pandas as pd
    from itertools import chain
    
    ## split the lst in 'Matched Results'
    col_id = index.repeat(length)
    col_version = list(chain(*list(matched)))
    col_clean_version = [re.sub('[^0-9a-z.]', '', x.lower()) for x in col_version]
    col_clean_version = [re.sub('[^0-9]$', '', x) for x in col_clean_version]
    extract_break = pd.DataFrame({'c_id':col_id, 'extract_info': col_version, 'clean_info': col_clean_version})
    
    
    return extract_break


def text_split(string):
    
    import numpy as np
    import re
    # input is a string 
    
    ## clean the unrelated character which will be different from 
    x = re.sub('[^A-Za-z0-9.]+', "", string)
    ind = x[0] in set(['0','1','2','3','4','5','6','7','8','9'])
    if ind:
        return np.nan, x
    else:
                # slice index
        start = re.search('\d',x).span()[0]
    
        p1 = x[:start]
        p2 = x[start:]

        return p1, p2


def words_near(comment_string, extract, search_num = 10, lower=True):
    
    import re
    
    
    extract = extract.rstrip('\\')
    extract = re.sub('\[', '\[', extract)
    extract = re.sub('\]', '\]', extract)
    cmt1 = re.sub('[()+]', ' ', comment_string)
    cmt2 = re.sub('\s[vV]ersion is|\s[vV]ersion|[vV]ersion', '', cmt1)
    cmt3 = re.sub('Notes|notes|Release|release|mapping|Mapping', '', cmt2)
   
    length = len(cmt3)
    ab = re.search(extract, cmt3).span()
    a = ab[0]
    b = ab[1]
    l_end = a < search_num*6
    # not enough words after
    r_end = (length - b) < 30
    
    if l_end & r_end:
        cmt_sub = cmt3
    elif l_end:
        cmt_sub = cmt3[:b + 30]
        
    elif r_end:
        cmt_sub = cmt3[a - search_num*6:]
    else:
        cmt_sub = cmt3[a - search_num*6: b+30 ]
    
    word_lst = re.split('\s|\n', cmt_sub)


    word_lst_lower = [re.sub('[^a-z]+', "", x.lower()) for x in word_lst]
    word_lst = [re.sub('[^A-Za-z]+', "", x) for x in word_lst]
    
    if lower:
        return set(word_lst_lower)
    else:
        return set(word_lst)


def find_alphabets(words_near,potential, lower=False):
    
    if len(words_near)==0:
        return set()
    words_near = set(words_near)- set({'Was', 'WAs','was', 'be'})
    
    if lower:
        a = set([x.lower() for x in words_near])
    else:
        a = set(words_near)
        
    b = set(potential)
    s2 = a.intersection(b)
    
    return s2
    
