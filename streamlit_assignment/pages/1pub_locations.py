from sre_parse import expand_template
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px


st.title('Pub locations')
df = pd.read_csv("open_pubs.csv", header=None, names=['fsa_id','name','address','postcode','easting','northing','latitude','longitude','local_authority'])
df.latitude.replace('\\N', np.nan, inplace=True)
df.longitude.replace('\\N', np.nan, inplace=True)
df.dropna(inplace=True)


df.latitude = df.latitude.astype('float64')
df.longitude = df.longitude.astype('float64')
df['city'] = [i[-1] for i in df.address.str.split()]

in_col, out_col = st.columns(2)
in_col.text('Here is the list of all the postal codes:')
in_col.dataframe(df.local_authority.value_counts().sort_values(ascending=False), 300, 300)


town = in_col.multiselect('Enter the city you are looking for!', df.local_authority.unique(),default= ['City of Edinburgh','Glasgow City'])

if len(town)==0:
    data = df.copy()
    # st.write(data)
else:
    data = df[df.local_authority.isin(town)]
    # st.write(data)

st.map(data)

# st.dataframe(data)

# st.map(data=df)


