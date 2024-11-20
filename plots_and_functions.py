import re
from nltk.stem import WordNetLemmatizer
from nltk.corpus import wordnet
from collections import Counter
import matplotlib.pyplot as plt
import plotly.express as px
import streamlit as st
import pandas as pd

#### REMOVE these

## with open('mormon13.txt', 'r') as file:
   # bom_text = file.read()

## df = pd.read_csv('df.csv')

# region Functions

def preprocess_text(text):
    text = text.lower().replace('\n', ' ')  # Convert text to lowercase and remove newlines
    lemmatizer = WordNetLemmatizer() # Tokenize and lemmatize words
    words = re.findall(r'\b\w+\b', text)  # Extract words ignoring punctuation
    # Remove numeric tokens and lemmatize the rest
    lemmatized_words = [lemmatizer.lemmatize(word) for word in words if not word.isnumeric()]
    # Join words back into a single string
    processed_text = ' '.join(lemmatized_words)

    return processed_text

def get_most_common_phrases(text, min_phrase_length=2, max_phrase_length=6, top_n=10):    
    words = re.findall(r'\b\w+\b', text)  # Tokenize the text by words
    top_phrases = {} # Dictionary to hold the top phrases for each length
    
    # Loop over phrase lengths from 2 up to max_phrase_length
    for n in range(min_phrase_length, max_phrase_length + 1):
        # Create n-word phrases using zip to get overlapping phrases
        phrases = [' '.join(words[i:i+n]) for i in range(len(words) - n + 1)]
        
        # Count phrases and get the top n most common
        phrase_counts = Counter(phrases).most_common(top_n)
        top_phrases[f"{n}-word phrases"] = phrase_counts
    
    return top_phrases

def get_most_common_phrases(text, phrase_length=4, top_n=10):    
    words = re.findall(r'\b\w+\b', text)  # Tokenize the text by words
    # Create n-word phrases using zip to get overlapping phrases
    phrases = [' '.join(words[i:i+phrase_length]) for i in range(len(words) - phrase_length + 1)]
    # Count phrases and get the top n most common
    phrase_counts = Counter(phrases).most_common(top_n)
    return phrase_counts

def get_most_and_least_common_words(text):
    words = text.split()
    word_counts = Counter(words)
    
    # Get the 10 most common words
    most_common = [word for word, _ in word_counts.most_common(10)]
    most_common_str = ", ".join(most_common) if most_common else None
    
    # Get the 10 least common words
    least_common = [word for word, _ in word_counts.most_common()[-10:]]
    least_common_str = ", ".join(least_common) if least_common else None
    
    return most_common_str, least_common_str

def count_occurrences(long_string, search_term):
    preprocessed_long_string = preprocess_text(long_string)
    preprocessed_search_term = preprocess_text(search_term)
    
    # Use regex to match whole words
    matches = re.findall(rf'\b{re.escape(preprocessed_search_term)}\b', preprocessed_long_string)
    return len(matches)

def preprocess_text_2(text):
    lemmatizer = WordNetLemmatizer()
    # Convert to lowercase and replace newlines with spaces
    text = text.lower().replace('\n', ' ')
    # Extract words using regex (ignores punctuation)
    words = re.findall(r'\b\w+\b', text)
    # Lemmatize the words
    lemmatized_words = [lemmatizer.lemmatize(word) for word in words]
    return lemmatized_words


def find_word_instances(df, book_name, input_word):
    """
    Find all instances of a word in the text column of the DataFrame.
    """
    lemmatizer = WordNetLemmatizer()
    input_word = lemmatizer.lemmatize(input_word.lower())  # Preprocess the input word
    
    # Filter the DataFrame by book name if needed
    if book_name.lower() != "entire book":
        filtered_df = df[df['name'].str.lower() == book_name.lower()]
    else:
        filtered_df = df  # Use the entire DataFrame
    
    # Initialize a list to store the results
    results = []
    
    # Iterate through the filtered DataFrame
    for _, row in filtered_df.iterrows():
        # Preprocess the text into lemmatized words
        words = preprocess_text_2(row['text_processed'])
        # Iterate through the words and find matches
        for i, word in enumerate(words):
            if word == input_word:
                # Extract 5 words before and after the match
                snippet = ' '.join(words[max(0, i - 5):i + 6])
                results.append(snippet)
    
    # Return a DataFrame with all found snippets
    df_final = pd.DataFrame({'Text': results})
    return df_final


# endregion

# region Plots - WORDS

def plot_word_histogram(df, text_column, search_term):
    # Ensure the DataFrame has a 'count' column based on occurrences of the search term
    df['count'] = df[text_column].apply(lambda text: count_occurrences(text, search_term))
    
    # Create the histogram
    fig = px.bar(
        df,
        x='name',  # Ensure 'name' exists in your DataFrame
        y='count',  # Using count as the y-axis
        title=f"Occurrences of '{search_term}' In Each Book",
        labels={'name': 'Names', 'count': 'Occurrences'},
    )
    
    # Customize the layout
    fig.update_layout(
        xaxis_title="Book",
        yaxis_title="Count",
        xaxis=dict(tickangle=45),  # Rotate x-axis labels
        bargap=0.1  # Adjust bar spacing
    )
    
    # Show the figure
    return fig


def plot_word_histogram_length(df, text_column, search_term):
    # Ensure the DataFrame has a 'count' column based on occurrences of the search term
    df['count'] = df[text_column].apply(lambda text: count_occurrences(text, search_term))
    
    # Calculate the length of each text
    df['str_length'] = df[text_column].apply(len)
    
    # Normalize the count by dividing by text length
    df['normalized_count'] = df['count'] / df['str_length']
    
    # Create the bar plot using normalized counts
    fig = px.bar(
        df,
        x='name',  # Ensure 'name' exists in your DataFrame
        y='normalized_count',  # Use normalized counts as the y-axis
        title=f"Occurrences of '{search_term}' In Each Book (Normalized by Text Length)",
        labels={'name': 'Names', 'normalized_count': 'Occurrences (Normalized)'},
    )
    
    # Customize the layout
    fig.update_layout(
        xaxis_title="Book",
        yaxis_title="Count/Length of Book",
        xaxis=dict(tickangle=45),  # Rotate x-axis labels
        bargap=0.1  # Adjust bar spacing
    )
    
    # Show the figure
    return fig

# endregion

# region Plots - PHRASES
def get_most_common_phrases(text, min_phrase_length=2, max_phrase_length=6, top_n=10):
    words = re.findall(r'\b\w+\b', text)  # Tokenize the text by words
    top_phrases = {}  # Dictionary to hold the top phrases for each length
    
    # Loop over phrase lengths from min_phrase_length to max_phrase_length
    for n in range(min_phrase_length, max_phrase_length + 1):
        # Create n-word phrases using zip to get overlapping phrases
        phrases = [' '.join(words[i:i+n]) for i in range(len(words) - n + 1)]
        
        # Count phrases and get the top_n most common
        phrase_counts = Counter(phrases).most_common(top_n)
        top_phrases[f"{n}-word phrases"] = phrase_counts
    
    return top_phrases

def plot_top_phrases(df, text_column, phrase_length, max_phrases):
    # Create a list to hold top phrases across all rows
    all_phrases = []
    for _, row in df.iterrows():
        top_phrases = get_most_common_phrases(row[text_column], min_phrase_length=phrase_length, max_phrase_length=phrase_length, top_n=max_phrases)
        all_phrases.extend(top_phrases.get(f"{phrase_length}-word phrases", []))  # Collect all phrases from each row

    # Combine counts of the same phrases
    combined_phrases = Counter(dict(all_phrases)).most_common(max_phrases)

    # Debugging: Check the combined phrases
    print("Combined Phrases:", combined_phrases)

    # Handle case where no phrases are found
    if not combined_phrases:
        st.warning(f"No {phrase_length}-word phrases found.")
        return None

    # Create a DataFrame for the phrases and their counts
    phrase_df = pd.DataFrame(combined_phrases, columns=['Phrase', 'Count'])

    # Plot a horizontal bar chart
    fig = px.bar(
        phrase_df,
        x='Count',
        y='Phrase',
        orientation='h',  # Horizontal bars
        title=f"Top {max_phrases} {phrase_length}-Word Phrases",
        labels={'Phrase': 'Phrase', 'Count': 'Occurrences'}
    )

    # Customize the layout
    fig.update_layout(
        yaxis=dict(tickangle=0),  # Keep y-axis labels readable
        xaxis_title="Occurrences",
        yaxis_title="Phrases",
        bargap=0.1,  # Adjust bar spacing
    )

    return fig

# endregion

# region Plots - Authors
def plot_word_histogram_author(df, text_column, search_term):
    # Ensure the DataFrame has a 'count' column based on occurrences of the search term
    df['count'] = df[text_column].apply(lambda text: count_occurrences(text, search_term))
    
    # Create the histogram
    fig = px.bar(
        df,
        x='Writer',  # Ensure 'name' exists in your DataFrame
        y='count',  # Using count as the y-axis
        title=f"Occurrences of '{search_term}' In Each Book",
        labels={'Writer': 'Writer', 'count': 'Occurrences'},
    )
    
    # Customize the layout
    fig.update_layout(
        xaxis_title="Writer",
        yaxis_title="Count",
        xaxis=dict(tickangle=45),  # Rotate x-axis labels
        bargap=0.1  # Adjust bar spacing
    )
    
    # Show the figure
    return fig


def plot_word_histogram_length_author(df, text_column, search_term):
    # Ensure the DataFrame has a 'count' column based on occurrences of the search term
    df['count'] = df[text_column].apply(lambda text: count_occurrences(text, search_term))
    
    # Calculate the length of each text
    df['str_length'] = df[text_column].apply(len)
    
    # Normalize the count by dividing by text length
    df['normalized_count'] = df['count'] / df['str_length']
    
    # Create the bar plot using normalized counts
    fig = px.bar(
        df,
        x='Writer',  # Ensure 'name' exists in your DataFrame
        y='normalized_count',  # Use normalized counts as the y-axis
        title=f"Occurrences of '{search_term}' In Each Book (Normalized by Text Length)",
        labels={'Writer': 'Writer', 'normalized_count': 'Occurrences (Normalized)'},
    )
    
    # Customize the layout
    fig.update_layout(
        xaxis_title="Writer",
        yaxis_title="Count/Length of Writer's Words",
        xaxis=dict(tickangle=45),  # Rotate x-axis labels
        bargap=0.1  # Adjust bar spacing
    )
    
    # Show the figure
    return fig
