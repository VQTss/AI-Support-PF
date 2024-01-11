import pandas as pd
from collections import Counter
import re
from itertools import chain
from nltk.util import ngrams
from io import BytesIO


# Define a list of stop words
stop_words = set(["a", "about", "above", "after", "again", "against", "all", "am", "an", "and", "any", "are", "as", "at",
                  "be", "because", "been", "before", "being", "below", "between", "both", "but", "by", "could", "did",
                  "do", "does", "doing", "down", "during", "each", "few", "for", "from", "further", "had", "has", "have",
                  "having", "he", "her", "here", "hers", "herself", "him", "himself", "his", "how", "i", "if", "in",
                  "into", "is", "it", "its", "itself", "just", "me", "more", "most", "my", "myself", "no", "nor", "not",
                  "now", "of", "off", "on", "once", "only", "or", "other", "our", "ours", "ourselves", "out", "over",
                  "own", "s", "same", "she", "should", "so", "some", "such", "t", "than", "that", "the", "their",
                  "theirs", "them", "themselves", "then", "there", "these", "they", "this", "those", "through", "to",
                  "too", "under", "until", "up", "very", "was", "we", "were", "what", "when", "where", "which", "while",
                  "who", "whom", "why", "will", "with", "you", "your", "yours", "yourself", "yourselves",
                   'thanks', 'thank', 'thankyou', 'thankful', 'thx', 'thnx', 'appreciate',
                'grateful', 'gratitude', 'thanking', 'ty', 'tysm', 'thankies', 'thks'
    ])



# Function to clean text and extract phrases
def clean_and_extract_phrases(text, stop_words):
    if not isinstance(text, str):
        return []
    text = re.sub(r'[^A-Za-z\s]', '', text)
    text = text.lower()
    words = text.split()
    filtered_words = [word for word in words if word not in stop_words]
    phrases = list(chain.from_iterable(ngrams(filtered_words, n) for n in range(2, 5)))
    return [" ".join(phrase) for phrase in phrases]

# Function to count phrase frequencies and exclude specified phrases
def count_phrase_frequencies_excluding(column_data, stop_words, exclude_phrases):
    phrase_counts = Counter()
    for item in column_data:
        phrases = clean_and_extract_phrases(item, stop_words)
        phrases = [phrase for phrase in phrases if phrase not in exclude_phrases]
        phrase_counts.update(phrases)
    return phrase_counts

# List of phrases to exclude, provided by the user
exclude_phrases = [
    "assistance provided", "provided support", "support team", "team excellent",
    "excellent user", "user appreciates", "assistance provided support",
    "provided support team", "support team excellent", "team excellent user",
    "excellent user appreciates", "assistance provided support team",
    "provided support team excellent", "support team excellent user",
    "team excellent user appreciates", "thats says", "says im", "im eligible",
    "eligible leave", "leave review", "review ok", "ok doneeee", "doneeee thank",
    "thank youuu", "youuu hi", "hi gotta", "gotta step", "step away", "away anyway",
    "anyway yyessss", "yyessss thanks", "thats says im", "says im eligible",
    "im eligible leave", "eligible leave review", "leave review ok", "review ok doneeee",
    "ok doneeee thank", "doneeee thank youuu", "thank youuu hi", "youuu hi gotta",
    "hi gotta step", "gotta step away", "step away anyway", "away anyway yyessss",
    "anyway yyessss thanks", "thats says im eligible", "says im eligible leave",
    "im eligible leave review", "eligible leave review ok", "leave review ok doneeee",
    "review ok doneeee thank", "ok doneeee thank youuu", "doneeee thank youuu hi",
    "thank youuu hi gotta", "youuu hi gotta step", "hi gotta step away",
    "gotta step away anyway", "step away anyway yyessss", "away anyway yyessss thanks"
]

def analysis_counter(file_content: bytes) -> BytesIO:
    # Load the Excel file
    new_data = pd.read_excel(BytesIO(file_content))
    output = BytesIO()
    # Counting phrase frequencies in each column and excluding specified phrases
    bug_phrase_counts_excluding = count_phrase_frequencies_excluding(new_data['Bug'], stop_words, exclude_phrases)
    feature_phrase_counts_excluding = count_phrase_frequencies_excluding(new_data['Feature'], stop_words, exclude_phrases)
    ux_ui_phrase_counts_excluding = count_phrase_frequencies_excluding(new_data['UX/UI'], stop_words, exclude_phrases)

    # Combining phrase counts
    combined_phrase_counts_excluding = bug_phrase_counts_excluding + feature_phrase_counts_excluding + ux_ui_phrase_counts_excluding

    # Creating a new dataframe for the output
    output_data_phrases_excluding = pd.DataFrame(columns=["STT", "Phrase", "Frequency", "URL Tickets"])

    # Function to find tickets containing a specific keyword or phrase
    def find_tickets_with_keyword(keyword, data_columns):
        ticket_urls = []
        for index, row in new_data.iterrows():
            if any(keyword in clean_and_extract_phrases(text, stop_words) for text in row[data_columns]):
                ticket_urls.append(row['Ticket URL'])
        return ticket_urls

    # Populating the dataframe with the updated phrase counts
    for index, (phrase, frequency) in enumerate(combined_phrase_counts_excluding.items()):
        ticket_urls = find_tickets_with_keyword(phrase, ['Bug', 'Feature', 'UX/UI'])
        new_row = pd.DataFrame({
            "STT": [index + 1],
            "Phrase": [phrase],
            "Frequency": [frequency],
            "URL Tickets": [", ".join(ticket_urls)]
        })
        output_data_phrases_excluding = pd.concat([output_data_phrases_excluding, new_row], ignore_index=True)
    output_data_phrases_excluding.to_excel(output, index=False)
    output.seek(0)
    return output




# Saving the output to an Excel file
# output_file_path_phrases_excluding = './result/analyzed_phrases_excluding.xlsx'
# output_data_phrases_excluding.to_excel(output_file_path_phrases_excluding, index=False)
