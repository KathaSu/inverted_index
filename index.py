import pandas
import nltk
import re
import json

from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer

class Index():

    def __init__(self, documents):   
        self.documents = documents
        self.index(self.documents)

    def preprocessing(self, document):
        stemmer = PorterStemmer()
        clean_text = re.sub(r'[^\w\s]', '', document)
        token_list = word_tokenize(clean_text)
        stemmed_token_list = [stemmer.stem(token) for token in token_list]
        return stemmed_token_list

    def index(self, documents):
        dictonary = {}
        postings_list = {}
        pointerlist_id = 0
        
        documents = pandas.read_csv(documents, sep="\t")
        
        for document_id, document_text in zip(documents.id, documents.news_text):
            tokens = self.preprocessing(document_text)
            for token in tokens:
                if token not in dictonary:
                    dictonary.update({token : [1, pointerlist_id]})
                    postings_list.update({pointerlist_id: [document_id]})
                    pointerlist_id += 1
                elif token in dictonary:
                    if document_id not in postings_list[dictonary[token][1]]:
                        dictonary[token][0] += 1
                        postings_list[dictonary[token][1]].append(document_id)

        with open('dictonary.json', 'w+', encoding="utf-8") as outfile:
            json.dump(dictonary, outfile)
        with open('postings_list.json', 'w+', encoding="utf-8") as outfile:
            json.dump(postings_list, outfile)
        with open('data.json', 'w+', encoding="utf-8") as outfile:
            outfile.write(documents.to_json(orient="index"))

Index("postillon.csv")