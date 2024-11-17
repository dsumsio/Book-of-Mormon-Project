import re
from nltk.stem import WordNetLemmatizer
from nltk.corpus import wordnet
from collections import Counter
import matplotlib.pyplot as plt

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

def most_common_words(text, top_n=10):
    # Use regular expressions to remove punctuation and split by whitespace
    words = re.findall(r'\b\w+\b', text.lower())
    word_counts = Counter(words)
    
    # Get the most common words
    most_common = word_counts.most_common(top_n)
    
    return most_common

def count_occurrences(long_string, search_term):
    # Preprocess the search term
    preprocessed_search_term = preprocess_text(search_term)
    
    # Count occurrences
    count = long_string.count(preprocessed_search_term)
    return count


# endregion

# region Plots
def plot_word_histogram(df, text_column, search_term):
    # Apply count_occurrences to the text column
    df['count'] = df[text_column].apply(lambda text: count_occurrences(text, search_term))
    
    # Create the figure
    fig, ax = plt.subplots(figsize=(10, 6))
    
    # Plot the bar chart using df['name'] for the x-axis
    ax.bar(df['name'], df['count'], color='skyblue')
    
    # Set labels and title
    ax.set_xlabel('Document Name', fontsize=12)
    ax.set_ylabel('Count of Search Term', fontsize=12)
    ax.set_title(f"Occurrences of '{search_term}' in Each Document", fontsize=14)
    
    # Adjust the x-ticks to show the document names
    ax.set_xticks(df['name'])  # Set the positions of the ticks to df['name']
    ax.set_xticklabels(df['name'], rotation=45, ha='right')  # Set labels to the actual names and rotate for readability
    
    # Adjust layout to ensure everything fits
    plt.tight_layout()

    return fig













x=1


