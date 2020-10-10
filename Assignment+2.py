
# coding: utf-8

# ---
# 
# _You are currently looking at **version 1.2** of this notebook. To download notebooks and datafiles, as well as get help on Jupyter notebooks in the Coursera platform, visit the [Jupyter Notebook FAQ](https://www.coursera.org/learn/python-data-analysis/resources/0dhYG) course resource._
# 
# ---

# # Assignment 2 - Pandas Introduction
# All questions are weighted the same in this assignment.
# ## Part 1
# The following code loads the olympics dataset (olympics.csv), which was derrived from the Wikipedia entry on [All Time Olympic Games Medals](https://en.wikipedia.org/wiki/All-time_Olympic_Games_medal_table), and does some basic data cleaning. 
# 
# The columns are organized as # of Summer games, Summer medals, # of Winter games, Winter medals, total # number of games, total # of medals. Use this dataset to answer the questions below.

# In[75]:


import pandas as pd

df = pd.read_csv('olympics.csv', index_col=0, skiprows=1)

for col in df.columns:
    if col[:2]=='01':
        df.rename(columns={col:'Gold'+col[4:]}, inplace=True)
    if col[:2]=='02':
        df.rename(columns={col:'Silver'+col[4:]}, inplace=True)
    if col[:2]=='03':
        df.rename(columns={col:'Bronze'+col[4:]}, inplace=True)
    if col[:1]=='№':
        df.rename(columns={col:'#'+col[1:]}, inplace=True)

names_ids = df.index.str.split('\s\(') 

df.index = names_ids.str[0] 
df['ID'] = names_ids.str[1].str[:3] 

df = df.drop('Totals')
df.head()


# ### Question 0 (Example)
# 
# What is the first country in df?
# 
# *This function should return a Series.*

# In[76]:


def answer_zero():
    return df.iloc[0]

answer_zero()


# ### Question 1
# Which country has won the most gold medals in summer games?
# 
# *This function should return a single string value.*

# In[77]:


def answer_one():
    x = max(df['Gold'])
    answer = df[df['Gold'] == x].index.tolist()
    return answer[0]

answer_one()


# ### Question 2
# Which country had the biggest difference between their summer and winter gold medal counts?
# 
# *This function should return a single string value.*

# In[78]:


def answer_two():
    x = max(df['Gold'] - df['Gold.1'])
    answer = df[(df['Gold'] - df['Gold.1']) == x].index.tolist()
    return answer[0]

answer_two()


# ### Question 3
# Which country has the biggest difference between their summer gold medal counts and winter gold medal counts relative to their total gold medal count? 
# 
# $$\frac{Summer~Gold - Winter~Gold}{Total~Gold}$$
# 
# Only include countries that have won at least 1 gold in both summer and winter.
# 
# *This function should return a single string value.*

# In[79]:


def answer_three():
    df_has_gold = df[(df['Gold']>0) & (df['Gold.1']>0)]
    df_max_diff = (abs(df_has_gold['Gold']-df_has_gold['Gold.1'])/df_has_gold['Gold.2'])
    return df_max_diff.idxmax()

answer_three()


# ### Question 4
# Write a function that creates a Series called "Points" which is a weighted value where each gold medal (`Gold.2`) counts for 3 points, silver medals (`Silver.2`) for 2 points, and bronze medals (`Bronze.2`) for 1 point. The function should return only the column (a Series object) which you created, with the country names as indices.
# 
# *This function should return a Series named `Points` of length 146*

# In[80]:


def answer_four():
    points = 3*df['Gold.2'] + 2*df['Silver.2'] + 1*df['Bronze.2']
    return points

answer_four()


# ## Part 2
# For the next set of questions, we will be using census data from the [United States Census Bureau](http://www.census.gov). Counties are political and geographic subdivisions of states in the United States. This dataset contains population data for counties and states in the US from 2010 to 2015. [See this document](https://www2.census.gov/programs-surveys/popest/technical-documentation/file-layouts/2010-2015/co-est2015-alldata.pdf) for a description of the variable names.
# 
# The census dataset (census.csv) should be loaded as census_df. Answer questions using this as appropriate.
# 
# ### Question 5
# Which state has the most counties in it? (hint: consider the sumlevel key carefully! You'll need this for future questions too...)
# 
# *This function should return a single string value.*

# In[81]:


census_df = pd.read_csv('census.csv')
census_df.head()


# In[82]:


def answer_five():
    counties_df = census_df[census_df['SUMLEV'] == 50]
    x = counties_df.groupby('STNAME').count()['SUMLEV']
    answer = x.idxmax()
    return answer

answer_five()


# ### Question 6
# **Only looking at the three most populous counties for each state**, what are the three most populous states (in order of highest population to lowest population)? Use `CENSUS2010POP`.
# 
# *This function should return a list of string values.*

# In[83]:


def answer_six():
    counties_df = census_df[census_df['SUMLEV'] == 50]
    top_counties_df = counties_df.sort_values(by=['STNAME','CENSUS2010POP'],ascending=False).groupby('STNAME').head(3)
    answer = top_counties_df.groupby('STNAME').sum().sort_values(by='CENSUS2010POP').head(3).index.tolist()
    return answer

answer_six()


# ### Question 7
# Which county has had the largest absolute change in population within the period 2010-2015? (Hint: population values are stored in columns POPESTIMATE2010 through POPESTIMATE2015, you need to consider all six columns.)
# 
# e.g. If County Population in the 5 year period is 100, 120, 80, 105, 100, 130, then its largest change in the period would be |130-80| = 50.
# 
# *This function should return a single string value.*

# In[84]:


def answer_seven():
    counties_df = census_df[census_df['SUMLEV'] == 50]
    counties_df['pop_change'] = abs(counties_df['POPESTIMATE2015'] - counties_df['POPESTIMATE2014'])+abs(counties_df['POPESTIMATE2014'] - counties_df['POPESTIMATE2013'])+abs(counties_df['POPESTIMATE2013'] - counties_df['POPESTIMATE2012'])+abs(counties_df['POPESTIMATE2012'] - counties_df['POPESTIMATE2011'])+abs(counties_df['POPESTIMATE2011'] - counties_df['POPESTIMATE2010'])
    x = max(counties_df['pop_change'])
    answer = counties_df['CTYNAME'][counties_df['pop_change']==x].tolist()
    return answer[0]


answer_seven()


# ### Question 8
# In this datafile, the United States is broken up into four regions using the "REGION" column. 
# 
# Create a query that finds the counties that belong to regions 1 or 2, whose name starts with 'Washington', and whose POPESTIMATE2015 was greater than their POPESTIMATE 2014.
# 
# *This function should return a 5x2 DataFrame with the columns = ['STNAME', 'CTYNAME'] and the same index ID as the census_df (sorted ascending by index).*

# In[86]:


def answer_eight():
    counties_df = census_df[census_df['SUMLEV'] == 50]
    answer = counties_df[((counties_df['REGION']==1)|(counties_df['REGION']==2))&
                         (counties_df['CTYNAME']=='Washington County')&
                         (counties_df['POPESTIMATE2015']>counties_df['POPESTIMATE2014'])][['STNAME','CTYNAME']]
    return answer

answer_eight()


# In[ ]:



