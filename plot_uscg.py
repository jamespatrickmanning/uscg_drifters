# -*- coding: utf-8 -*-
"""
Created on Wed Jun  10 11:39:35 2020
@author: JiM
Routine to plot USCG iSLMDB drifters in our area after downloading a csv file from Linc,
where we selected units from the output of "get_uscg_for_our_area.py"
where our_area is 34-46N, and -77--64W (ie the Northeast Shelf)

Modifed Jun 14, 2020 to export tracks in the standard "drift_.dat" format
"""

import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
from datetime import datetime as dt
from datetime import timedelta as td
#NOTE: I needed the following two lines on my Toshiba laptop runs
import os
os.environ['PROJ_LIB'] = 'c:\\Users\\Joann\\anaconda3\\pkgs\\proj4-5.2.0-ha925a31_1\\Library\share'
from mpl_toolkits.basemap import Basemap
from scipy.interpolate import griddata

area='NE'
input_file='all_assets_637272425998242740.csv'
output_file='drift_uscg_2019_1.dat'
gs=50      # number of bins in the x and y direction so,  if you want more detail, make it bigger
ss=100     # subsample input data so, if you want more detail, make it smaller
cont=[-200]

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
def write_to_dat_file(df,output_file):
    # routine to export a standard .dat file for subsequent processing
    f=open(output_file,'a')
    j=1
    for k in range(len(df)):
      try: # had to skip the bad points with this
        #print(k)
        mth=dt.strptime('{}'.format(int(df[' DAY'][k])),'%j').month
        day_of_mth=dt.strptime('{}'.format(int(df[' DAY'][k])),'%j').day
        #yd=str((dt(int(df[' YEAR'][k]),mth,day_of_mth,int(df[' HOUR'][k]),int(df[' MIN'][k]))-dt(int(df[' YEAR'][k]),1,1))/td(1))# calculates a fractional yearday
        yd='{:.4f}'.format((dt(int(df[' YEAR'][k]),mth,day_of_mth,int(df[' HOUR'][k]),int(df[' MIN'][k]))-dt(int(df[' YEAR'][k]),1,1))/td(1))# calculates a fractional yearday
        if (k==0) or ((k>0) & (df['Asset Id'][k]!=df['Asset Id'][k-1])):
            # generate a new "deployment_id" w/id,esn,mth,dat,hr,mn,yd,lat,lon,
            if mth>9:
                mth1=0 # we use "0" for 
            else:
                mth1=mth
            id1=df[' GPS_YEAR'][k][-2:]+str(mth1)+str(int(df[' LATITUDE'][0]))+str(abs(int(df[' LONGITUDE'][0])))
            if k==0:
                id2=id1
            else:
                if id1==id2:# new ESN in the same time/mth block
                    j=j+1#increment the deployment id
                    id2=id1#save id for next time
                else:
                    j=1
            id=id1+str(j) # adds the incremental number for this month,lat,lon block
        f.write(str(id)+' '+df['Asset Id'][k][-6:]+' '+str(mth)+'  '+str(day_of_mth)+'  '+df[' HOUR'][k]+'  '+df[' MIN'][k]+'  '+yd+'  '+str(df[' LONGITUDE'][k])+'  '+str(df[' LATITUDE'][k])+' -1.0'+str(df[' SST'][k])+'\n')
      except:
        continue  
    f.close()
# Make a basemap
gb=getgbox(area)
m=make_basemap(gb)        # adds coastline
print('adding isobath which takes a minute so it is commented out to save time')
#add_isobath(m,gs,ss,cont) # adds isobath
df=pd.read_csv(input_file,index_col='Data Date (UTC)')
df=df[~df[' LATITUDE'].str.contains('LATITUDE')] # gets rid of extra header lines
df.index = pd.to_datetime(df.index, format="%Y-%m-%d %H:%M:%S")
df[' LATITUDE']=pd.to_numeric(df[' LATITUDE'],downcast="float") # converts string to float
df[' LONGITUDE']=pd.to_numeric(df[' LONGITUDE'],downcast="float")
drifter_ids=list(np.unique(df['Asset Id'].values))
f=open(output_file,'w')
f.write(output_file+'\n')
f.close()
for k in drifter_ids:
    df1=df[df['Asset Id']==k]
    df1=df1.sort_index()# sorts by time
    write_to_dat_file(df1,output_file) # exports/appends data to drift_uscg_2019_1.dat
    x,y=m(df1[' LONGITUDE'].values,df1[' LATITUDE'].values) # converts to basemap coordinates
    plt.plot(x,y,'-')#,markersize=4)
time_range=str(min(df.index).month)+'/'+str(min(df.index).year)+'-'+str(max(df.index).month)+'/'+str(max(df.index).year)
plt.title('USCG drifters '+time_range)



