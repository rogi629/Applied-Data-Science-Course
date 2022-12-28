#!/usr/bin/env python
# coding: utf-8

# # Assignment 3
# All questions are weighted the same in this assignment. This assignment requires more individual learning then the last one did - you are encouraged to check out the [pandas documentation](http://pandas.pydata.org/pandas-docs/stable/) to find functions or methods you might not have used yet, or ask questions on [Stack Overflow](http://stackoverflow.com/) and tag them as pandas and python related. All questions are worth the same number of points except question 1 which is worth 17% of the assignment grade.
# 
# **Note**: Questions 3-13 rely on your question 1 answer.

# In[1]:


import pandas as pd
import numpy as np

# Filter all warnings. If you would like to see the warnings, please comment the two lines below.
import warnings
warnings.filterwarnings('ignore')


# ### Question 1
# Load the energy data from the file `assets/Energy Indicators.xls`, which is a list of indicators of [energy supply and renewable electricity production](assets/Energy%20Indicators.xls) from the [United Nations](http://unstats.un.org/unsd/environment/excel_file_tables/2013/Energy%20Indicators.xls) for the year 2013, and should be put into a DataFrame with the variable name of **Energy**.
# 
# Keep in mind that this is an Excel file, and not a comma separated values file. Also, make sure to exclude the footer and header information from the datafile. The first two columns are unneccessary, so you should get rid of them, and you should change the column labels so that the columns are:
# 
# `['Country', 'Energy Supply', 'Energy Supply per Capita', '% Renewable]`
# 
# Convert `Energy Supply` to gigajoules (**Note: there are 1,000,000 gigajoules in a petajoule**). For all countries which have missing data (e.g. data with "...") make sure this is reflected as `np.NaN` values.
# 
# Rename the following list of countries (for use in later questions):
# 
# ```"Republic of Korea": "South Korea",
# "United States of America": "United States",
# "United Kingdom of Great Britain and Northern Ireland": "United Kingdom",
# "China, Hong Kong Special Administrative Region": "Hong Kong"```
# 
# There are also several countries with numbers and/or parenthesis in their name. Be sure to remove these, e.g. `'Bolivia (Plurinational State of)'` should be `'Bolivia'`.  `'Switzerland17'` should be `'Switzerland'`.
# 
# Next, load the GDP data from the file `assets/world_bank.csv`, which is a csv containing countries' GDP from 1960 to 2015 from [World Bank](http://data.worldbank.org/indicator/NY.GDP.MKTP.CD). Call this DataFrame **GDP**. 
# 
# Make sure to skip the header, and rename the following list of countries:
# 
# ```"Korea, Rep.": "South Korea", 
# "Iran, Islamic Rep.": "Iran",
# "Hong Kong SAR, China": "Hong Kong"```
# 
# Finally, load the [Sciamgo Journal and Country Rank data for Energy Engineering and Power Technology](http://www.scimagojr.com/countryrank.php?category=2102) from the file `assets/scimagojr-3.xlsx`, which ranks countries based on their journal contributions in the aforementioned area. Call this DataFrame **ScimEn**.
# 
# Join the three datasets: GDP, Energy, and ScimEn into a new dataset (using the intersection of country names). Use only the last 10 years (2006-2015) of GDP data and only the top 15 countries by Scimagojr 'Rank' (Rank 1 through 15). 
# 
# The index of this DataFrame should be the name of the country, and the columns should be ['Rank', 'Documents', 'Citable documents', 'Citations', 'Self-citations',
#        'Citations per document', 'H index', 'Energy Supply',
#        'Energy Supply per Capita', '% Renewable', '2006', '2007', '2008',
#        '2009', '2010', '2011', '2012', '2013', '2014', '2015'].
# 
# *This function should return a DataFrame with 20 columns and 15 entries, and the rows of the DataFrame should be sorted by "Rank".*
# Let's look at an example. First, we'll bring in our pandas and numpy libraries
import pandas as pd
import numpy as np

###This part of the code is to clean up and format the Energy Indicators.xls file into DataFrame 'Energy'
df = pd.read_excel('assets/Energy Indicators.xls')
df = df[['Unnamed: 2', 'Unnamed: 3', 'Unnamed: 4', 'Unnamed: 5']]
#rename columns to ['Country', 'Energy Supply', 'Energy Supply per Capita', '% Renewable]
df = df.rename(columns={'Unnamed: 2': 'Country', 'Unnamed: 3': 'Energy Supply',
                        'Unnamed: 4': 'Energy Supply per Capita', 'Unnamed: 5': '% Renewable'})
