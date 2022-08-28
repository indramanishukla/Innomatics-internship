from sre_parse import expand_template
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import os

path = os.path.dirname(__file__)
my_file = path+'/pages/data/open_pubs.csv'

hex = st.container()
description = st.container()

with hex:
    df = pd.read_csv(my_file, header=None, names=['fsa_id','name','address','postcode','easting','northing','latitude','longitude','local_authority'])
    st.title('Pubs Dashboard')
    st.header('The top 5 rows are shown below in the dataframe')
    st.markdown('This is the dashboard which explains you the dataset')


# my_expander = st.expander('dig down here')
# my_expander.write('Hello there!')
# clicked = my_expander.button('Click me!')

# st.code(body='''code''', language='python')

    st.dataframe(df.head(), 10000, 200)

with description:
    st.subheader('This is the description of data')
    describe = df.local_authority.value_counts(ascending=False).head(20)
    
    # fig = px.histogram(x = df.local_authority.value_counts().sort_values(ascending=False).head(20).index, y=df.local_authority.value_counts().sort_values(ascending=False).head(20), labels={"y":'counts'})
    fig = px.bar(describe, labels={'value':'count', 
    'index':'local_authority'}, title='Top 20 local_authority with max number of pubs').update_layout(showlegend=False).update_xaxes(tickangle=270)
    st.plotly_chart(fig)

    describe = df.local_authority.value_counts(ascending=True).head(20)
    fig = px.bar(describe, labels={'value':'count', 
    'index':'local_authority'}, title='Top 20 local_authority with least number of pubs').update_layout(showlegend=False).update_xaxes(tickangle=270)
    st.plotly_chart(fig)
    st.markdown('* **Country Durham, Leeds and Conwall are the top 3 location with maximum number of pubs**')
    st.markdown('* **Isles of Scilly, Na h-Eileanan Siar and East Renfrewshire are the location with least number of pubs**')


    describe = df.name.value_counts(ascending=False).head(20)
    fig = px.bar(describe, labels={'value':'count', 
    'index':'name of pub'}, title='Top 20 pubs according to frequency').update_layout(showlegend=False).update_xaxes(tickangle=270)
    st.plotly_chart(fig)

    my_expander = st.expander('Feature Engineering to know across city distribution of pubs')
    df['city'] = [i[-1] for i in df.address.str.split()]
    describe = df.city.value_counts(ascending=False).head(20)
    fig = px.bar(describe, labels={'value':'count', 
    'index':'cities'}, title='Top 20 cities with highest number of pubs').update_layout(showlegend=False).update_xaxes(tickangle=270)
    my_expander.plotly_chart(fig)
    my_expander.markdown('* **London has the highest number of pubs followed by Kent followed by Sussex**')