#!/usr/bin/env python
# coding: utf-8

# # Assignment 4
# ## Description
# In this assignment you must read in a file of metropolitan regions and associated sports teams from [assets/wikipedia_data.html](assets/wikipedia_data.html) and answer some questions about each metropolitan region. Each of these regions may have one or more teams from the "Big 4": NFL (football, in [assets/nfl.csv](assets/nfl.csv)), MLB (baseball, in [assets/mlb.csv](assets/mlb.csv)), NBA (basketball, in [assets/nba.csv](assets/nba.csv) or NHL (hockey, in [assets/nhl.csv](assets/nhl.csv)). Please keep in mind that all questions are from the perspective of the metropolitan region, and that this file is the "source of authority" for the location of a given sports team. Thus teams which are commonly known by a different area (e.g. "Oakland Raiders") need to be mapped into the metropolitan region given (e.g. San Francisco Bay Area). This will require some human data understanding outside of the data you've been given (e.g. you will have to hand-code some names, and might need to google to find out where teams are)!
# 
# For each sport I would like you to answer the question: **what is the win/loss ratio's correlation with the population of the city it is in?** Win/Loss ratio refers to the number of wins over the number of wins plus the number of losses. Remember that to calculate the correlation with [`pearsonr`](https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.pearsonr.html), so you are going to send in two ordered lists of values, the populations from the wikipedia_data.html file and the win/loss ratio for a given sport in the same order. Average the win/loss ratios for those cities which have multiple teams of a single sport. Each sport is worth an equal amount in this assignment (20%\*4=80%) of the grade for this assignment. You should only use data **from year 2018** for your analysis -- this is important!
# 
# ## Notes
# 
# 1. Do not include data about the MLS or CFL in any of the work you are doing, we're only interested in the Big 4 in this assignment.
# 2. I highly suggest that you first tackle the four correlation questions in order, as they are all similar and worth the majority of grades for this assignment. This is by design!
# 3. It's fair game to talk with peers about high level strategy as well as the relationship between metropolitan areas and sports teams. However, do not post code solving aspects of the assignment (including such as dictionaries mapping areas to teams, or regexes which will clean up names).
# 4. There may be more teams than the assert statements test, remember to collapse multiple teams in one city into a single value!

# In[1]:


from IPython.display import display, HTML
display(HTML("<style>.container { width:100% !important; }</style>"))
display(HTML("<style>.container { border-left-width: 0px !important; }</style>"))


# ## Question 1
# For this question, calculate the win/loss ratio's correlation with the population of the city it is in for the **NHL** using **2018** data.

# In[22]:


import pandas as pd
import numpy as np
import scipy.stats as stats
import re

nhl_df=pd.read_csv("assets/nhl.csv")
cities=pd.read_html("assets/wikipedia_data.html")[1]
cities=cities.iloc[:-1,[0,3,5,6,7,8]]
nhl_df = nhl_df[nhl_df['year'] == 2018]
nhl_df = nhl_df[nhl_df['GP'] == '82']
nhl_df['W'] = nhl_df['W'].astype(int) 
nhl_df['L'] = nhl_df['L'].astype(int)
nhl_df['OL'] = nhl_df['OL'].astype(int)
nhl_df['Ratio'] = nhl_df['W']/(nhl_df['W']+nhl_df['L'])
nhl_df['City'] = ['Tampa Bay Area', 'Boston', 'Toronto', 'Miami–Fort Lauderdale', 'Detroit',
                  'Montreal', 'Ottawa', 'Buffalo','Washington, D.C.', 'Pittsburgh',
                  'Philadelphia', 'Columbus', 'New York City', 'Raleigh', 'New York City',
                  'New York City', 'Nashville', 'Winnipeg', 'Minneapolis–Saint Paul', 'Denver',
                  'St. Louis', 'Dallas–Fort Worth', 'Chicago', 'Las Vegas', 'Los Angeles', 
                  'San Francisco Bay Area', 'Los Angeles', 'Calgary', 'Edmonton', 'Vancouver',
                  'Phoenix']
nhl_df
nhl_ratio = nhl_df[['City', 'Ratio']]
nhl_ratio = nhl_ratio.groupby('City', as_index=False, sort=False)['Ratio'].mean()
nhl_ratio


# In[1]:


cities = cities.rename(columns = {'Metropolitan area': 'City',
                                  'Population (2016 est.)[8]': 'Pop.'})
