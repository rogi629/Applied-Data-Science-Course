
# coding: utf-8

# # Assignment 2
# 
# Before working on this assignment please read these instructions fully. In the submission area, you will notice that you can click the link to **Preview the Grading** for each step of the assignment. This is the criteria that will be used for peer grading. Please familiarize yourself with the criteria before beginning the assignment.
# 
# An NOAA dataset has been stored in the file `data/C2A2_data/BinnedCsvs_d400/fb441e62df2d58994928907a91895ec62c2c42e6cd075c2700843b89.csv`. This is the dataset to use for this assignment. Note: The data for this assignment comes from a subset of The National Centers for Environmental Information (NCEI) [Daily Global Historical Climatology Network](https://www1.ncdc.noaa.gov/pub/data/ghcn/daily/readme.txt) (GHCN-Daily). The GHCN-Daily is comprised of daily climate records from thousands of land surface stations across the globe.
# 
# Each row in the assignment datafile corresponds to a single observation.
# 
# The following variables are provided to you:
# 
# * **id** : station identification code
# * **date** : date in YYYY-MM-DD format (e.g. 2012-01-24 = January 24, 2012)
# * **element** : indicator of element type
#     * TMAX : Maximum temperature (tenths of degrees C)
#     * TMIN : Minimum temperature (tenths of degrees C)
# * **value** : data value for element (tenths of degrees C)
# 
# For this assignment, you must:
# 
# 1. Read the documentation and familiarize yourself with the dataset, then write some python code which returns a line graph of the record high and record low temperatures by day of the year over the period 2005-2014. The area between the record high and record low temperatures for each day should be shaded.
# 2. Overlay a scatter of the 2015 data for any points (highs and lows) for which the ten year record (2005-2014) record high or record low was broken in 2015.
# 3. Watch out for leap days (i.e. February 29th), it is reasonable to remove these points from the dataset for the purpose of this visualization.
# 4. Make the visual nice! Leverage principles from the first module in this course when developing your solution. Consider issues such as legends, labels, and chart junk.
# 
# The data you have been given is near **Ann Arbor, Michigan, United States**, and the stations the data comes from are shown on the map below.

# In[39]:

import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import mplleaflet
import pandas as pd
from datetime import datetime

df = pd.read_csv('data/C2A2_data/BinnedCsvs_d400/fb441e62df2d58994928907a91895ec62c2c42e6cd075c2700843b89.csv')

tenyrdf = df[df['Date'] < '2015-01-01']
minmaxdf = tenyrdf
minmaxdf['Date'] = tenyrdf['Date'].str[5:]
minmaxdf = minmaxdf.sort_values(by = ['Date', 'ID', 'Element'])
minmaxdf = minmaxdf[minmaxdf['Date'] != '02-29']
minmaxdf['Date'] = pd.to_datetime('2015-' + minmaxdf['Date'])

df_2015 = df[df['Date'] >= '2015-01-01']
df_2015 = df_2015.sort_values(by = ['Date', 'ID', 'Element'])
df_2015['Date'] = pd.to_datetime(df_2015['Date'])

zipped = list(zip(minmaxdf['Date'], minmaxdf['Data_Value']))
#print(zipped)

date= []
max_temp = []
min_temp = []
temps = []
for x, y in zipped:
    #print(x,y)
    if x not in date:
        try:
            max_temp.append(max(temps))
            min_temp.append(min(temps))
        except: pass
        date.append(x)
        temps =[(y/10)]
    else:
        temps.append(y/10)
max_temp.append(max(temps))
min_temp.append(min(temps))
print(len(date))
print(len(max_temp))
print(len(min_temp))

zipped2 = list(zip((df_2015['Date']), df_2015['Data_Value']))
date2= []
dateover = []
dateunder = []
overtemp = []
undertemp = []
        
z = 0
for a, b in zipped2:
    t = b/10
    if a not in date2:
        date2.append(a)
        c = max_temp[z]
        d = min_temp[z]
        z += 1
        if t > c:
            dateover.append(a)
            overtemp.append(t)
        elif t < d:
            dateunder.append(a)
            undertemp.append(t)
    else:
        c = max_temp[z-1]
        d = min_temp[z-1]
        if t > c:
            dateover.append(a)
            overtemp.append(t)
        elif t < d:
            dateunder.append(a)
            undertemp.append(t)

print(dateover, dateunder)
fig, ax = plt.subplots()
ax.set_ylabel("Degrees C")
ax.set_xlabel("Month")
ax.set_title('Record Temps from 2005-2014 compared to Temps in 2015')


xfmt = mdates.DateFormatter('%b')
months = mdates.MonthLocator()
ax.xaxis.set_major_locator(months)
ax.xaxis.set_major_formatter(xfmt)

l1, l2 =ax.plot(date, max_temp, '--o', date, min_temp, '--o')
ax.fill_between(date, max_temp, min_temp, alpha=.25)
l3 =ax.scatter(dateover, overtemp, c = 'red')
l4 =ax.scatter(dateunder, undertemp, c='blue')

#ax.legend((l1, l2, l3, l4), ('Max', 'Min', 'High', 'Low'), loc='upper right', frameon= False, title = 'Legend')
ax.legend((l1, l2, l3, l4), ('Max Temp 2005-2014', 'Min Temp 2005-2014', '2015 Temps Higher than 10 year record', '2015 Temps Lower than 10 Year Record'), bbox_to_anchor=(1.75, .5), loc='right', frameon= False)
#plt.plot(date, min_temp, '--o')

plt.show()


# In[ ]:

import matplotlib.pyplot as plt
import mplleaflet
import pandas as pd

def leaflet_plot_stations(binsize, hashid):

    df = pd.read_csv('data/C2A2_data/BinSize_d{}.csv'.format(binsize))

    station_locations_by_hash = df[df['hash'] == hashid]

    lons = station_locations_by_hash['LONGITUDE'].tolist()
    lats = station_locations_by_hash['LATITUDE'].tolist()

    plt.figure(figsize=(8,8))

    plt.scatter(lons, lats, c='r', alpha=0.7, s=200)

    return mplleaflet.display()

leaflet_plot_stations(400,'fb441e62df2d58994928907a91895ec62c2c42e6cd075c2700843b89')


# In[ ]:



