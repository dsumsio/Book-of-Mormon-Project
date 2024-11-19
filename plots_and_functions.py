import re
from nltk.stem import WordNetLemmatizer
from nltk.corpus import wordnet
from collections import Counter
import matplotlib.pyplot as plt
import plotly.express as px

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
    # Preprocess the search term
    preprocessed_search_term = preprocess_text(search_term)
    
    # Count occurrences
    count = long_string.count(preprocessed_search_term)
    return count


# endregion

# region Plots - WORDS
import plotly.express as px

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
lemmatizer = WordNetLemmatizer()
def preprocess_text(text):
    # Tokenize, lemmatize, and join the words back into a single string
    tokens = word_tokenize(text.lower())  # Tokenize and lowercase
    lemmatized_tokens = [lemmatizer.lemmatize(token) for token in tokens]
    return ' '.join(lemmatized_tokens)

# Helper function to count phrase occurrences
def count_phrase_occurrences(text, phrase):
    # Escape special characters in the phrase for regex, count all non-overlapping matches
    return len(re.findall(re.escape(phrase), text, flags=re.IGNORECASE))

# Function to create the plot
def plot_word_histogram(df, text_column, search_term):
    # Preprocess text column and search term
    df['processed_text'] = df[text_column].apply(preprocess_text)
    processed_search_term = preprocess_text(search_term)
    
    # Ensure the DataFrame has a 'count' column based on occurrences of the processed search term
    df['count'] = df['processed_text'].apply(lambda text: count_phrase_occurrences(text, processed_search_term))
    
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











