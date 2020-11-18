# Import relevant packages.
import pandas
import nltk
import re
import json

from nltk.tokenize import word_tokenize
from nltk.stem.snowball import SnowballStemmer

# Create class Index.
class Index():

    # Initial function when class "Index" is called.
    def __init__(self, documents):
        # When calling the index class the index function is executed.
        self.index(documents)

    # Preprocess document.
    def preprocessing(self, document):
        # Assign the Snowball Stemmer to the "stemmer" variable. The stemmer 
        # reduces morpholigical endings.
        stemmer = SnowballStemmer("german")
        # Using regular expressions to exclude anything different from words 
        # and whitespaces in the document.
        clean_text = re.sub(r'[^\w\s]', '', document)
        # Tokenization of the cleaned document.
        token_list = word_tokenize(clean_text)
        # Stemming of the tokenized document.
        stemmed_token_list = [stemmer.stem(token) for token in token_list]
        return stemmed_token_list

    def index(self, documents):
        # Assign an empty dictionary to the variable "dictionary".
        dictionary = {}
        # Assign an empty dictionary to the variable "postings_list".
        postings_list = {}
        # Assign value 0 to the first calling of the "pointerlist_id" variable.
        pointerlist_id = 0
        
        # Read data using pandas. Use separation of tabs and assign it to the 
        # variable "documents".
        documents = pandas.read_csv(documents, sep="\t")
        
        # Create for-loop for document_id and news_text.
        for document_id, document_text in zip(documents.id, documents.news_text):
            # Assign the list we got from preprocessing to the variable "tokens".
            tokens = self.preprocessing(document_text)
            # Create for-loop for each token in the list.
            for token in tokens:
                # If statement to check if the token is in the dictionary.
                if token not in dictionary:
                    # Add token to the dictionary with the information that the
                    # length of the postings list is 1 and the current
                    # pointerlist_id.
                    dictionary.update({token: [1, pointerlist_id]})
                    # Add entry to postings_list that contains the pointerlist 
                    # id and the document id. Through the pointerlist id we can
                    # connect the dictionary with the postings list.
                    postings_list.update({pointerlist_id: [document_id]})
                    # Increase the pointerlist id by one.
                    pointerlist_id += 1
                elif token in dictionary:
                    # Check if a document id already is in the postings list.
                    if document_id not in postings_list[dictionary[token][1]]:
                        # Increase the length of the postingslist by one.
                        dictionary[token][0] += 1
                        # Add document id to the postings list.
                        postings_list[dictionary[token][1]].append(document_id)

        # Write dictionary, postings_list and documents as json to seperate files.
        with open('dictionary.json', 'w+', encoding="utf-8") as outfile:
            json.dump(dictionary, outfile)
        with open('postings_list.json', 'w+', encoding="utf-8") as outfile:
            json.dump(postings_list, outfile)
        with open('data.json', 'w+', encoding="utf-8") as outfile:
            outfile.write(documents.to_json(orient="index"))

# Call Index with argument of file name with the document.
Index("postillon.csv")