Pop_df = cities[['City', 'Pop.']]
Pop_df['Pop.'] = Pop_df['Pop.'].astype(int)
nhl_corr = pd.merge(nhl_ratio, Pop_df, how='left', on='City')
#Pop_df = Pop_df.set_index('City')

Pop_df


# In[ ]:





# In[4]:


nhl_corr


# In[12]:


nhl_df=pd.read_csv("assets/nhl.csv")
cities=pd.read_html("assets/wikipedia_data.html")[1]
cities=cities.iloc[:-1,[0,3,5,6,7,8]]
nhl_df = nhl_df[nhl_df['year'] == 2018]
nhl_df = nhl_df[nhl_df['GP'] == '82']
nhl_df['W'] = nhl_df['W'].astype(int) 
nhl_df['L'] = nhl_df['L'].astype(int)
nhl_df['OL'] = nhl_df['OL'].astype(int)
nhl_df['Ratio'] = nhl_df['W']/(nhl_df['W']+nhl_df['L'])
nhl_df['City'] = ['Tampa Bay Area', 'Boston', 'Toronto', 'Miami–Fort Lauderdale', 'Detroit',
                  'Montreal', 'Ottawa', 'Buffalo','Washington, D.C.', 'Pittsburgh',
                  'Philadelphia', 'Columbus', 'New York City', 'Raleigh', 'New York City',
                  'New York City', 'Nashville', 'Winnipeg', 'Minneapolis–Saint Paul', 'Denver',
                  'St. Louis', 'Dallas–Fort Worth', 'Chicago', 'Las Vegas', 'Los Angeles', 
                  'San Francisco Bay Area', 'Los Angeles', 'Calgary', 'Edmonton', 'Vancouver',
                  'Phoenix']
nhl_ratio = nhl_df[['City', 'Ratio']]
nhl_ratio = nhl_ratio.groupby('City', as_index=False, sort=False)['Ratio'].mean()

cities = cities.rename(columns = {'Metropolitan area': 'City',
                              'Population (2016 est.)[8]': 'Pop.'})
#creating Population dataframe based on wiki
Pop_df = cities[['City', 'Pop.']]
Pop_df['Pop.'] = Pop_df['Pop.'].astype(int)
nhl_corr = pd.merge(nhl_ratio, Pop_df, how='left', on='City')

def nhl_correlation(): 
    # YOUR CODE HERE
    #raise NotImplementedError()
    import pandas as pd
    import numpy as np
    import scipy.stats as stats
    import re

   

    population_by_region = nhl_corr['Pop.'] # pass in metropolitan area population from cities
    win_loss_by_region = nhl_corr['Ratio'] # pass in win/loss ratio from nhl_df in the same order as cities["Metropolitan area"]

    assert len(population_by_region) == len(win_loss_by_region), "Q1: Your lists must be the same length"
    assert len(population_by_region) == 28, "Q1: There should be 28 teams being analysed for NHL"
    
    return stats.pearsonr(population_by_region, win_loss_by_region)[0]


# In[13]:


nhl_correlation()


# In[ ]:





# ## Question 2
# For this question, calculate the win/loss ratio's correlation with the population of the city it is in for the **NBA** using **2018** data.

# In[ ]:


nba_df=pd.read_csv("assets/nba.csv")
nba_df = nba_df[nba_df['year'] == 2018]
nba_df = nba_df.rename(columns = {'W/L%': 'Ratio'})
nba_df['City'] = ['Toronto', 'Boston', 'Philadelphia', 'Cleveland', 'Indianapolis',
                  'Miami–Fort Lauderdale', 'Milwaukee', 'Washington, D.C.', 'Detroit',
                  'Charlotte', 'New York City', 'New York City', 'Chicago', 'Orlando',
                  'Atlanta', 'Houston', 'San Francisco Bay Area', 'Portland', 'Oklahoma City',
                  'Salt Lake City', 'New Orleans', 'San Antonio', 'Minneapolis–Saint Paul',
                  'Denver', 'Los Angeles', 'Los Angeles', 'Sacramento', 'Dallas–Fort Worth',
                  'Memphis', 'Phoenix']
nba_ratio = nba_df[['City', 'Ratio']]
nba_ratio['Ratio'] = nba_ratio['Ratio'].astype(float)
nba_ratio = nba_ratio.groupby('City', as_index=False, sort=False)['Ratio'].mean()
nba_ratio


# In[ ]:


nba_corr = pd.merge(nba_ratio, Pop_df, how='left', on='City')
Pop_df
nba_corr


# In[14]:


import pandas as pd
import numpy as np
import scipy.stats as stats
import re

nba_df=pd.read_csv("assets/nba.csv")
nba_df = nba_df[nba_df['year'] == 2018]
nba_df = nba_df.rename(columns = {'W/L%': 'Ratio'})
nba_df['City'] = ['Toronto', 'Boston', 'Philadelphia', 'Cleveland', 'Indianapolis',
                  'Miami–Fort Lauderdale', 'Milwaukee', 'Washington, D.C.', 'Detroit',
                  'Charlotte', 'New York City', 'New York City', 'Chicago', 'Orlando',
                  'Atlanta', 'Houston', 'San Francisco Bay Area', 'Portland', 'Oklahoma City',
                  'Salt Lake City', 'New Orleans', 'San Antonio', 'Minneapolis–Saint Paul',
                  'Denver', 'Los Angeles', 'Los Angeles', 'Sacramento', 'Dallas–Fort Worth',
                  'Memphis', 'Phoenix']
nba_ratio = nba_df[['City', 'Ratio']]
nba_ratio['Ratio'] = nba_ratio['Ratio'].astype(float)
nba_ratio = nba_ratio.groupby('City', as_index=False, sort=False)['Ratio'].mean()

nba_corr = pd.merge(nba_ratio, Pop_df, how='left', on='City')

def nba_correlation():
    # YOUR CODE HERE
    #raise NotImplementedError()
    
    population_by_region = nba_corr['Pop.'] # pass in metropolitan area population from cities
    win_loss_by_region = nba_corr['Ratio'] # pass in win/loss ratio from nba_df in the same order as cities["Metropolitan area"]

    assert len(population_by_region) == len(win_loss_by_region), "Q2: Your lists must be the same length"
    assert len(population_by_region) == 28, "Q2: There should be 28 teams being analysed for NBA"

    return stats.pearsonr(population_by_region, win_loss_by_region)[0]


# In[15]:


nba_correlation()


# In[ ]:





# ## Question 3
# For this question, calculate the win/loss ratio's correlation with the population of the city it is in for the **MLB** using **2018** data.

# In[ ]:


mlb_df=pd.read_csv("assets/mlb.csv")
cities=pd.read_html("assets/wikipedia_data.html")[1]
cities=cities.iloc[:-1,[0,3,5,6,7,8]]
mlb_df = mlb_df.rename(columns = {'W-L%': 'Ratio'})
mlb_df = mlb_df[mlb_df['year']==2018]
mlb_df['City'] = ['Boston', 'New York City', 'Tampa Bay Area', 'Toronto', 'Baltimore', 
                  'Cleveland', 'Minneapolis–Saint Paul', 'Detroit', 'Chicago', 'Kansas City',
                  'Houston', 'San Francisco Bay Area', 'Seattle', 'Los Angeles',
                  'Dallas–Fort Worth', 'Atlanta', 'Washington, D.C.', 'Philadelphia',
                  'New York City', 'Miami–Fort Lauderdale', 'Milwaukee', 'Chicago', 'St. Louis',
                  'Pittsburgh', 'Cincinnati', 'Los Angeles', 'Denver', 'Phoenix',
                  'San Francisco Bay Area', 'San Diego']
mlb_ratio = mlb_df[['City', 'Ratio']]
mlb_ratio = mlb_ratio.groupby('City', as_index=False, sort=False)['Ratio'].mean()
mlb_ratio


# In[ ]:


mlb_corr = pd.merge(mlb_ratio, Pop_df, how='left', on='City')
Pop_df
mlb_corr


# In[16]:


import pandas as pd
import numpy as np
import scipy.stats as stats
import re