df = df.replace(['...'], [np.nan])
#set the index to country to make some special changes to the names
df = df.set_index('Country')
df = df.rename(index={"Republic of Korea": "South Korea",
                      "United States of America20": "United States", 
                      "United Kingdom of Great Britain and Northern Ireland19": "United Kingdom",
                      "China, Hong Kong Special Administrative Region3": "Hong Kong",
                      "China, Macao Special Administrative Region4": "Macao"})
#Reset the index so we can do column string manipulation (probably a way to do this on the index)
df = df.reset_index()
df['Country'] = df['Country'].str.extract('([a-zA-Z\s]+)')
#Test = df[df['Country'].isna()]
#Setting the index back to Country
df = df.set_index('Country')
df = df.rename(index={"Macao": "China, Macao Special Administrative Region"})
df['Energy Supply'] = df['Energy Supply']*1000000
Energy = df.iloc[17:-38]
Energy = Energy.rename(mapper=str.strip, axis='index')
Energy['Energy Supply'] = Energy['Energy Supply'].astype(float)
Energy['Energy Supply per Capita'] = Energy['Energy Supply per Capita'].astype(float)
Energy1 = Energy.reset_index()
Energy1

country_list = ['Australia', 'Bolivia', 'China', 'Hong Kong', 'China, Macao Special Administrative Region', 'Denmark', 'Falkland Islands', 'France', 'Greenland', 'Indonesia', 'Iran', 'Italy', 'Japan', 'Kuwait', 'Micronesia', 'Netherlands', 'Portugal', 'South Korea', 'Saudi Arabia', 'Serbia', 'Sint Maarten', 'Spain', 'Switzerland', 'Ukraine', 'United Kingdom', 'United States', 'Venezuela']

for i in range(len(country_list)):
    if country_list[i] not in Energy.index.values.tolist():
        print(country_list[i])
Energy###This part of the code is to clean up and format the world_bank.csv file into DataFrame 'GDP'
df = pd.read_csv('assets/world_bank.csv')
df.columns = df.iloc[3]
df = df.iloc[4:]
df = df.rename(columns={'Country Name': 'Country'})
df.set_index('Country', inplace=True)
GDP = df.rename(index={"Korea, Rep.": "South Korea", 
          "Iran, Islamic Rep.": "Iran",
          "Hong Kong SAR, China": "Hong Kong"})
GDP = GDP.rename(mapper=str.strip, axis='index')
GDP = GDP[[2006., 2007, 2008, 2009, 2010, 2011, 2012, 2013, 2014, 2015]]
GDP = GDP.rename(columns={2006:'2006', 2007:'2007', 2008:'2008', 2009:'2009', 2010:'2010',
                          2011:'2011', 2012:'2012', 2013:'2013', 2014:'2014', 2015:'2015'})
GDP1 = GDP.reset_index()###This part of the code is to clean up and format the scimagojr-3.xlsx file into DataFrame 'ScimEn'
ScimEn = pd.read_excel('assets/scimagojr-3.xlsx', index_col= 0)
ScimEn = ScimEn.reset_index()
ScimEn1 = ScimEn.iloc[:15]
ScimEn
#ScimEn.set_index('Country', inplace=True)
#ScimEn.loc['Macao']#Merge Dataframes Energy, GDP, and ScimEn on Country |The index of this DataFrame should be the name of the country,
#and the columns should be ['Rank', 'Documents', 'Citable documents', 'Citations', 'Self-citations', 
#'Citations per document', 'H index', 'Energy Supply', 'Energy Supply per Capita', '% Renewable', 
#'2006', '2007', '2008', '2009', '2010', '2011', '2012', '2013', '2014', '2015'].
new_df = pd.merge(ScimEn1, Energy1, how='left', on='Country')
new_df = pd.merge(new_df, GDP1, how='left', on='Country')
new_df = new_df.set_index('Country')
new_df
# In[2]:


# Let's look at an example. First, we'll bring in our pandas and numpy libraries
import pandas as pd
import numpy as np

