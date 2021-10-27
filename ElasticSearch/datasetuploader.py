from elasticsearch import Elasticsearch, helpers
from elasticsearch_dsl import Index
import json, re
import codecs
import unicodedata
# import queries

client = Elasticsearch(HOST="http://localhost", PORT=9200)
def read_all_data():
    with open('D:/Aca Sem 07/Data Mining/IR project/sl_rulers - Sheet1.json', 'r', encoding='utf-8-sig') as f:
        sl_rulers = json.loads(
                          f.read())
        #print (sl_rulers)
        return sl_rulers

def genData(ruler_array):
    for ruler in ruler_array:
        name = ruler.get("නම", None)
        period = ruler.get("රාජ්‍ය සමය",None)
        marriages = ruler.get("විවාහයන්", None)
        death = ruler.get("මරණය", None)
        house = ruler.get("රාජවංශය/පක්ෂය", None)
        capital = ruler.get("රාජධානිය/අගනගරය", None)
        predecessor = ruler.get("පූර්වප්‍රාප්තිකයා", None)
        successor = ruler.get("අනුප්‍රාප්තිකයා", None)
        details = ruler.get("විස්තර",None)

        yield {
            "_index": "srilankanrulers",
            "_source": {
                "නම": name,
                "රාජ්‍ය සමය": period,
                "විවාහයන්": marriages,
                "මරණය": death,
                "රාජවංශය/පක්ෂය": house,
                "රාජධානිය/අගනගරය": capital,
                "පූර්වප්‍රාප්තිකයා": predecessor,
                "අනුප්‍රාප්තිකයා": successor,
                "විස්තර": details
            },
        }

all_rulers = read_all_data()
helpers.bulk(client,genData(all_rulers))