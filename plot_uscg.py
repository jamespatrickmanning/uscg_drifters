# -*- coding: utf-8 -*-
"""
Created on Wed Jun  10 11:39:35 2020
@author: JiM
Routine to plot USCG iSLMDB drifters in our area after downloading a csv file from Linc,
where we selected units from the output of "get_uscg_for_our_area.py"
where our_area is 34-46N, and -77--64W (ie the Northeast Shelf)
"""

import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
import os
os.environ['PROJ_LIB'] = 'c:\\Users\\Joann\\anaconda3\\pkgs\\proj4-5.2.0-ha925a31_1\\Library\share'
from mpl_toolkits.basemap import Basemap

area='NE'
input_file='all_assets_637272425998242740.csv'

def getgbox(area):
  # gets geographic box based on area
  if area=='SNE':
    gbox=[-71.,-66.,39.,42.] # for SNE
  elif area=='OOI':
    gbox=[-72.,-69.5,39.5,41.5] # for OOI
  elif area=='GBANK':
    gbox=[-70.,-64.,39.,42.] # for GBANK
  elif area=='GS':           
    gbox=[-71.,-63.,38.,42.5] # for Gulf Stream
  elif area=='NorthShore':
    gbox=[-71.,-69.5,41.5,43.] # for north shore
  elif area=='CCBAY':
    gbox=[-70.75,-69.8,41.5,42.23] # CCBAY
  elif area=='inside_CCBAY':
    gbox=[-70.75,-70.,41.7,42.23] # CCBAY
  elif area=='NEC':
    gbox=[-69.,-64.,39.,43.5] # NE Channel
  elif area=='NE':
    gbox=[-76.,-64.,35.,46.] # NE Channel  
  return gbox

def make_basemap(gb):
    m = Basemap(projection='merc',lon_0=(gb[0]+gb[1])/2.,lat_0=(gb[2]+gb[3])/2.,lat_ts=0,llcrnrlat=gb[2],urcrnrlat=gb[3],\
                llcrnrlon=gb[0],urcrnrlon=gb[1],rsphere=6371200.,resolution='l',area_thresh=100)# JiM changed resolution to "c" for crude
    # draw coastlines
    m.drawcoastlines()
    parallels = np.arange(0.,90,3.)
    m.drawparallels(parallels,labels=[1,0,0,0],fontsize=14,linewidth=0)
    # draw meridians
    meridians = np.arange(180.,360.,3.)
    m.drawmeridians(meridians,labels=[0,0,0,1],fontsize=14,linewidth=0)
    return m

# Make a basemap
gb=getgbox(area)
m=make_basemap(gb)
df=pd.read_csv(input_file)
#df=df[' LATITUDE'].replace('',np.nan,inplace=True)
#df=df.dropna(subset=[' LATITUDE'], inplace=True)
df=df[~df[' LATITUDE'].str.contains('LATITUDE')]
df[' LATITUDE']=pd.to_numeric(df[' LATITUDE'],downcast="float")
df[' LONGITUDE']=pd.to_numeric(df[' LONGITUDE'],downcast="float")
x,y=m(df[' LONGITUDE'].values,df[' LATITUDE'].values)
plt.plot(x,y,'r.',markersize=4)
plt.title('USCG drifters May 2019 - May 2020')



