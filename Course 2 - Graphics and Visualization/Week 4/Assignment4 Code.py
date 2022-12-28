
# coding: utf-8

# # Assignment 4
# 
# Before working on this assignment please read these instructions fully. In the submission area, you will notice that you can click the link to **Preview the Grading** for each step of the assignment. This is the criteria that will be used for peer grading. Please familiarize yourself with the criteria before beginning the assignment.
# 
# This assignment requires that you to find **at least** two datasets on the web which are related, and that you visualize these datasets to answer a question with the broad topic of **sports or athletics** (see below) for the region of **Ann Arbor, Michigan, United States**, or **United States** more broadly.
# 
# You can merge these datasets with data from different regions if you like! For instance, you might want to compare **Ann Arbor, Michigan, United States** to Ann Arbor, USA. In that case at least one source file must be about **Ann Arbor, Michigan, United States**.
# 
# You are welcome to choose datasets at your discretion, but keep in mind **they will be shared with your peers**, so choose appropriate datasets. Sensitive, confidential, illicit, and proprietary materials are not good choices for datasets for this assignment. You are welcome to upload datasets of your own as well, and link to them using a third party repository such as github, bitbucket, pastebin, etc. Please be aware of the Coursera terms of service with respect to intellectual property.
# 
# Also, you are welcome to preserve data in its original language, but for the purposes of grading you should provide english translations. You are welcome to provide multiple visuals in different languages if you would like!
# 
# As this assignment is for the whole course, you must incorporate principles discussed in the first week, such as having as high data-ink ratio (Tufte) and aligning with Cairo’s principles of truth, beauty, function, and insight.
# 
# Here are the assignment instructions:
# 
#  * State the region and the domain category that your data sets are about (e.g., **Ann Arbor, Michigan, United States** and **sports or athletics**).
#  * You must state a question about the domain category and region that you identified as being interesting.
#  * You must provide at least two links to available datasets. These could be links to files such as CSV or Excel files, or links to websites which might have data in tabular form, such as Wikipedia pages.
#  * You must upload an image which addresses the research question you stated. In addition to addressing the question, this visual should follow Cairo's principles of truthfulness, functionality, beauty, and insightfulness.
#  * You must contribute a short (1-2 paragraph) written justification of how your visualization addresses your stated research question.
# 
# What do we mean by **sports or athletics**?  For this category we are interested in sporting events or athletics broadly, please feel free to creatively interpret the category when building your research question!
# 
# ## Tips
# * Wikipedia is an excellent source of data, and I strongly encourage you to explore it for new data sources.
# * Many governments run open data initiatives at the city, region, and country levels, and these are wonderful resources for localized data sources.
# * Several international agencies, such as the [United Nations](http://data.un.org/), the [World Bank](http://data.worldbank.org/), the [Global Open Data Index](http://index.okfn.org/place/) are other great places to look for data.
# * This assignment requires you to convert and clean datafiles. Check out the discussion forums for tips on how to do this from various sources, and share your successes with your fellow students!
# 
# ## Example
# Looking for an example? Here's what our course assistant put together for the **Ann Arbor, MI, USA** area using **sports and athletics** as the topic. [Example Solution File](./readonly/Assignment4_example.pdf)

# In[1]:

get_ipython().magic('matplotlib notebook')
from IPython.display import display, HTML
display(HTML("<style>.container { width:100% !important; }</style>"))
display(HTML("<style>.container { border-left-width: 0px !important; }</style>"))


# In[15]:


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec

df = pd.read_csv('MichiganFootballRecords.csv')
df
df.drop(df.columns[0], axis=1, inplace=True)
record_df = df[['Year', 'Pct', 'Coach(es)']]
record_df = record_df.drop([2])
record_df= record_df[record_df['Year'] > 1994]
record_df= record_df[record_df['Year'] < 2022]
record_df
#record_df.set_index('Year', inplace =True)
#record_df.drop([2])
hist_df = record_df[['Year', 'Coach(es)']]
hist_df['Coach(es)'] = hist_df['Coach(es)'].str.extract('([\w+ \w+]+)')
hist_df


# In[42]:

ndf = pd.read_csv('Michigan_Football_Drafts.csv')
ndf


# In[108]:

drafts = {}
counts = {}
zipped = list(zip(ndf['Year'], ndf['Draft Position']))
medians = []
place =[]
#Loop through Draft position doc to create dictionary of year/draft pos,
#list of medians, and a dictionary of counts / year 
for year, pos in zipped:
    if year not in drafts.keys():
        try:
            mid = len(place)//2
            res = (place[mid] + place[~mid])/2
            medians.append(res)
        except: pass
        place =[]
        z = 1
        place.append(pos)
        drafts[year] = place
        counts[year] = z
    elif year in drafts.keys():
        z += 1
        place.append(pos)
        drafts[year] = place
        counts[year] = z
mid = len(place)//2
res = (place[mid] + place[~mid])/2
medians.append(res)        
#print(drafts)

#Creates DF for each coach with count of draft picks per year
count_df = pd.DataFrame(list(counts.items()), columns =['Year', 'Count'])
coach_df = pd.merge(hist_df, count_df, on='Year')
Jim_DF = coach_df[coach_df['Coach(es)'] == 'Jim Harbaugh ']
Brady_DF = coach_df[coach_df['Coach(es)'] == 'Brady Hoke ']
Rich_DF = coach_df[coach_df['Coach(es)'] == 'Rich Rodriguez ']
Lloyd_DF = coach_df[coach_df['Coach(es)'] == 'Lloyd Carr ']
J = len(Jim_DF['Year'])
B = len(Brady_DF['Year'])
R = len(Rich_DF['Year'])
L = len(Lloyd_DF['Year'])

Jim = range(1, J+1)
Brady = range(J+1, J+B+1)
Rich = range(J+B+1, J+B+R+1)
Lloyd = range(J+B+R+1, J+B+R+L+1)
#Creates boxplot as a subplot ax
#fig, ax =plt.subplots()
fig = plt.figure()
gspec = gridspec.GridSpec(3, 3)

#fig = plt.subplots()
ax = plt.subplot(gspec[1:, 0:])
ax2 = plt.subplot(gspec[1:, 0:])
ax3 = plt.subplot(gspec[0, 0:], sharex=ax)


labels, data = [*zip(*drafts.items())]
ax.boxplot(data, whis = .75)
ax.set_xticklabels(labels, rotation = 45)
ax.set_ylabel('Draft Position') 
ax.invert_yaxis()   
#makes ax2 share an x axis with ax
ax2 =ax.twinx()
bJ =ax3.bar(Jim, Jim_DF['Count'], color='Blue')
bB= ax3.bar(Brady, Brady_DF['Count'], color='Green')
bR= ax3.bar(Rich, Rich_DF['Count'], color='Yellow')
bL = ax3.bar(Lloyd, Lloyd_DF['Count'], color='orange')

#plot a line plot of win pct
ax2.plot(np.arange(len(record_df.Pct))+1, record_df.Pct)
#ax2.plot(record_df.Year, record_df.Pct)
ax2.set_xlabel('Year')
ax2.set_ylabel('Win Percentage')
ax3.set_ylabel('# Players Drafted')
ax3.tick_params(axis = 'x', which='both', labelbottom='off')
#create text for medians of box plots
spot = range(len(medians))
for xtick in (ax.get_xticks()):
    ax.text(xtick, medians[xtick-1]-2, medians[xtick-1], horizontalalignment ='center', 
            size ='x-small', color='b', weight='semibold')
    print(xtick)
lgd = ax3.legend((bJ, bB, bR, bL),
                 ('Jim Harbaugh Era','Brady Hoke Era','Rich Rodriguez Era',
                  'Lloyd Carr Era'), bbox_to_anchor=(1.07, 0.5), loc='center',
                 frameon= False, prop={'size':10})
ax3.set_title('Average NFL Draft Placement for Michigan Football against Win Percentage')
fig.set_figwidth(20)
fig.savefig('Draft Position vs Win Pct')


# In[5]:

#things to add, need to add a subplot above this with histogram of 
#count of draft players, colored by era of coach.
#Add title, and average placement


# In[6]:



