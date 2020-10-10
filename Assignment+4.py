
# coding: utf-8

# ---
# 
# _You are currently looking at **version 1.1** of this notebook. To download notebooks and datafiles, as well as get help on Jupyter notebooks in the Coursera platform, visit the [Jupyter Notebook FAQ](https://www.coursera.org/learn/python-data-analysis/resources/0dhYG) course resource._
# 
# ---

# In[1]:


import pandas as pd
import numpy as np
import re
from scipy.stats import ttest_ind


# # Assignment 4 - Hypothesis Testing
# This assignment requires more individual learning than previous assignments - you are encouraged to check out the [pandas documentation](http://pandas.pydata.org/pandas-docs/stable/) to find functions or methods you might not have used yet, or ask questions on [Stack Overflow](http://stackoverflow.com/) and tag them as pandas and python related. And of course, the discussion forums are open for interaction with your peers and the course staff.
# 
# Definitions:
# * A _quarter_ is a specific three month period, Q1 is January through March, Q2 is April through June, Q3 is July through September, Q4 is October through December.
# * A _recession_ is defined as starting with two consecutive quarters of GDP decline, and ending with two consecutive quarters of GDP growth.
# * A _recession bottom_ is the quarter within a recession which had the lowest GDP.
# * A _university town_ is a city which has a high percentage of university students compared to the total population of the city.
# 
# **Hypothesis**: University towns have their mean housing prices less effected by recessions. Run a t-test to compare the ratio of the mean price of houses in university towns the quarter before the recession starts compared to the recession bottom. (`price_ratio=quarter_before_recession/recession_bottom`)
# 
# The following data files are available for this assignment:
# * From the [Zillow research data site](http://www.zillow.com/research/data/) there is housing data for the United States. In particular the datafile for [all homes at a city level](http://files.zillowstatic.com/research/public/City/City_Zhvi_AllHomes.csv), ```City_Zhvi_AllHomes.csv```, has median home sale prices at a fine grained level.
# * From the Wikipedia page on college towns is a list of [university towns in the United States](https://en.wikipedia.org/wiki/List_of_college_towns#College_towns_in_the_United_States) which has been copy and pasted into the file ```university_towns.txt```.
# * From Bureau of Economic Analysis, US Department of Commerce, the [GDP over time](http://www.bea.gov/national/index.htm#gdp) of the United States in current dollars (use the chained value in 2009 dollars), in quarterly intervals, in the file ```gdplev.xls```. For this assignment, only look at GDP data from the first quarter of 2000 onward.
# 
# Each function in this assignment below is worth 10%, with the exception of ```run_ttest()```, which is worth 50%.

# In[2]:


states = {'OH': 'Ohio', 'KY': 'Kentucky', 'AS': 'American Samoa', 'NV': 'Nevada', 'WY': 'Wyoming', 'NA': 'National', 
          'AL': 'Alabama', 'MD': 'Maryland', 'AK': 'Alaska', 'UT': 'Utah', 'OR': 'Oregon', 'MT': 'Montana', 
          'IL': 'Illinois', 'TN': 'Tennessee', 'DC': 'District of Columbia', 'VT': 'Vermont', 'ID': 'Idaho', 
          'AR': 'Arkansas', 'ME': 'Maine', 'WA': 'Washington', 'HI': 'Hawaii', 'WI': 'Wisconsin', 'MI': 'Michigan', 
          'IN': 'Indiana', 'NJ': 'New Jersey', 'AZ': 'Arizona', 'GU': 'Guam', 'MS': 'Mississippi', 'PR': 'Puerto Rico',
          'NC': 'North Carolina', 'TX': 'Texas', 'SD': 'South Dakota', 'MP': 'Northern Mariana Islands', 'IA': 'Iowa',
          'MO': 'Missouri', 'CT': 'Connecticut', 'WV': 'West Virginia', 'SC': 'South Carolina', 'LA': 'Louisiana', 
          'KS': 'Kansas', 'NY': 'New York', 'NE': 'Nebraska', 'OK': 'Oklahoma', 'FL': 'Florida', 'CA': 'California',
          'CO': 'Colorado', 'PA': 'Pennsylvania', 'DE': 'Delaware', 'NM': 'New Mexico', 'RI': 'Rhode Island', 
          'MN': 'Minnesota', 'VI': 'Virgin Islands', 'NH': 'New Hampshire', 'MA': 'Massachusetts', 'GA': 'Georgia', 
          'ND': 'North Dakota', 'VA': 'Virginia'}


# In[3]:


import pandas as pd
def get_list_of_university_towns():
    
    data = []
    file = open('university_towns.txt')
    for line in file:
        data.append(line[:-1])
    names = []
    for line in data:
        if line[-6:] == '[edit]':
            state_name = line[:-6]
        elif '(' in line:
            town_name = line[:line.index('(')-1]
            names.append([state_name, town_name])
        else:
            town_name = line
            names.append([state_name, town_name])
    df = pd.DataFrame(names, columns = ['State', 'RegionName'])
    return df
            
get_list_of_university_towns()


# In[4]:


import pandas as pd
def get_recession_start():
    '''Returns the year and quarter of the recession start time as a 
    string value in a format such as 2005q3'''
    gdp = pd.read_excel('gdplev.xls', skiprows = 219, usecols=[4,6],names=['Quarter', 'GDP'])
    quarters = []
    for i in range(len(gdp) - 2):
        if (gdp.iloc[i][1] > gdp.iloc[i+1][1]) & (gdp.iloc[i+1][1] > gdp.iloc[i+2][1]):
            quarters.append(gdp.iloc[i][0])
    return quarters[0]

get_recession_start()


# In[5]:


def get_recession_end():
    '''Returns the year and quarter of the recession end time as a 
    string value in a format such as 2005q3'''
    gdp = pd.read_excel('gdplev.xls', skiprows = 7, usecols= {'Unnamed: 4', 'Unnamed: 6'})
    gdp = gdp.rename(columns = {'Unnamed: 4': 'Quarter', 'Unnamed: 6': 'GDP'})
    start = get_recession_start()
    start_index = gdp[gdp['Quarter']==start].index.tolist()[0]
    gdp = gdp.iloc[start_index:]
    
    for i in range(2, len(gdp)):
        if (gdp.iloc[i-2][1] < gdp.iloc[i-1][1]) & (gdp.iloc[i-1][1] < gdp.iloc[i][1]):
            return gdp.iloc[i][0]
    
get_recession_end()


# In[6]:


def get_recession_bottom():
    '''Returns the year and quarter of the recession bottom time as a 
    string value in a format such as 2005q3'''
    gdp = pd.read_excel('gdplev.xls', skiprows = 7, usecols= {'Unnamed: 4', 'Unnamed: 6'})
    gdp = gdp.rename(columns = {'Unnamed: 4': 'Quarter', 'Unnamed: 6': 'GDP'})
    
    start = get_recession_start()
    start_index = gdp[gdp['Quarter']==start].index.tolist()[0]
    
    end = get_recession_end()
    end_index = gdp[gdp['Quarter'] == end].index.tolist()[0]
    
    gdp = gdp.iloc[start_index : end_index+1]
    
    bottom = gdp['GDP'].min()
    bottom_index = gdp[gdp['GDP'] == bottom].index.tolist()[0] - start_index
    
    return gdp.iloc[bottom_index]['Quarter']

get_recession_bottom()


# In[7]:


housing = pd.read_csv('City_Zhvi_AllHomes.csv')
pd.set_option('max_columns', None)
housing.head()


# In[8]:


import pandas as pd
def convert_housing_data_to_quarters():
    '''Converts the housing data to quarters and returns it as mean 
    values in a dataframe. This dataframe should be a dataframe with
    columns for 2000q1 through 2016q3, and should have a multi-index
    in the shape of ["State","RegionName"].
    
    Note: Quarters are defined in the assignment description, they are
    not arbitrary three month periods.
    
    The resulting dataframe should have 67 columns, and 10,730 rows.
    '''
   
    housing = pd.read_csv('City_Zhvi_AllHomes.csv')
    housing = housing.drop(housing.columns[[0]+list(range(3,51))],axis=1)
    housing2 = pd.DataFrame(housing[['State','RegionName']])
    for year in range(2000,2016):
        housing2[str(year)+'q1'] = housing[[str(year)+'-01',str(year)+'-02',str(year)+'-03']].mean(axis=1)
        housing2[str(year)+'q2'] = housing[[str(year)+'-04',str(year)+'-05',str(year)+'-06']].mean(axis=1)
        housing2[str(year)+'q3'] = housing[[str(year)+'-07',str(year)+'-08',str(year)+'-09']].mean(axis=1)
        housing2[str(year)+'q4'] = housing[[str(year)+'-10',str(year)+'-11',str(year)+'-12']].mean(axis=1)
    year = 2016    
    housing2[str(year)+'q1'] = housing[[str(year)+'-01',str(year)+'-02',str(year)+'-03']].mean(axis=1)
    housing2[str(year)+'q2'] = housing[[str(year)+'-04',str(year)+'-05',str(year)+'-06']].mean(axis=1)
    housing2[str(year)+'q3'] = housing[[str(year)+'-07',str(year)+'-08']].mean(axis=1)
    housing2 = housing2.replace({'State':states})
    housing2 = housing2.set_index(['State','RegionName'])
    return housing2

convert_housing_data_to_quarters()


# In[27]:


from scipy import stats
def run_ttest():  
    unitowns = get_list_of_university_towns()
    bottom = get_recession_bottom()
    start = get_recession_start()
    housing = convert_housing_data_to_quarters()
    bstart = housing.columns[housing.columns.get_loc(start) -1]
    
    housing['ratio'] = housing[bottom] - housing[bstart]
    housing = housing[[bottom,bstart,'ratio']]
    housing = housing.reset_index()
    housing_unitowns = pd.merge(housing,unitowns,how='inner',on=['State','RegionName'])
    housing_unitowns['uni'] = True
    df2 = pd.merge(housing,housing_unitowns,how='outer',on=['State','RegionName',bottom,bstart,'ratio'])
    df2['uni'] = df2['uni'].fillna(False)

    ut = df2[df2['uni'] == True]
    nut = df2[df2['uni'] == False]

    st,p = ttest_ind(ut['ratio'].dropna(),nut['ratio'].dropna())
    
    different = True if p < 0.01 else False

    better = "non-university town" if ut['ratio'].mean() < nut['ratio'].mean() else "university town"

    return different, p, better

run_ttest()


# In[ ]:




