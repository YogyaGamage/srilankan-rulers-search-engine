from elasticsearch import Elasticsearch
from flask import *
from elasticsearch import Elasticsearch
from sinling import SinhalaTokenizer
from sinling import word_splitter
import re

from search import basic_search, standard_analyzer
# from rules import process
tokenizer = SinhalaTokenizer()

es = Elasticsearch()
INDEX = 'srilankanrulers'
client = Elasticsearch(HOST="http://localhost",PORT=9200)

ruler = ["ගේ","ගෙ"]
predecessor = ["පසු","පස්සේ","පසුව"]
successor = ["පෙර","කලින්"]
period = ["යුගයේ","කාළයේ"]
default = {"ruler":1.5,"predecessor":1.0,"successor":1.0,"period":1.0,"details":1.5}
period_extra = ["නව","පැරණි"]

def search(query):
    ## result = client. (index=INDEX,body=standard_analyzer(query))
    ## keywords = result ['tokens']['token']
    ## print(keywords)

    ## query_body= process(query)
    processed_query = preprocessQuery(query)
    print(processed_query)
    #query_body = basic_search(query)
    #print('Making Basic Search ')
    res = client.search(index=INDEX, body=processed_query)
    return res
    
def preprocessQuery(query):
        tokens = tokenizer.tokenize(query)
        boosting_fields, boosting_data, new_query = identifyContext(tokens, query)
        print(boosting_fields)
        if(len(boosting_data)!=0 or len(boosting_fields)!=0):
            boosting_string = generateBoosting(boosting_fields, boosting_data)
            if("rate" in boosting_fields):
                return multiMatchBoostingQuery(new_query, boosting_string, True)
            else:
                return multiMatchBoostingQuery(new_query, boosting_string)
        else:
            return multiMatchDefaultQuery(new_query)
 

    
def identifyContext(self, tokens,query):
    boosting_fields = []
    boosting_data = {}
    print(tokens)
    for token in tokens:
        results = word_splitter.split(token)
        #Split the token into affix and the base 
        if(results['affix']=="ගේ"):
            query = query.replace(token, results['base'])
        if("ගීත" in token):
            query = query.replace("ගීත", " ")
        #print(results, token)
        if(token in rating_identifiers or results['affix'] in rating_identifiers or results['base'] in rating_identifiers):
            boosting_fields.append("rate")
            print(token)
            query = self.replaceUnwantedData(query, [token, results['base'], results['affix']])
        if(token in artist_identifiers or results['affix'] in artist_identifiers or results['base'] in artist_identifiers):
            boosting_fields.append("artist")
            boosting_data['artist'] = 2.0
            query = self.replaceUnwantedData(query, [ results['affix']])
        if(token in writer_identifiers or results['affix'] in writer_identifiers or results['base'] in writer_identifiers):
            boosting_fields.append("writer")
            boosting_data['writer'] = 2.0
            query = self.replaceUnwantedData(query, [token, results['base'], results['affix']])
        if(token in genre_boosters or results['affix'] in genre_boosters or results['base'] in genre_boosters):
            boosting_fields.append("genre")
            boosting_data['genre'] = 3.0
        #append music as well.
        
    return list(set(boosting_fields)), boosting_data, query

def replaceUnwantedData(self, query, garbage_tokens):
    for g_val in garbage_tokens:
        query = query.replace(g_val," ")
    return query

def generateBoosting(self, boosting_fields, boosting_data):
    boosting_string = []
    for field in boosting_fields:
        try:
            val = boosting_data[field]
            boosting_string.append("{0}^{1}".format(field, val))
        except:
            pass
    return boosting_string