###This part of the code is to clean up and format the Energy Indicators.xls file into DataFrame 'Energy'
df = pd.read_excel('assets/Energy Indicators.xls')
df = df[['Unnamed: 2', 'Unnamed: 3', 'Unnamed: 4', 'Unnamed: 5']]
#rename columns to ['Country', 'Energy Supply', 'Energy Supply per Capita', '% Renewable]
df = df.rename(columns={'Unnamed: 2': 'Country', 'Unnamed: 3': 'Energy Supply',
                        'Unnamed: 4': 'Energy Supply per Capita', 'Unnamed: 5': '% Renewable'})
df = df.replace(['...'], [np.nan])
#set the index to country to make some special changes to the names
df = df.set_index('Country')
df = df.rename(index={"Republic of Korea": "South Korea",
                      "United States of America20": "United States", 
                      "United Kingdom of Great Britain and Northern Ireland19": "United Kingdom",
                      "China, Hong Kong Special Administrative Region3": "Hong Kong",
                      "China, Macao Special Administrative Region4": "Macao"})
#Reset the index so we can do column string manipulation (probably a way to do this on the index)
df = df.reset_index()
df['Country'] = df['Country'].str.extract('([a-zA-Z\s]+)')
#Test = df[df['Country'].isna()]
#Setting the index back to Country
df = df.set_index('Country')
df = df.rename(index={"Macao": "China, Macao Special Administrative Region"})
df['Energy Supply'] = df['Energy Supply']*1000000
Energy = df.iloc[17:-38]
Energy = Energy.rename(mapper=str.strip, axis='index')
Energy['Energy Supply'] = Energy['Energy Supply'].astype(float)
Energy['Energy Supply per Capita'] = Energy['Energy Supply per Capita'].astype(float)
Energy1 = Energy.reset_index()
Energy1

country_list = ['Australia', 'Bolivia', 'China', 'Hong Kong', 'China, Macao Special Administrative Region', 'Denmark', 'Falkland Islands', 'France', 'Greenland', 'Indonesia', 'Iran', 'Italy', 'Japan', 'Kuwait', 'Micronesia', 'Netherlands', 'Portugal', 'South Korea', 'Saudi Arabia', 'Serbia', 'Sint Maarten', 'Spain', 'Switzerland', 'Ukraine', 'United Kingdom', 'United States', 'Venezuela']

for i in range(len(country_list)):
    if country_list[i] not in Energy.index.values.tolist():
        print(country_list[i])
Energy

###This part of the code is to clean up and format the world_bank.csv file into DataFrame 'GDP'
df = pd.read_csv('assets/world_bank.csv')
df.columns = df.iloc[3]
df = df.iloc[4:]
df = df.rename(columns={'Country Name': 'Country'})
df.set_index('Country', inplace=True)
GDP = df.rename(index={"Korea, Rep.": "South Korea", 
          "Iran, Islamic Rep.": "Iran",
          "Hong Kong SAR, China": "Hong Kong"})
GDP = GDP.rename(mapper=str.strip, axis='index')
GDP = GDP[[2006., 2007, 2008, 2009, 2010, 2011, 2012, 2013, 2014, 2015]]
GDP = GDP.rename(columns={2006:'2006', 2007:'2007', 2008:'2008', 2009:'2009', 2010:'2010',
                          2011:'2011', 2012:'2012', 2013:'2013', 2014:'2014', 2015:'2015'})
GDP1 = GDP.reset_index()

###This part of the code is to clean up and format the scimagojr-3.xlsx file into DataFrame 'ScimEn'
ScimEn = pd.read_excel('assets/scimagojr-3.xlsx', index_col= 0)
ScimEn = ScimEn.reset_index()
ScimEn1 = ScimEn.iloc[:15]
ScimEn
#ScimEn.set_index('Country', inplace=True)
#ScimEn.loc['Macao']

#Merge Dataframes Energy, GDP, and ScimEn on Country |The index of this DataFrame should be the name of the country,
#and the columns should be ['Rank', 'Documents', 'Citable documents', 'Citations', 'Self-citations', 
#'Citations per document', 'H index', 'Energy Supply', 'Energy Supply per Capita', '% Renewable', 
#'2006', '2007', '2008', '2009', '2010', '2011', '2012', '2013', '2014', '2015'].
new_df = pd.merge(ScimEn1, Energy1, how='left', on='Country')
new_df = pd.merge(new_df, GDP1, how='left', on='Country')
new_df = new_df.set_index('Country')
new_df

def answer_one():
    return new_df
    raise NotImplementedError()


# In[3]:


assert type(answer_one()) == pd.DataFrame, "Q1: You should return a DataFrame!"

