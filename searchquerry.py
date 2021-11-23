from elasticsearch import Elasticsearch
from flask import *
from elasticsearch import Elasticsearch
from sinling import SinhalaTokenizer
from sinling import word_splitter
import re

from search import basic_search, simpleMatchQuery,multiComplexMatchQuery,aggMatchQuery
# from rules import process
tokenizer = SinhalaTokenizer()

es = Elasticsearch()
INDEX = 'srilankanrulers'
client = Elasticsearch(HOST="http://localhost",PORT=9200)

ruler_identifiers = ["ගේ","ගෙ"]
predecessor_identifiers = ["පසු","පස්සේ","පසුව"]
successor_identifiers = ["පෙර","කලින්"]
period_identifiers = ["කාළයේ","අවුරුද්දේ","වසරේ"]
capital_identifiers = ["යුගයේ","රාජධානියේ"]
house_identifiers = ["රාජවංශයේ","වංශයේ"]
default = {"ruler":1.5,"predecessor":1.0,"successor":1.0,"period":1.0,"capital":1.0,"house":1.0}
period_extra = ["නව","අවසාන"]
agg_extra = ["ගණන","කීයද","ප්‍රමාණය","කීදෙනාද"]
val_extra = ["දෙනා","ක්", "දෙනෙක්"]

def search(query):
    ## result = client. (index=INDEX,body=standard_analyzer(query))
    ## keywords = result ['tokens']['token']
    ## print(keywords)

    ## query_body= process(query)
    processed_query = preprocessQuery(query)
    #print(processed_query)
    #query_body = basic_search(query)
    #print('Making Basic Search ',query_body)
    res = client.search(index=INDEX, body=processed_query)
    #print(res)
    return res
    
def preprocessQuery(query):
        tokens = tokenizer.tokenize(query)
        boosting_fields, boosting_data, new_query, intExist = matchIdentifyers(tokens, query)
        print(boosting_fields)
        if(len(boosting_data)!=0 or len(boosting_fields)!=0):
            boosting_string = fieldBoosting(boosting_fields, boosting_data)
            if("num" in boosting_fields):
                return aggMatchQuery(new_query, boosting_string)
            else:
                if("range" in boosting_fields):
                    if ("year" in boosting_fields):
                        return multiComplexMatchQuery(new_query, boosting_string,intExist,True)
                    return multiComplexMatchQuery(new_query, boosting_string,intExist)
                return multiComplexMatchQuery(new_query, boosting_string)
        else:
            return simpleMatchQuery(new_query)
 

    
def matchIdentifyers(tokens,query):
    boosting_fields = []
    boosting_data = {}
    print(tokens)
    intExist=10
    for token in tokens:
        results = word_splitter.split(token)
        print(results, token)
        if token.isdigit():
            intExist=token
            
        if(token in val_extra or results['affix'] in val_extra or results['base'] in val_extra):
            boosting_fields.append("range")
            print(token)
            print(intExist,"inte")
            query = removeParts(query, [token])
        if(token in period_extra or results['affix'] in period_extra or results['base'] in period_extra):
            boosting_fields.append("year")
            print(token)
            query = removeParts(query, [token])
        if(token in agg_extra or results['affix'] in agg_extra or results['base'] in agg_extra):
            boosting_fields.append("num")
            print(token)
            query = removeParts(query, [token])
        if(token in ruler_identifiers or results['affix'] in ruler_identifiers or results['base'] in ruler_identifiers):
            boosting_fields.append("name")
            boosting_data['name'] = 2.0
            print(token)
        if(token in predecessor_identifiers or results['affix'] in predecessor_identifiers or results['base'] in predecessor_identifiers):
            boosting_fields.append("predecessor")
            boosting_data['predecessor'] = 2.0
            query = removeParts(query, [token])
        if(token in successor_identifiers or results['affix'] in successor_identifiers or results['base'] in successor_identifiers):
            boosting_fields.append("successor")
            boosting_data['successor'] = 2.0
            query = removeParts(query, [token])
        if(token in period_identifiers or results['affix'] in period_identifiers or results['base'] in period_identifiers):
            boosting_fields.append("period")
            boosting_data['period'] = 2.0
            query = removeParts(query, [token])
        if(token in house_identifiers or results['affix'] in house_identifiers or results['base'] in house_identifiers):
            boosting_fields.append("house")
            boosting_data['house'] = 2.0
            query = removeParts(query, [token])
        if(token in capital_identifiers or results['affix'] in capital_identifiers or results['base'] in capital_identifiers):
            boosting_fields.append("capital")
            boosting_data['capital'] = 2.0
            query = removeParts(query, [token])
        
    return list(set(boosting_fields)), boosting_data, query, intExist


        

def removeParts(query, garbage_tokens):
    for g_val in garbage_tokens:
        query = query.replace(g_val," ")
    return query

def fieldBoosting( boosting_fields, boosting_data):
    boosting_string = []
    for field in boosting_fields:
        try:
            val = boosting_data[field]
            boosting_string.append("{0}^{1}".format(field, val))
        except:
            pass
    return boosting_string