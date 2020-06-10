# -*- coding: utf-8 -*-
"""
Created on Mon Jun  8 11:39:35 2020

@author: DELL
"""

import pandas as pd
df=pd.read_csv('c:\\users\\DELL\\Downloads\\LiNC_Asset_Status_2020-06-03.csv')
df=df[0:241] # use only the first 241 rows since the others do not have lat/lon
# make all lat and lon floats rather than strings
df['Latitude']=pd.to_numeric(df['Latitude'],downcast="float")
df['Longitude']=pd.to_numeric(df['Longitude'],downcast="float")
# find units in our area
df=df[(df['Latitude']>34.0) & (df['Latitude']<46.0)]
df=df[(df['Longitude']>-77.0) & (df['Longitude']<-64.0)]
print(df['Asset Name'].values)
df.to_csv('uscg_our_area')