assert answer_one().shape == (15,20), "Q1: Your DataFrame should have 20 columns and 15 entries!"


# In[4]:


# Cell for autograder.


# ### Question 2
# The previous question joined three datasets then reduced this to just the top 15 entries. When you joined the datasets, but before you reduced this to the top 15 items, how many entries did you lose?
# 
# *This function should return a single number.*

# In[5]:


get_ipython().run_cell_magic('HTML', '', '<svg width="800" height="300">\n  <circle cx="150" cy="180" r="80" fill-opacity="0.2" stroke="black" stroke-width="2" fill="blue" />\n  <circle cx="200" cy="100" r="80" fill-opacity="0.2" stroke="black" stroke-width="2" fill="red" />\n  <circle cx="100" cy="100" r="80" fill-opacity="0.2" stroke="black" stroke-width="2" fill="green" />\n  <line x1="150" y1="125" x2="300" y2="150" stroke="black" stroke-width="2" fill="black" stroke-dasharray="5,3"/>\n  <text x="300" y="165" font-family="Verdana" font-size="35">Everything but this!</text>\n</svg>')

inner_df = pd.merge(GDP1, Energy1, how='inner', on='Country')
inner_df = pd.merge(inner_df, ScimEn, how='inner', on='Country')
inner_df = inner_df.set_index('Country')
icount = 0
for rows in inner_df.T:
    icount+=1
print(icount)
inner_dfout_df = pd.merge(GDP1, Energy1, how='outer', on='Country')
out_df = pd.merge(out_df, ScimEn, how='outer', on='Country')
out_df = out_df.set_index('Country')
ocount = 0
for rows in out_df.T:
    ocount+=1
print(ocount)
#out_df
diff = ocount-icount-1
print(diff)
# In[6]:


inner_df = pd.merge(GDP1, Energy1, how='inner', on='Country')
inner_df = pd.merge(inner_df, ScimEn, how='inner', on='Country')
inner_df = inner_df.set_index('Country')
icount = 0
for rows in inner_df.T:
    icount+=1
print(icount)
inner_df

out_df = pd.merge(GDP1, Energy1, how='outer', on='Country')
out_df = pd.merge(out_df, ScimEn, how='outer', on='Country')
out_df = out_df.set_index('Country')
ocount = 0
for rows in out_df.T:
    ocount+=1
print(ocount)
#out_df
diff = ocount-icount-1
print(diff)

def answer_two():
    return diff
    raise NotImplementedError()


# In[7]:


assert type(answer_two()) == int, "Q2: You should return an int number!"


# ### Question 3
# What are the top 15 countries for average GDP over the last 10 years?
# 
# *This function should return a Series named `avgGDP` with 15 countries and their average GDP sorted in descending order.*
columns = ['2006', '2007', '2008', '2009', '2010', '2011', '2012', '2013', '2014', '2015']
GDP1['AvgGDP'] = GDP1.apply(lambda x: np.mean(x[columns]), axis=1)
GDP1 = GDP1.sort_values('AvgGDP')
GDP1.dropna(inplace=True)
GDP1 = GDP1.reset_index()
GDP1 = GDP1.set_index('Country')
GDP2 = GDP1[:-13]
GDP2.drop('Late-demographic dividend', axis=0, inplace=True)
GDP2.drop('Euro area', axis=0, inplace=True)
GDP2.drop('Early-demographic dividend', axis=0, inplace=True)
GDP2.drop('East Asia & Pacific (excluding high income)', axis=0, inplace=True)
GDP2.drop('East Asia & Pacific (IDA & IBRD countries)', axis=0, inplace=True)
GDP2.drop('Latin America & Caribbean', axis=0, inplace=True)
GDP2.drop('Latin America & the Caribbean (IDA & IBRD countries)', axis=0, inplace=True)
GDP2.drop('Lower middle income', axis=0, inplace=True)
GDP2.drop('Latin America & Caribbean (excluding high income)', axis=0, inplace=True)
GDP2.drop('Europe & Central Asia (IDA & IBRD countries)', axis=0, inplace=True)
GDP2.drop('Europe & Central Asia (excluding high income)', axis=0, inplace=True)
GDP2.drop('Middle East & North Africa', axis=0, inplace=True)
GDP2.drop('South Asia (IDA & IBRD)', axis=0, inplace=True)
GDP2.drop('South Asia', axis=0, inplace=True)
GDP2.drop('Arab World', axis=0, inplace=True)
GDP2.drop('IDA total', axis=0, inplace=True)
GDP2.drop('Sub-Saharan Africa', axis=0, inplace=True)
GDP2.drop('Sub-Saharan Africa (IDA & IBRD countries)', axis=0, inplace=True)
GDP2.drop('Sub-Saharan Africa (excluding high income)', axis=0, inplace=True)
GDP2.drop('Central Europe and the Baltics', axis=0, inplace=True)
GDP2 = GDP2.iloc[-15:]
GDP2 = GDP2.sort_values('AvgGDP', ascending=False)
GDP2['10YR Diff'] = np.absolute(GDP2['2015']-GDP2['2006'])
avgGDP = GDP2['AvgGDP']
#print(type(avgGDP))
GDP2# columns = ['2006', '2007', '2008', '2009', '2010', '2011', '2012', '2013', '2014', '2015']
new_df['avgGDP'] = new_df.apply(lambda x: np.mean(x[columns]), axis=1)
new_df['10YR Diff'] = np.absolute(new_df['2015']-new_df['2006'])
new_df.sort_values('avgGDP', ascending = False, inplace=True)
#new_df
#print(new_df)
avgGDP = new_df['avgGDP']
avgGDP
#test_df = new_df.drop(columns, axis = 1)
#test_df
# In[8]:


