from flask import *
from elasticsearch import Elasticsearch
from sinling import SinhalaTokenizer
from sinling import word_splitter
import re

tokenizer = SinhalaTokenizer()

es = Elasticsearch()
app = Flask(__name__)


ruler = ["ගේ","ගෙ"]
predecessor = ["පසු","පස්සේ","පසුව"]
successor = ["පෙර","කලින්"]
period = ["යුගයේ","කාළයේ"]
default = {"ruler":1.5,"predecessor":1.0,"successor":1.0,"period":1.0,"details":1.5}
period_extra = ["නව","පැරණි"]

class QueryPreProcess:

    def __init__(self):
        print("-------------started--------------")
    
    @classmethod
    def preprocessQuery(self, query):
        tokens = tokenizer.tokenize(query)
        boosting_fields, boosting_data, new_query = self.identifyContext(tokens, query)
        print(boosting_fields)
        if(len(boosting_data)!=0 or len(boosting_fields)!=0):
            boosting_string = self.generateBoosting(boosting_fields, boosting_data)
            if("rate" in boosting_fields):
                return self.multiMatchBoostingQuery(new_query, boosting_string, True)
            else:
                return self.multiMatchBoostingQuery(new_query, boosting_string)
        else:
            return self.multiMatchDefaultQuery(new_query)
 

    @classmethod
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

    @classmethod
    def replaceUnwantedData(self, query, garbage_tokens):
        for g_val in garbage_tokens:
            query = query.replace(g_val," ")
        return query

    @classmethod
    def generateBoosting(self, boosting_fields, boosting_data):
        boosting_string = []
        for field in boosting_fields:
            try:
                val = boosting_data[field]
                boosting_string.append("{0}^{1}".format(field, val))
            except:
                pass
        return boosting_string

    @classmethod
    def multiMatchDefaultQuery(sef,query):
        if(query.strip()==""):
            body =  {
                "query": {
                    "match_all": {
                       
                    }
                },
                "sort": {
                    "rating":{
                         "order":"desc"
                        }
                    }
                }
            
        else:
            body =  {
                "query": {
                    "multi_match": {
                        "query": query
                    }
                },
                "aggs" : {
                    "genres" : {
                        "terms" : { "field" : "genre.keyword" } 
                    }
                }
            }
        return body
    

    @classmethod
    def multiMatchBoostingQuery(sef, query, boosting_string, sortByRating=False):
        print("00")

        body =  {
            "query": {
                "multi_match": {
                    "query": query,
                    "fields": boosting_string
                }
            },
            "aggs" : {
                    "genres" : {
                        "terms" : { "field" : "genre.keyword" } 
                    }
                }
        }

        if(sortByRating):
            body["sort"] = {
                    "rating":{
                         "order":"desc"
                        }
                    }
        return body
    

@app.route('/')
def hello_world():
    return render_template('index.html')  

@app.route('/search', methods=['GET'])
def search_songs():
    query  = request.args.get("q")
    from_  = request.args.get("from")
    
    qp = QueryPreProcess()

    pharseQuery = re.search("[\"\']*[\"\']", query)
    
    if pharseQuery:
        body = {
            "from" : from_,
            "query": {
                "match_phrase":{
                    "lyrics": query
                }
            }
        }
    else:
        processed_query = qp.preprocessQuery(query)
        print(processed_query)
        processed_query['from']=from_
        body = processed_query

    res = es.search(index="srilankanrulers", body=body)

    return jsonify(res)

if __name__ == '__main__':
    app.run(debug=True)
