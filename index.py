import pandas
import os
import nltk
import re

from nltk.tokenize import word_tokenize


"""
Example for Dictonary Entry
    {
        term: [lenght_postingslist, pointer_postingslist]
    }
"""
"""
Example for Postings Lists
    {
        pointer: list
    }
"""
def preprocessing(document):
    clean_text = re.sub(r'[^\w\s]', '', document)
    token_list = word_tokenize(clean_text)
    return token_list

def index(documents):
    dictonary = {}
    postings_list = {}
    
    documents = pandas.read_csv(documents, sep="\t")
    
    pointerlist = 0

    for id,document in zip(documents.id, documents.news_text):
        tokens = preprocessing(document)
        for token in tokens:
            if token not in dictonary:
                entry = {token : [1, pointerlist]}
                dictonary.update(entry)
    
    
    print(dictonary)
                

index('postillon.csv')