
# coding: utf-8

# # Assignment 3 - Building a Custom Visualization
# 
# ---
# 
# In this assignment you must choose one of the options presented below and submit a visual as well as your source code for peer grading. The details of how you solve the assignment are up to you, although your assignment must use matplotlib so that your peers can evaluate your work. The options differ in challenge level, but there are no grades associated with the challenge level you chose. However, your peers will be asked to ensure you at least met a minimum quality for a given technique in order to pass. Implement the technique fully (or exceed it!) and you should be able to earn full grades for the assignment.
# 
# 
# &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Ferreira, N., Fisher, D., & Konig, A. C. (2014, April). [Sample-oriented task-driven visualizations: allowing users to make better, more confident decisions.](https://www.microsoft.com/en-us/research/wp-content/uploads/2016/02/Ferreira_Fisher_Sample_Oriented_Tasks.pdf) 
# &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;In Proceedings of the SIGCHI Conference on Human Factors in Computing Systems (pp. 571-580). ACM. ([video](https://www.youtube.com/watch?v=BI7GAs-va-Q))
# 
# 
# In this [paper](https://www.microsoft.com/en-us/research/wp-content/uploads/2016/02/Ferreira_Fisher_Sample_Oriented_Tasks.pdf) the authors describe the challenges users face when trying to make judgements about probabilistic data generated through samples. As an example, they look at a bar chart of four years of data (replicated below in Figure 1). Each year has a y-axis value, which is derived from a sample of a larger dataset. For instance, the first value might be the number votes in a given district or riding for 1992, with the average being around 33,000. On top of this is plotted the 95% confidence interval for the mean (see the boxplot lectures for more information, and the yerr parameter of barcharts).
# 
# <br>
# <img src="readonly/Assignment3Fig1.png" alt="Figure 1" style="width: 400px;"/>
# <h4 style="text-align: center;" markdown="1">  &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Figure 1 from (Ferreira et al, 2014).</h4>
# 
# <br>
# 
# A challenge that users face is that, for a given y-axis value (e.g. 42,000), it is difficult to know which x-axis values are most likely to be representative, because the confidence levels overlap and their distributions are different (the lengths of the confidence interval bars are unequal). One of the solutions the authors propose for this problem (Figure 2c) is to allow users to indicate the y-axis value of interest (e.g. 42,000) and then draw a horizontal line and color bars based on this value. So bars might be colored red if they are definitely above this value (given the confidence interval), blue if they are definitely below this value, or white if they contain this value.
# 
# 
# <br>
# <img src="readonly/Assignment3Fig2c.png" alt="Figure 1" style="width: 400px;"/>
# <h4 style="text-align: center;" markdown="1">  Figure 2c from (Ferreira et al. 2014). Note that the colorbar legend at the bottom as well as the arrows are not required in the assignment descriptions below.</h4>
# 
# <br>
# <br>
# 
# **Easiest option:** Implement the bar coloring as described above - a color scale with only three colors, (e.g. blue, white, and red). Assume the user provides the y axis value of interest as a parameter or variable.
# 
# 
# **Harder option:** Implement the bar coloring as described in the paper, where the color of the bar is actually based on the amount of data covered (e.g. a gradient ranging from dark blue for the distribution being certainly below this y-axis, to white if the value is certainly contained, to dark red if the value is certainly not contained as the distribution is above the axis).
# 
# **Even Harder option:** Add interactivity to the above, which allows the user to click on the y axis to set the value of interest. The bar colors should change with respect to what value the user has selected.
# 
# **Hardest option:** Allow the user to interactively set a range of y values they are interested in, and recolor based on this (e.g. a y-axis band, see the paper for more details).
# 
# ---
# 
# *Note: The data given for this assignment is not the same as the data used in the article and as a result the visualizations may look a little different.*

# In[158]:

from IPython.display import display, HTML
display(HTML("<style>.container { width:100% !important; }</style>"))
display(HTML("<style>.container { border-left-width: 0px !important; }</style>"))


# In[1]:

# Use the following data for this assignment:

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

np.random.seed(12345)

df = pd.DataFrame([np.random.normal(32000,200000,3650), 
                   np.random.normal(43000,100000,3650), 
                   np.random.normal(43500,140000,3650), 
                   np.random.normal(48000,70000,3650)], 
                  index=[1992,1993,1994,1995])
ndf = df.T
print(ndf.columns)

mean1992 = ndf[1992].mean()
print(mean1992)

mean1993 = ndf[1993].mean()
print(mean1993)

mean1994 = ndf[1994].mean()
print(mean1994)

mean1995 = ndf[1995].mean()
print(mean1995)

means = [mean1992, mean1993, mean1994, mean1995]
print(means)

ndf.describe()
ndf[1995].count()


# In[22]:

import math
import scipy.stats as st
from matplotlib import cm
import matplotlib as mpl
from mpl_toolkits.axes_grid1 import make_axes_locatable


years = ['1992', '1993', '1994', '1995']
ci95 =[]
sds=[]
prob=[]

y = 1992
x = 0
arb = 42000
c=3650

while y < 1996:
    sd = ndf[y].std()
    m = means[x]
    err = 1.96*sd/math.sqrt(c)
    ciH = m+err
    ciL = m-err
    sds.append(sd)
    ci95.append(err)
    prob.append(st.norm.cdf((arb-m)/(sd/math.sqrt(c))))
    y += 1
    x += 1

#defining color map
plt.clf
fig, ax = plt.subplots()
colors = cm.RdBu(prob) 
cmap = mpl.cm.RdBu

#Make bar charts with a horizontal line
bars = ax.bar(range(len(means)), means, width =1, color = colors, edgecolor='black', yerr =ci95, capsize = 10)
ax.set_xticks(range(len(means)))
ax.set_xticklabels(years)
hline = ax.axhline(arb, color='gray', linestyle = 'dashed', label = 'y-Value')
ax.text(0.05, .95, "Y-Value = {}".format(arb), transform=ax.transAxes)

#code for Color Bar
# create an Axes on the right side of ax. The width of cax will be 5%
# of ax and the padding between cax and ax will be fixed at 0.1 inch.
divider = make_axes_locatable(ax)
cax = divider.append_axes("right", size="5%", pad=0.1)

sm = cm.ScalarMappable(cmap=cmap, norm=plt.Normalize(1, 0))
sm.set_array([])

cbar = plt.colorbar(sm, cax=cax, ax=bars)
cbar.ax.invert_yaxis()

plt.show()
fig.savefig('Wk3 Assign3 Harder Option Figure')


# In[ ]:

#Code to create interactivity
def percentages(arb):
    percentages = []
    a=0
    for bar in bars:
        percentage = (st.norm.cdf((arb-means[a])/(sds[a]/math.sqrt(c))))
        percentages.append(percentage)
        a += 1
    return percentages

def update(arb):
    hline.set_ydata(arb)
    colors = cm.RdBu(percentages(arb))
    for bar, p in zip(bars, colors):
        bar.set_color(p)

update(arb)
        
def onclick(event):
    if event.inaxes == ax:
        update(event.ydata)
        fig.canvas.draw_idle()
        
plt.gcf().canvas.mpl_connect('button_press_event', onclick)


# In[ ]:




# In[78]:

import numpy as np

ax = plt.subplot()
im = ax.imshow(np.arange(100).reshape((10, 10)))

# create an Axes on the right side of ax. The width of cax will be 5%
# of ax and the padding between cax and ax will be fixed at 0.05 inch.
divider = make_axes_locatable(ax)
cax = divider.append_axes("right", size="5%", pad=0.05)

plt.colorbar(im, cax=cax)

plt.show()


# In[ ]:



