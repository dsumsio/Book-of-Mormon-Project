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
df_writers = pd.read_csv('author_bom.csv')

st.title('Book of Mormon Text Analysis')

with st.sidebar:
    st.subheader('WORD ANALYSIS')
    input_word = st.text_input('Enter a word:', value = 'Christ')
    most_least = st.radio('Find the 10:', ['Most Common Words', 'Least Common Words'])

    st.subheader('PHRASE ANALYSIS')
    phrase_length = st.slider('Select Phrase Length', min_value = 2, max_value =10, value = 4)
    max_phrases = st.slider("Select number of phrases to display", min_value=5, max_value=20, value=10)



    if st.button("Click me to turn yourself into a Dog"):
        st.write("Poof! You're Dawg")
    else:
        st.write('')


tab1, tab2, tab3, tab4 = st.tabs(['Project', 'Word', 'Phrase', 'Author'])

with tab1:
    st.write('Add text here')


with tab2:
    st.write('This tab will explore words across individual books in the Book of Mormon.')
    st.subheader('Word Occurances')
    st.write('This first graph is the total number of occurances in each book as well as the entire book of mormon. Use the entry box on the left side of your screen to input a word and the graph will automatically update showing the distribution of the word usage in different books. Hover your mouse of the bar to see the specific values.')    
    # Fig1 = count of words
    df_copy1 = df.copy()
    fig1 = plot_word_histogram(df_copy1, 'text_processed', input_word)
    st.plotly_chart(fig1, key="fig1_chart")

    st.write('This graph is similar to above only that it is normalized by text length. This is helpful because it takes into account the different lengths of books. It basically shows that if each book was the same length then the height of the bar shows how often this word would be used. The units on the bars are word frequency per character in book.')

    # Fig2 = normalized count of words
    df_copy2 = df.copy()
    fig2 = plot_word_histogram_length(df_copy2, 'text_processed', input_word)
    st.plotly_chart(fig2, key="fig2_chart")

    st.subheader('Most and Least Common Words')
    st.write('This section explores the most and least common 10 words across books and the entire book of mormon. Use the Toggle on the left hand side of the page to switch between the most common and least common words. If output is truncated because of the length, hover mouse over top right corner of the table to make it full screen')
    ## Most common/least common words
    df['most_common'], df['least_common'] = zip(*df['text_processed'].apply(get_most_and_least_common_words))
    if most_least == 'Most Common Words':
        result_df = df[['name', 'most_common']]
    elif most_least == 'Least Common Words':
        result_df = df[['name', 'least_common']]
    st.dataframe(result_df)

with tab3:
    st.write('This tab will explore phrases across individual books in the Book of Mormon.')
    st.subheader('Phrase Occurances')
    st.write('This first graph is the total number of occurances in each book as well as the entire book of mormon of the specified phrase. Use the entry box on the left side of your screen to input a phrase and the graph will automatically update showing the distribution of the word usage in different books. Hover your mouse of the bar to see the specific values.')    
    df_copy3 = df.copy()
    fig3 = plot_top_phrases(df_copy3, 'text_processed', phrase_length, max_phrases)
    st.plotly_chart(fig3, key="fig3_chart")

with tab4:
    st.write('One of the greatest lessons I have learned in this class so far is to really try to understand the writer and author of the story. Often times they are trying to communicate something by using history. As we better understand their background and reasoning for inlcuding certain phrases we can have a greater appreciation for the messages. This is a simplistic attempt to quantify this. Use the Word input textbox on the left so see the frequency used by the writers. Hover your mouse over the specific columns in the plots to see the specific values.')
    df_writers_copy1 = df_writers.copy()
    fig4 = plot_word_histogram(df_writers_copy1, 'text_processed', input_word)
    st.plotly_chart(fig4, key="fig4_chart")

    st.write("This graph is similar to above only that it is normalized by text length. This is helpful because it takes into account the different lengths of writer content. It basically shows that if each writer wrote the same amount then the height of the bar shows how often this word would be used. The units on the bars are word frequency per character in author's books.")

    # Fig2 = normalized count of words
    df_writers_copy2 = df_writers.copy()
    fig5 = plot_word_histogram_length(df_writers_copy2, 'text_processed', input_word)
    st.plotly_chart(fig5, key="fig5_chart")