mlb_df=pd.read_csv("assets/mlb.csv")
cities=pd.read_html("assets/wikipedia_data.html")[1]
cities=cities.iloc[:-1,[0,3,5,6,7,8]]
mlb_df = mlb_df.rename(columns = {'W-L%': 'Ratio'})
mlb_df = mlb_df[mlb_df['year']==2018]
mlb_df['City'] = ['Boston', 'New York City', 'Tampa Bay Area', 'Toronto', 'Baltimore', 
                  'Cleveland', 'Minneapolis–Saint Paul', 'Detroit', 'Chicago', 'Kansas City',
                  'Houston', 'San Francisco Bay Area', 'Seattle', 'Los Angeles',
                  'Dallas–Fort Worth', 'Atlanta', 'Washington, D.C.', 'Philadelphia',
                  'New York City', 'Miami–Fort Lauderdale', 'Milwaukee', 'Chicago', 'St. Louis',
                  'Pittsburgh', 'Cincinnati', 'Los Angeles', 'Denver', 'Phoenix',
                  'San Francisco Bay Area', 'San Diego']
mlb_ratio = mlb_df[['City', 'Ratio']]
mlb_ratio = mlb_ratio.groupby('City', as_index=False, sort=False)['Ratio'].mean()

mlb_corr = pd.merge(mlb_ratio, Pop_df, how='left', on='City')

def mlb_correlation(): 
    # YOUR CODE HERE
    #raise NotImplementedError()
    
    population_by_region = mlb_corr['Pop.'] # pass in metropolitan area population from cities
    win_loss_by_region = mlb_corr['Ratio'] # pass in win/loss ratio from mlb_df in the same order as cities["Metropolitan area"]

    assert len(population_by_region) == len(win_loss_by_region), "Q3: Your lists must be the same length"
    assert len(population_by_region) == 26, "Q3: There should be 26 teams being analysed for MLB"

    return stats.pearsonr(population_by_region, win_loss_by_region)[0]


# In[17]:


mlb_correlation()


# In[ ]:





# ## Question 4
# For this question, calculate the win/loss ratio's correlation with the population of the city it is in for the **NFL** using **2018** data.

# In[ ]:


nfl_df=pd.read_csv("assets/nfl.csv")
nfl_df = nfl_df.rename(columns = {'W-L%': 'Ratio'})
nfl_df = nfl_df[nfl_df['year']==2018]
nfl_df = nfl_df.drop(labels=[0,5,10, 15, 20, 25, 30, 35], axis=0)
nfl_df['Ratio'] = nfl_df['Ratio'].astype(float)
nfl_df
nfl_df['City'] = ['Boston', 'Miami–Fort Lauderdale', 'Buffalo', 'New York City',
                 'Baltimore', 'Pittsburgh', 'Cleveland', 'Cincinnati', 'Houston', 'Indianapolis',
                 'Nashville', 'Jacksonville', 'Kansas City', 'Los Angeles', 'Denver',
                 'San Francisco Bay Area', 'Dallas–Fort Worth', 'Philadelphia',
                 'Washington, D.C.', 'New York City', 'Chicago', 'Minneapolis–Saint Paul',
                 'Green Bay', 'Detroit', 'New Orleans', 'Charlotte', 'Atlanta',
                 'Tampa Bay Area', 'Los Angeles', 'Seattle', 'San Francisco Bay Area', 'Phoenix']
nfl_ratio = nfl_df[['City', 'Ratio']]
nfl_ratio = nfl_ratio.groupby('City', as_index=False, sort=False)['Ratio'].mean()
nfl_ratio


# In[ ]:


nfl_corr = pd.merge(nfl_ratio, Pop_df, how='left', on='City')
Pop_df
nfl_corr


# In[18]:


import pandas as pd
import numpy as np
import scipy.stats as stats
import re

nfl_df=pd.read_csv("assets/nfl.csv")
nfl_df = nfl_df.rename(columns = {'W-L%': 'Ratio'})
nfl_df = nfl_df[nfl_df['year']==2018]
nfl_df = nfl_df.drop(labels=[0,5,10, 15, 20, 25, 30, 35], axis=0)
nfl_df['Ratio'] = nfl_df['Ratio'].astype(float)
nfl_df
nfl_df['City'] = ['Boston', 'Miami–Fort Lauderdale', 'Buffalo', 'New York City',
                 'Baltimore', 'Pittsburgh', 'Cleveland', 'Cincinnati', 'Houston', 'Indianapolis',
                 'Nashville', 'Jacksonville', 'Kansas City', 'Los Angeles', 'Denver',
                 'San Francisco Bay Area', 'Dallas–Fort Worth', 'Philadelphia',
                 'Washington, D.C.', 'New York City', 'Chicago', 'Minneapolis–Saint Paul',
                 'Green Bay', 'Detroit', 'New Orleans', 'Charlotte', 'Atlanta',
                 'Tampa Bay Area', 'Los Angeles', 'Seattle', 'San Francisco Bay Area', 'Phoenix']
nfl_ratio = nfl_df[['City', 'Ratio']]
nfl_ratio = nfl_ratio.groupby('City', as_index=False, sort=False)['Ratio'].mean()

nfl_corr = pd.merge(nfl_ratio, Pop_df, how='left', on='City')

def nfl_correlation(): 
    # YOUR CODE HERE
    #raise NotImplementedError()
    
    population_by_region = nfl_corr['Pop.'] # pass in metropolitan area population from cities
    win_loss_by_region = nfl_corr['Ratio'] # pass in win/loss ratio from nfl_df in the same order as cities["Metropolitan area"]

    assert len(population_by_region) == len(win_loss_by_region), "Q4: Your lists must be the same length"
    assert len(population_by_region) == 29, "Q4: There should be 29 teams being analysed for NFL"

    return stats.pearsonr(population_by_region, win_loss_by_region)[0]


# In[19]:


nfl_correlation()


# In[ ]:





# ## Question 5
# In this question I would like you to explore the hypothesis that **given that an area has two sports teams in different sports, those teams will perform the same within their respective sports**. How I would like to see this explored is with a series of paired t-tests (so use [`ttest_rel`](https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.ttest_rel.html)) between all pairs of sports. Are there any sports where we can reject the null hypothesis? Again, average values where a sport has multiple teams in one region. Remember, you will only be including, for each sport, cities which have teams engaged in that sport, drop others as appropriate. This question is worth 20% of the grade for this assignment.
import numpy as np
import scipy.stats as stats
import re
i = 4
j = 4
l_df = []
lengths = []

while i > 0:
    if i == 4:
        a = nfl_ratio
    elif i == 3:
        a = nhl_ratio
    elif i == 2:
        a = mlb_ratio
    elif i ==1:
        a = nba_ratio
    i -= 1
    j = 4
    while j > 0:
        if j == 4:
            b = nfl_ratio
        elif j == 3:
            b = nhl_ratio
        elif j == 2:
            b = mlb_ratio
        elif j == 1:
            b = nba_ratio
        j -= 1
        df = pd.merge(a, b, how='inner', on='City')
        length = len(df)
        l_df.append(df)
        lengths.append(length)
lengths
# In[20]:


from scipy.stats import ttest_rel
a =[]
for x in [nfl_ratio, nba_ratio, nhl_ratio, mlb_ratio]:
    b= []    
    for y in [nfl_ratio, nba_ratio, nhl_ratio, mlb_ratio]:
        df = pd.merge(x , y, how = 'inner', on = 'City')
        b.append(ttest_rel(df['Ratio_x'], df['Ratio_y']).pvalue)
        #combs.append(len(df))
    a.append(b)
a


# In[21]:


sports = ['NFL', 'NBA', 'NHL', 'MLB']
p_values = pd.DataFrame(a, columns=sports, index=sports)
p_values


# In[22]:


import pandas as pd
import numpy as np
import scipy.stats as stats
import re

def sports_team_performance():
    # YOUR CODE HERE
    #raise NotImplementedError()
    
    a =[]
    for x in [nfl_ratio, nba_ratio, nhl_ratio, mlb_ratio]:
        b= []    
        for y in [nfl_ratio, nba_ratio, nhl_ratio, mlb_ratio]:
            df = pd.merge(x , y, how = 'inner', on = 'City')
            b.append(ttest_rel(df['Ratio_x'], df['Ratio_y']).pvalue)
            #combs.append(len(df))
        a.append(b)
    a
    
    # Note: p_values is a full dataframe, so df.loc["NFL","NBA"] should be the same as df.loc["NBA","NFL"] and
    # df.loc["NFL","NFL"] should return np.nan
    sports = ['NFL', 'NBA', 'NHL', 'MLB']
    p_values = pd.DataFrame(a, columns=sports, index=sports)
    p_values
    
    assert abs(p_values.loc["NBA", "NHL"] - 0.02) <= 1e-2, "The NBA-NHL p-value should be around 0.02"
    assert abs(p_values.loc["MLB", "NFL"] - 0.80) <= 1e-2, "The MLB-NFL p-value should be around 0.80"
    return p_values


# In[23]:


sports_team_performance()


# In[ ]:




