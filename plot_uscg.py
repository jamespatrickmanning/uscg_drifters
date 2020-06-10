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
#NOTE: I needed the following two lines on my Toshiba laptop runs in order for basemap to work
#import os
#os.environ['PROJ_LIB'] = 'c:\\Users\\Joann\\anaconda3\\pkgs\\proj4-5.2.0-ha925a31_1\\Library\share'
from mpl_toolkits.basemap import Basemap
from scipy.interpolate import griddata # needed for gridding bathymetry

area='NE' # Northeast shelf area
input_file='all_assets_637272425998242740.csv' # all the drifter data for the following period on NE Shelf
time_period='May 2019 - May 2020'
gs=50      # number of bins in the x and y direction so,  if you want more detail, make it bigger to contour depth
ss=100     # subsample depth input data so, if you want more detail, make it smaller 
cont=[-200] # 200 meter isobath

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
    gbox=[-76.,-66.,35.,44.5] # NE Shelf 
  return gbox

def add_isobath(m,gs,ss,cont):
    # draws an isobath on map given gridsize,subsample rate,and contour level
    # these inputs are typically 50, 100, and 200 for entire shelf low resolution
    url='http://apdrc.soest.hawaii.edu/erddap/griddap/hawaii_soest_794e_6df2_6381.csv?b_bathy[(0000-01-01T00:00:00Z):1:(0000-01-01T00:00:00Z)][(35.0):1:(45.0)][(-76.0):1:(-66.0)]'
    df=pd.read_csv(url)
    df=df.drop('time',axis=1)
    df=df[1:].astype('float')# removes unit row and make all float          
    Xb,Yb=m.makegrid(gs,gs) # where "gs" is the gridsize specified in hardcode section
    Xb,Yb=m(Xb,Yb) # converts grid to basemap coordinates .
    xlo,yla=m(df['longitude'][0:-1:ss].values,df['latitude'][0:-1:ss].values)
    zi = griddata((xlo,yla),df['b_bathy'][0:-1:ss].values,(Xb,Yb),method='linear')
    CS=m.contour(Xb,Yb,zi,cont,zorder=0,color='k',linewidths=[.3],linestyles=['dashed'])
    plt.clabel(CS, inline=1, fontsize=8,fmt='%d')
def make_basemap(gb):
    m = Basemap(projection='merc',lon_0=(gb[0]+gb[1])/2.,lat_0=(gb[2]+gb[3])/2.,lat_ts=0,llcrnrlat=gb[2],urcrnrlat=gb[3],\
                llcrnrlon=gb[0],urcrnrlon=gb[1],rsphere=6371200.,resolution='l',area_thresh=100,suppress_ticks=True)# JiM changed resolution to "c" for crude
    # draw coastlines
    #m.drawcoastlines()
    m.fillcontinents(color='grey',lake_color='grey')
    parallels = np.arange(0.,90,3.)
    m.drawparallels(parallels,labels=[1,0,0,0],fontsize=10,linewidth=0)
    # draw meridians
    meridians = np.arange(180.,360.,3.)
    m.drawmeridians(meridians,labels=[0,0,0,1],fontsize=10,linewidth=0)
    return m

# MAIN PROGRAM STARTS HERE
# Make a basemap
gb=getgbox(area)
m=make_basemap(gb)        # adds coastline
print('adding isobath which takes a minute ... comment out to save time')
add_isobath(m,gs,ss,cont) # adds isobath
df=pd.read_csv(input_file)
#df=df[' LATITUDE'].replace('',np.nan,inplace=True)
#df=df.dropna(subset=[' LATITUDE'], inplace=True)
df=df[~df[' LATITUDE'].str.contains('LATITUDE')] # gets rid of extra header lines
df[' LATITUDE']=pd.to_numeric(df[' LATITUDE'],downcast="float") # converts string to float
df[' LONGITUDE']=pd.to_numeric(df[' LONGITUDE'],downcast="float")
drifter_ids=list(np.unique(df['Asset Id'].values))
for k in drifter_ids:
    df1=df[df['Asset Id']==k]
    x,y=m(df1[' LONGITUDE'].values,df1[' LATITUDE'].values) # converts to basemap coordinates
    plt.plot(x,y,'-')#,markersize=4)
plt.title('USCG drifters '+time_period)



