from elasticsearch import Elasticsearch, RequestsHttpConnection, serializer, compat, exceptions
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

def postUrl(url):
    text = urlopen(url).read()
    doc_id = randint(1,10**20)
    filepath = os.getcwd() + "/cache/" + str(doc_id) + ".htm"
    es.index(index="url", doc_type="urlText", id = doc_id, body = {'urlRes' : url,'textRes' : text})
    f = open(filepath, "w")
    f.write(text)
    f.close()
    
def searchQuery(query):
    pass
