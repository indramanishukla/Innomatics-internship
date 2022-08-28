from sre_parse import expand_template
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
from math import radians, cos, sin, asin, sqrt
import haversine as hs
import os

path = os.path.dirname(__file__)
my_file = path+'/data/open_pubs.csv'
df = pd.read_csv(my_file, header=None, names=['fsa_id','name','address','postcode','easting','northing','latitude','longitude','local_authority'])


st.title('Pubs near me!')
st.write('This is section where you can search pubs near you, give your coordinates.')

df.latitude.replace('\\N', np.nan, inplace=True)
df.longitude.replace('\\N', np.nan, inplace=True)
df.dropna(inplace=True)


df.latitude = df.latitude.astype('float64')
df.longitude = df.longitude.astype('float64')
df['city'] = [i[-1] for i in df.address.str.split()]

in_col, out_col = st.columns(2)

lat = in_col.number_input('Enter your latitude in Britain', 51.50)
lon = in_col.number_input('Enter your longitude in Britain', 0.12)
find = pd.DataFrame([[lat, lon]], columns=['lat', 'lon'])
out_col.text('Here you are located!')
out_col.map(find)


dist =[]

df.reset_index(drop=True, inplace=True)


def nearest(latitude, lat, longitude, lon):
    near =((df['latitude']-lat)**2+(df['longitude']-lon)**2)**0.5

    return near



df['nearest_eucledian_dist'] = nearest(df.latitude, lat, df.longitude, lon)
data = df.sort_values('nearest_eucledian_dist', ascending=True).head()
st.write(data)
st.text('Five Pubs Nearest to You, Cheers!!!')
st.map(data)

# st.write(dist)