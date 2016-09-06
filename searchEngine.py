from elasticsearch import Elasticsearch, RequestsHttpConnection, serializer, compat, exceptions
from elasticsearch_dsl import Search, Q
from urllib2 import urlopen
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
    text = urlopen(url).read()
    doc_id = randint(1,10**20)
    filepath = os.getcwd() + "/static/" + str(doc_id) + ".htm"
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
        s = Search(using=es, index=INDEX).query(q)
        response = s.execute()
        for hit in response:
            print(hit.meta.score, hit.urlRes)
    except exceptions.NotFoundError:
        print "Index named "+ INDEX + " doesn't exist!"