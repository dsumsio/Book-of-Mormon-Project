import streamlit as st
import pandas as pd
import plotly.express as px
from plots_and_functions import *
import re
import nltk
nltk.download('wordnet')
from nltk.stem import WordNetLemmatizer
from nltk.corpus import wordnet
from collections import Counter
import matplotlib.pyplot as plt

df = pd.read_csv('df.csv')

with open('mormon13.txt', 'r') as file:
    bom_text = file.read()

st.title('Book of Mormon Text Analysis Project')

with st.sidebar:
    input_word = st.text_input('Enter a word:', value = 'Christ')
    input_phrase = st.text_input('Enter a phrase:', value = 'And it came to pass')

    n_names = st.radio('Number of names per sex', [3,5,10])
    if st.button("Click me to turn yourself into a Dog"):
        st.write("Poof! You're Dawg")
    else:
        st.write('')


tab1, tab2 = st.tabs(['Entire BOM', 'Individual Books'])
with tab1:
    # fig1 = plot_word_histogram(data, year = year_input, n=n_names)
    fig1 = 1
    # st.plotly_chart(fig)

with tab2:
    st.write('This tab will explore words and phrases across individual books in the Book of Mormon.')
    fig2 = plot_word_histogram(df, 'text_processed', input_word)
    st.plotly_chart(fig2)