import json

# Create class Query.
class Query():

    # When class Query is called the following is executed.
    def __init__(self, term1, term2):
        # Call function query for term1 and term2.
        self.query(term1, term2)

    # Read dictionary and postingslist from json file.
    def open_index(self):
        with open('./dictonary.json') as f:
            dictonary = json.load(f)
        with open('./postings_list.json') as f:
            postingslist = json.load(f)
        return dictonary, postingslist

    # Read documents from json file.
    def open_data(self):
        with open('./data.json') as f:
            data = json.load(f)
        return data

    def query(self, term1, term2):
        # Assign emtpy list to variable "result_document_ids".
        result_document_ids = []
        # Create variables that contain the dictionary and postingslist.
        dictionary, postingslist = self.open_index()
        
        try:
            # Look for term1 in dictionary.
            dictionary_t1 = dictionary[term1]
            # Look for length of the postingslist of term1.
            len_postingslist_t1 = dictionary_t1[0]
            # Call postingslist of term1.
            postingslist_t1 = postingslist[str(dictionary_t1[1])]
            # Call iteration function for postingslist of term1.
            iter_postingslist_t1 = iter(postingslist_t1)
        # If the previous block creates an key error, the next part will be printed. 
        except KeyError:
            print(f"Results for query {term1} AND {term2}")
            print(f"Key '{term1}' was not found in Dictonary")
            print("--------")

        try:
            # Looking up the relevant information for term2 in dictionary. 
            # Compare the comments from the code above
            dictionary_t2 = dictionary[term2]
            len_postingslist_t2 = dictionary_t2[0]
            postingslist_t2 = postingslist[str(dictionary_t2[1])]
            iter_postingslist_t2 = iter(postingslist_t2)
        except KeyError:
            print(f"Results for query {term1} AND {term2}")
            print(f"Key '{term2}' was not found in Dictonary")
            print("--------")
        
        # Check if both variable exist.
        try:
            dictionary_t1
            dictionary_t2
        # if the variables do not exist the else statement will be ignored. 
        # No error message is printed out, since one has been printed with the
        # previous code block.
        except UnboundLocalError:
            pass
        # if the variables are available the rest of the code will be executed
        else:
            # Check if the length of the second postingslist is longer or the 
            # same as the first.
            if len_postingslist_t1 >= len_postingslist_t2:
                # Create for-loop for the document ids.
                for document_id in postingslist_t2:
                    try:
                        # Check if document id from postingslist2 equals document id 
                        # of postingslist1 at the current position.
                        if document_id == next(iter_postingslist_t1):
                            # If statement is correct, document is added to list of
                            # results.
                            result_document_ids.append(document_id)
                    # If preceeding block creates StopIteration error (which can be
                    # caused if there is no more id left in the longer list), this
                    # error will be ignored.
                    except StopIteration:
                        pass
                    try:
                        # Check if document id from postingslist 2 is higher than the
                        # document id of postingslist 2 at the current position.
                        if document_id > next(iter_postingslist_t1):
                            # As long as the document id for postingslist 2 is higher
                            # than the document id at the current position the
                            # following code will be executed.
                            while document_id > next(iter_postingslist_t1):
                                # Call the next position in the iteratior of
                                # postingslist 1.
                                next(iter_postingslist_t1)
                                # Check if the document id of postingslist2 equals
                                # the new document id of postingslist1.
                                if document_id == next(iter_postingslist_t1):
                                    # If statement is correct, document is added
                                    # to list of results.
                                    result_document_ids.append(document_id)
                                    # Then break out of the while loop.
                                    break
                    # If preceeding block creates StopIteration error (which can
                    # be caused if there is no more id left in the longer list),
                    # this error will be ignored.
                    except StopIteration:
                        pass
                    try:
                        # Check if document id from postingslist 2 is lower than
                        # the document id of postingslist 1 at the current position.
                        if document_id < next(iter_postingslist_t1):
                            # The for-loop will start again.
                            pass
                    # If preceeding block creates StopIteration error (which can
                    # be caused if there is no more id left in the longer list),
                    # this error will be ignored.
                    except StopIteration:
                        pass
            # Check if length of the postingslist1 is greater than the length of
            # postingslist2. The code below is similar to the code above, just
            # switched, check comments above.
            elif len_postingslist_t1 < len_postingslist_t2:
                for document_id in postingslist_t1:
                    try:
                        if document_id == next(iter_postingslist_t2):
                            result_document_ids.append(document_id)
                    except StopIteration:
                        pass
                    try:
                        if document_id > next(iter_postingslist_t2):
                            while document_id > next(iter_postingslist_t2):
                                next(iter_postingslist_t2)
                                if document_id == next(iter_postingslist_t2):
                                    result_document_ids.append(document_id)
                                    break
                    except StopIteration:
                        pass
                    try:
                        if document_id < next(iter_postingslist_t2):
                            pass
                    except StopIteration:
                        pass

            # If we got results for our query, the following code will be executed.
            if result_document_ids:
                # To print out the document text in the result the original documents
                # will be opened.
                data = self.open_data()
                # The search query and resulting document ids will be printed out.
                print("Results for query {} AND {}: Document IDs {}"
                    .format(term1, term2, ', '.join([str(result) for result in result_document_ids])))
                # For every document the id + the document text will be printed out.    
                for result in result_document_ids:
                    print(f"Document ID: {result}")
                    print(f"Document Text: {data[str(result)]['news_text']}")
                print("--------")
            # This will be printed if there were no documents found for the query.
            else:
                print(f"Results for query {term1} AND {term2}")
                print("No Documents were found!")
                print("--------")

# Call Query class with different arguments.
Query("weiß", "maße")
Query("weiß", "masse")
Query("weiss", "maße")
Query("weiss", "masse")
Query("lieb", "dieser")

