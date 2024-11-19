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

df = pd.read_csv('df.csv', index_col='Unnamed: 0')

st.title('Book of Mormon Text Analysis')

with st.sidebar:
    st.subheader('Word Analysis')
    input_word = st.text_input('Enter a word:', value = 'Christ')
    most_least = st.radio('Find the 10:', ['Most Common Words', 'Least Common Words'])

    st.subheader('Phrase Analysis')
    input_phrase = st.text_input('Enter a phrase:', value = 'And it came to pass')


    phrase_length = st.slider('Year', min_value = 1880, max_value =2023, value = 2000)



    if st.button("Click me to turn yourself into a Dog"):
        st.write("Poof! You're Dawg")
    else:
        st.write('')


tab1, tab2, tab3 = st.tabs(['Project', 'Word', 'Phrase'])

with tab1:
    st.write('Add text here')


with tab2:
    st.write('This tab will explore words across individual books in the Book of Mormon.')
    st.subheader('Word Occurances')
    st.write('This first graph is the total number of occurances in each book as well as the entire book of mormon. Use the entry box on the left side of your screen to input a word and the graph will automatically update showing the distribution of the word usage in different books. Hover your mouse of the bar to see the specific values.')    
    # Fig1 = count of words
    df_copy1 = df.copy()
    fig2 = plot_word_histogram(df_copy1, 'text_processed', input_word)
    st.plotly_chart(fig2, key="fig2_chart")

    st.write('This graph is similar to above only that it is normalized by text length. This is helpful because it takes into account the different lengths of books. It basically shows that if each book was the same length then the height of the bar shows how often this word would be used. The units on the bars are word frequency per character in book.')

    # Fig2 = normalized count of words
    df_copy2 = df.copy()
    fig3 = plot_word_histogram_length(df_copy2, 'text_processed', input_word)
    st.plotly_chart(fig3, key="fig3_chart")

    ## Most common/least common words
    df['most_common'], df['least_common'] = zip(*df['text_processed'].apply(get_most_and_least_common_words))
    if most_least == 'Most Common Word':
        result_df = df[['name', 'most_common']]
    if most_least == 'Least Common Word':
        result_df = df[['name', 'least_common']]
    st.dataframe(result_df)

with tab3:
    # fig1 = plot_word_histogram(data, year = year_input, n=n_names)
    fig1 = 1
    # st.plotly_chart(fig)