# -*- coding: utf-8 -*-
"""
Created on Wed Jun  10 11:39:35 2020

@author: JiM
Routine to plot USCG iSLMDB drifters in our area after downloading a csv file from Linc,
where we selected units from the output of "get_uscg_for_our_area.py"
where our_area is 34-46N, and -77--64W (ie the Northeast Shelf)

"""

import pandas as pd
from mpl_toolkits.basemap import Basemap

area='NEC'
input_file='c:\\users\\DELL\\Downloads\\all_assets_637272425998242740.csv'

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
  return gbox

def make_basemap(gb):
    m = Basemap(projection='stere',lon_0=(gb[0]+gb[1])/2.,lat_0=(gb[2]+gb[3])/2.,lat_ts=0,llcrnrlat=gb[2],urcrnrlat=gb[3],\
                llcrnrlon=gb[0],urcrnrlon=gb[1],rsphere=6371200.,resolution='f',area_thresh=100)# JiM changed resolution to "c" for crude
    # draw coastlines, state and country boundaries, edge of map.
    m.drawcoastlines()
    m.drawstates()
    m.drawcountries()
    parallels = np.arange(0.,90,1.)
    m.drawparallels(parallels,labels=[1,0,0,0],fontsize=20)
    # draw meridians
    meridians = np.arange(180.,360.,1.)
    m.drawmeridians(meridians,labels=[0,0,0,1],fontsize=20)
    # draw filled contours.
    dept_clevs=[50,100, 150,300,1000]
    dept_cs=m.contour(x,y,depth,dept_clevs,colors='black')
    plt.clabel(dept_cs, inline = True, fontsize =15,fmt="%1.0f")
    return m

# Make a basemap
gb=getgbox(area)
make_basemap(gb)
df=pd.read_csv(input_file)
x,y=m(df['LONGITUDE'].values,df[' LATITUDE'].values)
plot(x,y,'.')

    