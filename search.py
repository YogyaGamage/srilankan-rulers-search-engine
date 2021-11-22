import json


def standard_analyzer(query):
    q = {
        "analyzer": "rule_analyzer",
        "text": query
    }
    return q


def basic_search(query):
    q = {
        "query": {
            "query_string": {
                "query": query,
                "analyzer": "rule_analyzer"
            }
        }
    }
    return q


def simpleMatchQuery(query,size=10):
    print("default")
    if(query.strip()==""):
        body =  {
            "size": size,
            "query": {
                "match_all": {
                    
                }
            }
        }
        
    else:
        body =  {
            "size": size,
            "query": {
                "multi_match": {
                    "query": query,
                    "analyzer": "rule_analyzer"
                }
            }
        }
    return body
    

def multiComplexMatchQuery(query, boosting_string,size=10):
    print("not d")

    body =  {
        "size": size,
        "query": {
            "multi_match": {
                "query": query,
                "analyzer": "rule_analyzer",
                "fields": boosting_string
            }
        }
    }
    return body

def aggMatchQuery(query, boosting_string):
    print("not d")

    body =  {
        "query": {
            "match": {
                "capital": query
            }
        },
        "aggs": {
                "capitals" : {
                    "terms" : { "field" : "capital.keyword" } 
                }
            }
    }

    return body

