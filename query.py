import json
import pandas

class Query():

    def __init__(self, term1, term2):   
        self.term1 = term1
        self.term2 = term2
        self.query(self.term1, self.term2)

    def open_index(self):
        with open('dictonary.json') as f:
            dictonary = json.load(f)
        with open('postings_list.json') as f:
            postingslist = json.load(f)
        return dictonary, postingslist

    def open_data(self):
        with open('data.json') as f:
            data = json.load(f)
        return data

    def query(self, term1, term2):
        result_document_ids = []
        directory, postingslist = self.open_index()
        
        try:
            directory_t1 = directory[term1]
            len_postingslist_t1 = directory_t1[0]
            postingslist_t1 = postingslist[str(directory_t1[1])]
            iter_postingslist_t1 = iter(postingslist_t1)
        except KeyError:
            print(f"Key '{term1}' was not found in Dictonary")

        try:
            directory_t2 = directory[term2]
            len_postingslist_t2 = directory_t2[0]
            postingslist_t2 = postingslist[str(directory_t2[1])]
            iter_postingslist_t2 = iter(postingslist_t2)
        except KeyError:
            print(f"Key '{term1}' was not found in Dictonary")

        try:
            if len_postingslist_t1 > len_postingslist_t2:
                for document_id in postingslist_t2:
                    if document_id == next(iter_postingslist_t1):
                        result_document_ids.append(document_id)
                    if document_id > next(iter_postingslist_t1):
                        while document_id > next(iter_postingslist_t1):
                            next(iter_postingslist_t1)
                            if document_id == next(iter_postingslist_t1):
                                result_document_ids.append(document_id)
                                pass
                    if document_id < next(iter_postingslist_t1):
                        pass
            data = self.open_data()
            if result_document_ids:
                for result in result_document_ids:
                    print(f"Document ID: {result}")
                    print(f"Document Text: {data[str(result)]['news_text']}")
            else:
                print("No Documents were found!")
        except:
            pass

Query("weiß", "maße")

