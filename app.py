import streamlit as st
import pandas as pd
#
from youtube import get_data
import plotly.express as px
from helper import count_words, count_words2
import httpx
#Create a template witwh markdown and html
st.set_page_config(layout='wide')

st.sidebar.markdown("<center> <img src='https://png.pngtree.com/png-vector/20221018/ourmid/pngtree-youtube-social-media-round-icon-png-image_6315993.png' with=100 height=100 /> </center> <h1 Style='display:inline-block'> Youtube Analytics </h1>", unsafe_allow_html=True)
st.sidebar.markdown("This dashboard allows you analyses trending youtube using python and Streamlit")
st.sidebar.markdown("To get started <ol><li>Enter the <i> search</i> you wish to analyses </li> <li> Get data </i><li> Get analyse</ol>", unsafe_allow_html=True)
search = st.text_input('Search here', value='')
number = st.text_input('Number of resuts', value='')

if st.button('Get data'):
    st.write('Searching word:', search, 'with this amount of results:', number)
    get_data(str(search), int(number))
    #if have any data do this:
    if get_data:
        df = pd.read_csv('test.csv')
        st.markdown("# This is a document .csv of your search")
        st.dataframe(df)
        st.markdown("# How many views have the title of your search?")
        fig = px.histogram(df, x='Title', y='View Count:')
        st.plotly_chart(fig, use_container_width=True)
        

        value = list(df['Title'].values)
        diccionario = count_words(value)
        

        st.markdown("# What are the most used words in the search title?")
        fig2 = px.histogram(df, x=diccionario.keys(), y=diccionario.values())
        st.plotly_chart(fig2, use_container_width=True)


        value2 = list(df['Keywords Tags'].values)
        diccionario2 = count_words2(value2)
        st.markdown("# What are the most used words in the search Tags?")
        fig3 = px.histogram(df, x=diccionario2.keys(), y=diccionario2.values())
        st.plotly_chart(fig3, use_container_width=True)

        
        st.markdown("# What are the most country in the search title?")
        fig4 = px.pie(df, values=df['View Count:'], names='Country', title='Population of country in your search')
        
        st.plotly_chart(fig4, use_container_width=True)