import pandas as pd
import numpy as np

def answer_three():
    columns = ['2006', '2007', '2008', '2009', '2010', '2011', '2012', '2013', '2014', '2015']
    new_df['avgGDP'] = new_df.apply(lambda x: np.mean(x[columns]), axis=1)
    new_df['10YR Diff'] = np.absolute(new_df['2015']-new_df['2006'])
    new_df.sort_values('avgGDP', ascending = False, inplace=True)
    #new_df
    #print(new_df)
    avgGDP = new_df['avgGDP']
    avgGDP
    #test_df = new_df.drop(columns, axis = 1)
    #test_df
    return avgGDP
    #raise NotImplementedError()


# In[9]:


assert type(answer_three()) == pd.Series, "Q3: You should return a Series!"


# ### Question 4
# By how much had the GDP changed over the 10 year span for the country with the 6th largest average GDP?
# 
# *This function should return a single number.*
new_df.sort_values('avgGDP', inplace=True)
new_df
sixth_country = new_df.iloc[-6]['10YR Diff']
sixth_country
# In[10]:


new_df.sort_values('avgGDP', inplace=True)
new_df
sixth_country = new_df.iloc[-6]['10YR Diff']
sixth_country

def answer_four():
    return sixth_country
    raise NotImplementedError()


# In[11]:


# Cell for autograder.


# ### Question 5
# What is the mean energy supply per capita?
# 
# *This function should return a single number.*

# In[12]:


ESCmean = new_df['Energy Supply per Capita'].mean()
ESCmean


# In[13]:


def answer_five():
    return ESCmean
    raise NotImplementedError()


# In[14]:


# Cell for autograder.


# ### Question 6
# What country has the maximum % Renewable and what is the percentage?
# 
# *This function should return a tuple with the name of the country and the percentage.*
new_df['% Renewable'].max()
maxRen = new_df[new_df['% Renewable'] > 69]
maxRen.reset_index(inplace=True)
maxRen = maxRen.set_index(['Country', '% Renewable'])
lst = []
for group, frame in maxRen.groupby(level=(0,1)):
    lst.append(group)
lst[0]
# In[15]:


new_df['% Renewable'].max()
maxRen = new_df[new_df['% Renewable'] > 69]
maxRen.reset_index(inplace=True)
maxRen = maxRen.set_index(['Country', '% Renewable'])
lst = []
for group, frame in maxRen.groupby(level=(0,1)):
    lst.append(group)
lst[0]

def answer_six():
    return lst[0]
    raise NotImplementedError()


# In[16]:


assert type(answer_six()) == tuple, "Q6: You should return a tuple!"

assert type(answer_six()[0]) == str, "Q6: The first element in your result should be the name of the country!"


# ### Question 7
# Create a new column that is the ratio of Self-Citations to Total Citations. 
# What is the maximum value for this new column, and what country has the highest ratio?
# 
# *This function should return a tuple with the name of the country and the ratio.*
new_df['Ratio'] = np.absolute(new_df['Self-citations']/new_df['Citations'])
new_df['Ratio'].max()
ScimEnR = new_df[new_df['Ratio']>0.68]
ScimEnR.reset_index(inplace=True)
ScimEnR = ScimEnR.set_index(['Country', 'Ratio'])
ratio = []
for group, frame in ScimEnR.groupby(level=(0,1)):
    ratio.append(group)
ratio[0]
# In[17]:


new_df['Ratio'] = np.absolute(new_df['Self-citations']/new_df['Citations'])
new_df['Ratio'].max()
ScimEnR = new_df[new_df['Ratio']>0.68]
ScimEnR.reset_index(inplace=True)
ScimEnR = ScimEnR.set_index(['Country', 'Ratio'])
ratio = []
for group, frame in ScimEnR.groupby(level=(0,1)):
    ratio.append(group)
ratio[0]

def answer_seven():
    return ratio[0]
    raise NotImplementedError()


# In[18]:


assert type(answer_seven()) == tuple, "Q7: You should return a tuple!"

assert type(answer_seven()[0]) == str, "Q7: The first element in your result should be the name of the country!"


# ### Question 8
# 
# Create a column that estimates the population using Energy Supply and Energy Supply per capita. 
# What is the third most populous country according to this estimate?
# 
# *This function should return the name of the country*
new_df['PopEst'] = np.absolute(new_df['Energy Supply']/new_df['Energy Supply per Capita'])
new_df.sort_values('PopEst', inplace=True)
Energy3 = new_df.reset_index()
Energy3
ESC3 = Energy3['Country'].iloc[-3]

# In[19]:


new_df['PopEst'] = np.absolute(new_df['Energy Supply']/new_df['Energy Supply per Capita'])
new_df.sort_values('PopEst', inplace=True)
Energy3 = new_df.reset_index()
Energy3
ESC3 = Energy3['Country'].iloc[-3]

def answer_eight():
    return ESC3
    raise NotImplementedError()


# In[20]:


assert type(answer_eight()) == str, "Q8: You should return the name of the country!"


# ### Question 9
# Create a column that estimates the number of citable documents per person. 
# What is the correlation between the number of citable documents per capita and the energy supply per capita? Use the `.corr()` method, (Pearson's correlation).
# 
# *This function should return a single number.*
# 
# *(Optional: Use the built-in function `plot9()` to visualize the relationship between Energy Supply per Capita vs. Citable docs per Capita)*
#Corr_DF = pd.merge(ScimEn1, Energy1, how='left', on='Country')
#Corr_DF = pd.merge(Corr_DF, GDP1, how='left', on='Country')
#Corr_DF = Corr_DF.set_index('Country')
#Corr_DF
Corr_DF = new_df[new_df['PopEst'].notna()]
Corr_DF = Corr_DF[Corr_DF['PopEst']>0]

Corr_DF['Citable docs per Capita'] = np.absolute(Corr_DF['Citable documents']/Corr_DF['PopEst'])
Corr_DF.corr()

correlation = Corr_DF['Citable docs per Capita'].corr(Corr_DF['Energy Supply per Capita'])
#Corr_DF1 = Corr_DF[['Citable docs per Capita','Energy Supply per Capita']]
print(correlation)
Corr_DF
# In[21]:


#Corr_DF = pd.merge(ScimEn1, Energy1, how='left', on='Country')
#Corr_DF = pd.merge(Corr_DF, GDP1, how='left', on='Country')
#Corr_DF = Corr_DF.set_index('Country')
#Corr_DF
Corr_DF = new_df[new_df['PopEst'].notna()]
Corr_DF = Corr_DF[Corr_DF['PopEst']>0]

Corr_DF['Citable docs per Capita'] = np.absolute(Corr_DF['Citable documents']/Corr_DF['PopEst'])
Corr_DF.corr()

correlation = Corr_DF['Citable docs per Capita'].corr(Corr_DF['Energy Supply per Capita'])
#Corr_DF1 = Corr_DF[['Citable docs per Capita','Energy Supply per Capita']]
print(correlation)
Corr_DF

def answer_nine():
    return correlation
    raise NotImplementedError()


# In[22]:


def plot9():
    import matplotlib as plt
    get_ipython().run_line_magic('matplotlib', 'inline')
    
    Top15 = answer_one()
    Top15['PopEst'] = Top15['Energy Supply'] / Top15['Energy Supply per Capita']
    Top15['Citable docs per Capita'] = Top15['Citable documents'] / Top15['PopEst']
    Top15.plot(x='Citable docs per Capita', y='Energy Supply per Capita', kind='scatter', xlim=[0, 0.0006])


# In[23]:


plot9


# In[24]:


assert answer_nine() >= -1. and answer_nine() <= 1., "Q9: A valid correlation should between -1 to 1!"


# ### Question 10
# Create a new column with a 1 if the country's % Renewable value is at or above the median for all countries in the top 15, and a 0 if the country's % Renewable value is below the median.
# 
# *This function should return a series named `HighRenew` whose index is the country name sorted in ascending order of rank.*

# In[25]:


def compare_to_median(x):
    median = Corr_DF['% Renewable'].median()
    if x >= median:
        return 1
    else:
        return 0
Corr_DF.sort_values('Rank', inplace=True)
Corr_DF['Comparison'] = Corr_DF['% Renewable'].apply(lambda x: compare_to_median(x))
series10 = Corr_DF['Comparison']
print(series10)


# In[26]:


def answer_ten():
    return series10
    raise NotImplementedError()


# In[27]:


assert type(answer_ten()) == pd.Series, "Q10: You should return a Series!"


# ### Question 11
# Use the following dictionary to group the Countries by Continent, then create a DataFrame that displays the sample size (the number of countries in each continent bin), and the sum, mean, and std deviation for the estimated population of each country.
# 
# ```python
# ContinentDict  = {'China':'Asia', 
#                   'United States':'North America', 
#                   'Japan':'Asia', 
#                   'United Kingdom':'Europe', 
#                   'Russian Federation':'Europe', 
#                   'Canada':'North America', 
#                   'Germany':'Europe', 
#                   'India':'Asia',
#                   'France':'Europe', 
#                   'South Korea':'Asia', 
#                   'Italy':'Europe', 
#                   'Spain':'Europe', 
#                   'Iran':'Asia',
#                   'Australia':'Australia', 
#                   'Brazil':'South America'}
# ```
# 
# *This function should return a DataFrame with index named Continent `['Asia', 'Australia', 'Europe', 'North America', 'South America']` and columns `['size', 'sum', 'mean', 'std']`*
ContinentDict  = {'China':'Asia', 
                  'United States':'North America', 
                  'Japan':'Asia', 
                  'United Kingdom':'Europe', 
                  'Russian Federation':'Europe', 
                  'Canada':'North America', 
                  'Germany':'Europe', 
                  'India':'Asia',
                  'France':'Europe', 
                  'South Korea':'Asia', 
                  'Italy':'Europe', 
                  'Spain':'Europe', 
                  'Iran':'Asia',
                  'Australia':'Australia', 
                  'Brazil':'South America'}
Asia =[]
NA = []
EU = []
SA = []
AUS = []
for key, item in ContinentDict.items():
    if item == 'Asia':
        Asia.append(key)
    elif item == 'North America':
        NA.append(key)
    elif item == 'Europe':
        EU.append(key)
    elif item == 'South America':
        SA.append(key)
    elif item == 'Australia':
        AUS.append(key)
def get_continent(x):
    if x in Asia:
        return 'Asia'
    if x in NA:
        return 'North America'
    if x in EU:
        return 'Europe'
    if x in SA:
        return 'South America'
    if x in AUS:
        return 'Australia'
    
tempdf = Corr_DF.reset_index()
tempdf['Continent'] = tempdf['Country'].apply(lambda x: get_continent(x))
tempdf
ContDF = tempdf.groupby('Continent').agg({'PopEst':(np.size, np.sum, np.mean, np.std)})
ContDF.columns = ContDF.columns.droplevel(0)
ContDF
#ContDF.droplevel('PopEst', axis=1)
# In[28]:


ContinentDict  = {'China':'Asia', 
                  'United States':'North America', 
                  'Japan':'Asia', 
                  'United Kingdom':'Europe', 
                  'Russian Federation':'Europe', 
                  'Canada':'North America', 
                  'Germany':'Europe', 
                  'India':'Asia',
                  'France':'Europe', 
                  'South Korea':'Asia', 
                  'Italy':'Europe', 
                  'Spain':'Europe', 
                  'Iran':'Asia',
                  'Australia':'Australia', 
                  'Brazil':'South America'}
Asia =[]
NA = []
EU = []
SA = []
AUS = []
for key, item in ContinentDict.items():
    if item == 'Asia':
        Asia.append(key)
    elif item == 'North America':
        NA.append(key)
    elif item == 'Europe':
        EU.append(key)
    elif item == 'South America':
        SA.append(key)
    elif item == 'Australia':
        AUS.append(key)
