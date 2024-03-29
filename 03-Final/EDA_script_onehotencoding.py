# %%
# Import packages
import pandas as pd
from warnings import simplefilter
simplefilter(action="ignore", category=pd.errors.PerformanceWarning)
import numpy as np
import os
import matplotlib.pyplot as plt
import seaborn as sns

# Set options
pd.options.display.max_rows = 999
pd.options.display.max_columns = 999

train_x_raw = pd.read_csv("../01-Data/X_train.csv", low_memory = True, index_col=0)
train_y_raw = pd.read_csv("../01-Data/y_train.csv", low_memory = True, index_col=0)
test_x_raw = pd.read_csv("../01-Data/X_test.csv", low_memory=True, index_col=0)

df_train = pd.DataFrame(train_x_raw)
df_test = pd.DataFrame(test_x_raw)
df_y = pd.DataFrame(train_y_raw)

############################################################# FUNCTIONS ###############################################################

### Function to find the targeted colname
def find_colname_start(data, target):
  temp = []
  for varname in data.columns:
      if varname.startwith(target):
        temp.append(varname)
  return(temp)
  
def find_colname_end(data, target):
  temp = []
  for varname in data.columns:
      if varname.endswith(target):
        temp.append(varname)
  return(temp)

from collections import Counter

def merge_columns(dat, colname):
    for name in colname:
        name_org = name.replace("_11c", "")
        dat.loc[dat[name_org] == -4, name_org] = dat.loc[dat[name_org] == -4, name]


def print_diff(varname):
  print(set(df_train[varname].unique()).difference(set(df_test[varname].unique())))

def cumulatively_categorise(column,threshold=0.80,return_categories_list=True):
  #Find the threshold value using the percentage and number of instances in the column
  threshold_value=int(threshold*len(column))
  #Initialise an empty list for our new minimised categories 
  categories_list=[]
  #Initialise a variable to calculate the sum of frequencies
  s=0
  #Create a counter dictionary of the form unique_value: frequency
  counts=Counter(column)

  #Loop through the category name and its corresponding frequency after sorting the categories by descending order of frequency
  for i,j in counts.most_common():
    #Add the frequency to the global sum
    s+=dict(counts)[i]
    #Append the category name to the list
    categories_list.append(i)
    #Check if the global sum has reached the threshold value, if so break the loop
    if s>=threshold_value:
      break
  #Append the category Other to the list
  categories_list.append(-100)

  #Replace all instances not in our new categories by Other  
  new_column=column.apply(lambda x: x if x in categories_list else -100)

  #Return transformed column and unique values if return_categories=True
  if(return_categories_list):
    return new_column,categories_list
  #Return only the transformed column if return_categories=False
  else:
    return new_column
  
def simpleAggregation_helper(var, threshold):
  train=df_train[var]
  test=df_test[var]
  cat = [train, test]
  df = pd.concat(cat)
  transformed_column=cumulatively_categorise(df, threshold, return_categories_list=False)
  tc_train=transformed_column[0:len(train)]
  tc_test=transformed_column[len(train):len(train)+len(test)]
  df_train[var]=tc_train
  df_test[var]=tc_test

  
def simpleAggregation(variable, threshold=0.8):
    if isinstance(variable, str):
      simpleAggregation_helper(variable, threshold)
    elif isinstance(variable, list):
      for varname in variable:
        simpleAggregation_helper(varname, threshold)
        
### Convert fw_start ==> Start month of fw
### Convert fw_end ==> Duration of fw
def timeEDA(data):
    fw_start = data['fw_start']
    fw_end = data['fw_end']
    fieldwork_start_month = []
    fw_duration = []
    for obs in range(0, len(fw_end)):
        fw_start_year = int(str(fw_start[obs])[0:4])
        fw_start_month = int(str(fw_start[obs])[4:6])
        fw_end_year = int(str(fw_end[obs])[0:4])
        fw_end_month = int(str(fw_end[obs])[4:6])
        duration_year = fw_end_year - fw_start_year
        duration_month = fw_end_month - fw_start_month
        duration = 12*duration_year + duration_month
        fieldwork_start_month.append(fw_start_month)
        fw_duration.append(duration)
    data['fw_start'] = fieldwork_start_month
    data['fw_end'] = fw_duration
    data.rename(columns={'fw_start':'fw_start_month', 'fw_end':'fw_duration'}, inplace=True)


##############################################################################################################################

# %% [markdown]
############################################################ EDA-AMY ############################################################
# ### Age-related variables processing
columns_to_drop = ['c_abrv', 'f46_IT', 'v72_DE', 'v73_DE', 'v74_DE', 'v75_DE', 'v76_DE', 'v77_DE', 'v78_DE', 'v79_DE']
df_train.drop(columns=columns_to_drop, inplace=True)
df_test.drop(columns=columns_to_drop, inplace=True)
# %%
# v226 year of birth respondent (Q64)
# age age:respondent
# age_r age recorded (6 intervals)
# age_r2 age recoded (3 intervals)
# age_r3 age recoded (7 intervals)

ages = ['v226', 'age', 'age_r', 'age_r2', 'age_r3']
#df_train.drop(columns=ages_to_drop, inplace=True)
#df_test.drop(columns=ages_to_drop, inplace=True)
# DECIDE WHICH ONE TO KEEP AFTER EVALUATING 




# %% [markdown]
# ### Education level-related variables drop

# v243*: educational level respondent: ... with variations



# %%
# keep v243_ISCED_3: educational level respondent: ISCED-code three digit  
v243_to_drop = ['v243_edulvlb', 'v243_edulvlb_2', 'v243_edulvlb_1', 'v243_ISCED_2', 'v243_ISCED_2b','v243_ISCED_1', 'v243_EISCED', 'v243_ISCED97', 'v243_8cat', 'v243_r', 'v243_cs', 'v243_cs_DE1', 'v243_cs_DE2', 'v243_cs_DE3', 'v243_cs_GB1', 'v243_cs_GB2']

df_train.drop(columns=v243_to_drop, inplace=True)
df_test.drop(columns=v243_to_drop, inplace=True)

# %% [markdown]
# ### Job kinds-related variables drop

# %%

# %%
# keep v246_ESeC : kind of job respondent - ESEC08 code  
v246_to_drop = ['v246_ISCO_2', 'v246_SIOPS', 'v246_ISEI', 'v246_egp']

df_train.drop(columns=v246_to_drop, inplace=True)
df_test.drop(columns=v246_to_drop, inplace=True)

# %% [markdown]
# ### Partner Education Level variables drop

# %%


# %%
# keep v252_edulvlb_2: educational level spouse/partner: ESS-edulvlb coding two digits 
v252_to_drop = ['v252_edulvlb', 'v252_edulvlb_1', 'v252_ISCED_3', 'v252_ISCED_2', 'v252_ISCED_2b', 'v252_ISCED_1', 'v252_EISCED', 'v252_ISCED97', 'v252_8cat', 'v252_r', 'v252_cs', 'v252_cs_DE1', 'v252_cs_DE2', 'v252_cs_DE3', 'v252_cs_GB1', 'v252_cs_GB2']

df_train.drop(columns=v252_to_drop, inplace=True)
df_test.drop(columns=v252_to_drop, inplace=True)

# %% [markdown]
# ### Kind of job partner variables drop

# %%

# %%
# keep v255_ESeC: kind of job spouse/partner - ESEC08 code 
v255_to_drop = ['v255_ISCO_2', 'v255_SIOPS', 'v255_ISEI', 'v255_egp']

df_train.drop(columns=v255_to_drop, inplace=True)
df_test.drop(columns=v255_to_drop, inplace=True)

# %% [markdown]
# ### Households income variables to drop



# %%
df_train.drop('v261_ppp', inplace=True, axis=1)
df_test.drop('v261_ppp', inplace=True, axis=1)

# %% [markdown]
# ### education level father/mother variables drop

# %%

# %%
# keep v262_edulvlb_2: educational level father: ESS-edulvlb coding two digits 
v262_to_drop = ['v262_edulvlb', 'v262_edulvlb_1', 'v262_ISCED_3', 'v262_ISCED_2', 'v262_ISCED_2b', 'v262_ISCED_1', 'v262_EISCED', 'v262_ISCED97', 'v262_8cat', 'v262_r', 'v262_cs', 'v262_cs_DE1', 'v262_cs_DE2', 'v262_cs_DE3', 'v262_cs_GB1', 'v262_cs_GB2']

df_train.drop(columns=v262_to_drop, inplace=True)
df_test.drop(columns=v262_to_drop, inplace=True)

# %%

