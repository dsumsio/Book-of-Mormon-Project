import streamlit as st


st.title('Book of Mormon Text Analysis Project')

with st.sidebar:
    input_word = st.text_input('Enter a word:', value = 'Christ')
    input_phrase = st.text_input('Enter a phrase:', value = 'And it came to pass')

    n_names = st.radio('Number of names per sex', [3,5,10])
    if st.button("Click me to turn yourself into a Dog"):
        st.write("Poof! You're Dawg")
    else:
        st.write('')