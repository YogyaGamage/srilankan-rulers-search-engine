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