# %%
# keep v263_edulvlb_2:educational level mother: ESS-edulvlb coding two digits
v263_to_drop = ['v263_edulvlb', 'v263_edulvlb_2', 'v263_edulvlb_1', 'v263_ISCED_3', 'v263_ISCED_2', 'v263_ISCED_2b', 'v263_ISCED_1', 'v263_EISCED', 'v263_ISCED97', 'v263_8cat', 'v263_r', 'v263_cs', 'v263_cs_DE1', 'v263_cs_DE2', 'v263_cs_DE3', 'v263_cs_GB1', 'v263_cs_GB2']

df_train.drop(columns=v263_to_drop, inplace=True)
df_test.drop(columns=v263_to_drop, inplace=True)

# %% [markdown]
# ### Interview dates variables drop

# %%
# v277: date of interview 
# v278a: time of interview: start hour 
# v278b: time of interview: start minute 
# v278c_r: time of interview: start  
# v279a: time of interview: end hour 
# v279b: time of interview: end minute 
# v279c_r: time of interview: end 
# v279d_r: time of interview: duration in minutes 

times_to_drop = ['v277', 'v278b', 'v278c_r', 'v279a', 'v279b', 'v279c_r']

df_train.drop(columns=times_to_drop, inplace=True)
df_test.drop(columns=times_to_drop, inplace=True)

#######################################################################################################################################

# %% [markdown]
# ### Age related variables group into intervals

# %%
# v241, v242
# more to add

# %% [markdown]
# ### Imputation / String variable drop

# %%
######################################## EDA - JaiYeon ################################################################################
#columns_to_drop = ['v228b', 'v231b', 'v233b', 'v251b', 'f252_edulvlb_CH', 'v275b_N1', 'v275b_N2', 'v275c_N2', 'v281a']
columns_to_drop = ['f252_edulvlb_CH']
df_train.drop(columns=columns_to_drop, inplace=True)
df_test.drop(columns=columns_to_drop, inplace=True)
## Try one hot encoding
num_to_drop = ['v228b_r','v231b_r','v233b_r','v251b_r','v275c_N2', 'v275c_N1', 'v281a_r']
df_train.drop(columns=num_to_drop, inplace=True)
df_test.drop(columns=num_to_drop, inplace=True)

columns_to_encode = ['v228b', 'v231b', 'v233b', 'v251b', 'v275b_N1', 'v275b_N2', 'v281a']
df_train = pd.get_dummies(df_train, columns=columns_to_encode)
df_test = pd.get_dummies(df_test, columns=columns_to_encode)
df_train = df_train.reindex(columns = sorted(df_train.columns))
df_test = df_test.reindex(columns = sorted(df_test.columns))

## removed the column having 'GB'
df_train.drop(list(df_train.filter(regex='DE')), axis=1, inplace=True)
df_test.drop(list(df_test.filter(regex='DE')), axis=1, inplace=True)

## removed the column having 'GB'
df_train.drop(list(df_train.filter(regex='GB')), axis=1, inplace=True)
df_test.drop(list(df_test.filter(regex='GB')), axis=1, inplace=True)

# Imputation 
df_train.fillna({'v231b_r': -3}, inplace=True)
df_test.fillna({'v231b_r': -3}, inplace=True)

df_train.fillna({'v233b_r': -3}, inplace=True)
df_test.fillna({'v233b_r': -3}, inplace=True)

df_train.fillna({'v251b_r': -3}, inplace=True)
df_test.fillna({'v251b_r': -3}, inplace=True)

df_train.fillna({'v228b_r': -3}, inplace=True)
df_test.fillna({'v228b_r': -3}, inplace=True)
# %%
######################################## EDA - JEONGHAN ########################################
merge_colname = find_colname_end(df_train, '_11c')
merge_columns(df_train, merge_colname)
merge_columns(df_test, merge_colname)
# print(find_colname(train_x_raw, 'c', 'endwith'))
# print(find_colname(train_x_raw, '_r', 'endwith'))
### Find variables containing _cs and do SimpleAggregation
# print(find_colname(df_train, '_cs', 'endwith'))
#aggregatecol = find_colname_end(df_train, '_cs')
#simpleAggregation(aggregatecol) #### TRAIN/TEST BOTH APPLICABLE

timeEDA(df_train)
timeEDA(df_test)
####################################################################################################
# %%