def get_continent(x):
    if x in Asia:
        return 'Asia'
    if x in NA:
        return 'North America'
    if x in EU:
        return 'Europe'
    if x in SA:
        return 'South America'
    if x in AUS:
        return 'Australia'
    
tempdf = Corr_DF.reset_index()
tempdf['Continent'] = tempdf['Country'].apply(lambda x: get_continent(x))
tempdf
ContDF = tempdf.groupby('Continent').agg({'PopEst':(np.size, np.sum, np.mean, np.std)})
ContDF.columns = ContDF.columns.droplevel(0)
ContDF

def answer_eleven():
    return ContDF
    raise NotImplementedError()


# In[29]:


assert type(answer_eleven()) == pd.DataFrame, "Q11: You should return a DataFrame!"

assert answer_eleven().shape[0] == 5, "Q11: Wrong row numbers!"

assert answer_eleven().shape[1] == 4, "Q11: Wrong column numbers!"


# ### Question 12
# Cut % Renewable into 5 bins. Group Top15 by the Continent, as well as these new % Renewable bins. How many countries are in each of these groups?
# 
# *This function should return a Series with a MultiIndex of `Continent`, then the bins for `% Renewable`. Do not include groups with no countries.*
RenDF = tempdf
RenDF['Bin'] = pd.cut(tempdf['% Renewable'],5)
RenDF = RenDF.rename(columns = {'% Renewable': 'Count', 'Bin': '% Renewable'})
binDF = RenDF.pivot_table(values='Count', index='Continent', columns='% Renewable', aggfunc=[np.size])
binDF = binDF.stack()
series12 = binDF.squeeze()
series12

# In[30]:


RenDF = tempdf
RenDF['Bin'] = pd.cut(tempdf['% Renewable'],5)
RenDF = RenDF.rename(columns = {'% Renewable': 'Count', 'Bin': '% Renewable'})
binDF = RenDF.pivot_table(values='Count', index='Continent', columns='% Renewable', aggfunc=[np.size])
binDF = binDF.stack()
series12 = binDF.squeeze()

def answer_twelve():
    return series12
    raise NotImplementedError()


# In[31]:


assert type(answer_twelve()) == pd.Series, "Q12: You should return a Series!"

assert len(answer_twelve()) == 9, "Q12: Wrong result numbers!"


# ### Question 13
# Convert the Population Estimate series to a string with thousands separator (using commas). Use all significant digits (do not round the results).
# 
# e.g. 12345678.90 -> 12,345,678.90
# 
# *This function should return a series `PopEst` whose index is the country name and whose values are the population estimate string*

# In[32]:


def format_nums(x):
    number = "{:,}".format(x)
    return number
DF_13 = new_df.reset_index()
DF_13.sort_values('Rank', inplace=True)
DF_13 = DF_13.set_index('Country')
DF_13['PopEst'] = DF_13['PopEst'].apply(lambda x: format_nums(x))

#s = format_nums(12343.94)
#print(s)
series13 = DF_13['PopEst']
series13


# In[33]:


def answer_thirteen():
    return series13
    raise NotImplementedError()


# In[34]:


assert type(answer_thirteen()) == pd.Series, "Q13: You should return a Series!"

assert len(answer_thirteen()) == 15, "Q13: Wrong result numbers!"


# ### Optional
# 
# Use the built in function `plot_optional()` to see an example visualization.

# In[35]:


def plot_optional():
    import matplotlib as plt
    get_ipython().run_line_magic('matplotlib', 'inline')
    Top15 = answer_one()
    ax = Top15.plot(x='Rank', y='% Renewable', kind='scatter', 
                    c=['#e41a1c','#377eb8','#e41a1c','#4daf4a','#4daf4a','#377eb8','#4daf4a','#e41a1c',
                       '#4daf4a','#e41a1c','#4daf4a','#4daf4a','#e41a1c','#dede00','#ff7f00'], 
                    xticks=range(1,16), s=6*Top15['2014']/10**10, alpha=.75, figsize=[16,6]);

    for i, txt in enumerate(Top15.index):
        ax.annotate(txt, [Top15['Rank'][i], Top15['% Renewable'][i]], ha='center')

    print("This is an example of a visualization that can be created to help understand the data. This is a bubble chart showing % Renewable vs. Rank. The size of the bubble corresponds to the countries' 2014 GDP, and the color corresponds to the continent.")


# In[ ]:




