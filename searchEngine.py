from elasticsearch import Elasticsearch, RequestsHttpConnection, serializer, compat, exceptions
from elasticsearch_dsl import Search, Q
from clean import htmlToText
import json
import os
from random import randint

class JSONSerializerPython2(serializer.JSONSerializer):
    def dumps(self, data):
        if isinstance(data, compat.string_types):
            return data
        try:
            return json.dumps(data, default=self.default, ensure_ascii=True)
        except (ValueError, TypeError) as e:
            raise exceptions.SerializationError(data, e)

es = Elasticsearch(serializer=JSONSerializerPython2())

INDEX = "url"
DOC_TYPE = "urlText"

def postUrl(url):
    text = htmlToText(url)
    doc_id = randint(1,10**20)
    filepath = "/var/www/Search/Search/static/" + str(doc_id) + ".html"
    try:
        es.index(index=INDEX, doc_type=DOC_TYPE, id = doc_id, body = {'urlRes' : url,'textRes' : text})
        f = open(filepath, "w")
        f.write(text)
        f.close()
        return True
    except exceptions.SerializationError:
        return False

    
def searchQuery(queryText):
    try:
        es.indices.refresh(index=INDEX)
        q = Q("match", textRes=queryText) | Q("prefix", textRes=queryText)
        s = Search(using=es, index=INDEX).query(q).highlight('textRes',pre_tags=[""],post_tags=[""],fragment_size=500)
        response = s.execute()
        return (map(lambda hit: (hit.urlRes,hit.meta.highlight.textRes,hit.meta.id),response))
    except exceptions.NotFoundError:
        return [] 
