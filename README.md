# Search Engine for Sri Lankan Rulers

## About

A Sinhala search engine for rulers who ruled Sri Lanka from the beginning of the Sri Lankan monarchy to the current president.

## Features

 - Search by the name of ruler
    - විජය රජතුමා 
 - Search by the period
    - අනුරාධපුර යුගයේ රජවරු
 - Search by predecessor
    - උපතිස්ස රජට පෙර සිටි රජු
 - Search by successor
    - උපතිස්ස රජට පසු සිටි රජු
 - Search by house
    - මෝරිය රාජවංශයේ රජවරු
 - Search by range queries
    - පොළොන්නරු රාජධානියේ අවසාන රජවරු 05 දෙනා
 - Search with synonyms
    - බ්‍රිතාන්‍යය රජවරු, එංගලන්ත රජවරු
 - Search by aggregated queries
    - අනුරාධපුර යුගයේ රජවරු ගණන කීයද 

 
## How to Run

 - Clone or download the repository
 - Run ElasticSearch [How to set up Elastic Search](#setting-up-elasticsearch) 
 - Open a terminal on the project root directory
 - Run app.py
 - Visit [webpage](http://localhost:5000/search) in your browser

## How to Search

After running the application you will see the web interface of the search engine. Type your querry and press enter and select the search button to explore the heads of state of Sri Lanka.


------------


## Setting up Elasticsearch

Download [Elasticsearch](https://www.elastic.co/downloads/elasticsearch) if you haven't already. After extracting the downloaded zip file, browse into "elasticsearch-x.x.0/bin" folder and run ./elasticsearch. This will start elasticsearch on the default port 9200. 

## Data

Details about rulers were scraped from [Wikipedia](https://si.wikipedia.org/) website. The data was manually curated from several wikipedia pages. After carrying out further preprocessing and cleaning steps to remove redundancies and inconsistencies the final dataset is obtained. The dataset consists of following data fields.

- Name (නම)
- Period (රාජ්‍ය සමය)
- Marriages (විවාහයන්)
- Death (මරණය)
- House (රාජවංශය/පක්ෂය)
- Capital (රාජධානිය/අගනගරය)
- Predecessor (පූර්වප්‍රාප්තිකයා)
- Successor (අනුප්‍රාප්තිකයා)
- Details (විස්තර)

The dataset can be found inside the ElasticSearch folder. You can upload the data to elasticsearch by running the datauploader.py file in the same folder. 

## Indexing Process

You can create the index and add the custom analyzers and the mappings as follows. The files stopwords.txt, stems.txt, synonyms.txt can be found inside the ElasticSearch folder. They were created based on two corpuses, [stopwords](https://github.com/nlpcuom/Sinhala-Stopword-list) and [sinhala-stemmer](https://raw.githubusercontent.com/shilpasayura/sinhala-nltk/master/sinhala-stemmer/)stem_dictionary.txt.

```
PUT srilankanrulers
{
  "settings": {
    "analysis": {
      "analyzer": {
        "rule_analyzer": {
          "tokenizer": "standard",
          "filter": [ "custom_stop", "custom_stem", "custom_syn" ]
        }
      },
      "filter": {
        "custom_stop": {
          "type": "stop",
          "stopwords_path": "analyze/stopwords.txt"
        },
        "custom_stem": {
          "type": "stemmer_override",
          "rules_path": "analyze/stems.txt"
        },
        "custom_syn": {
          "type": "synonym",
          "synonyms_path": "analyze/synonyms.txt"
        }
      }
    }
  }
}

PUT srilankanrulers/_mapping

{
  "properties": {
    "death": { 
      "type":     "text",
      "fielddata": true
    },
    "capitals": { 
      "type":     "text",
      "fielddata": true
    }
  }
}

```
## Indexing and Querrying Techniques

- **Tokenization**

Standard tokenizer is used during for the tokenizaton process.

- **Stop word filtering and stemming**

- **Rule based classification**

A rule based classification is used to classify the search queries into different categories of searches. The rules are applied after splitting the search query into tokens and identifying the context. The Sinling Sinhala tokenizer is used for the query tokenization process. 

- **Boosting**

Boosting is used as a query optimization technique. Each data field of a search is boosted with a predefined value based on the keywords in the search phrase.

- **Facet and Range queries**

Range queries are also supported such as last kings in Anuradhapura. Also, facet queries are supported such as the number of kings in each era for the search results.


- **Multi-match queries**
- **Boolean queries**
- **Sorting**