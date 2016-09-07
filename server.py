from flask import Flask, jsonify, request
from searchEngine import *
import json
import cgi

app = Flask(__name__)
HOST = '0.0.0.0'
PORT = 5000

@app.route("/search")
def search():
    query = request.args.get('q')
    result_list = map(lambda x : {'textResult' : cgi.escape(x[1]),
                                  'cacheLink' : 'http://' + HOST + ':' + str(PORT) + '/static/'+str(x[2])+'.htm',
                                  'urlResult' : x[0]} , searchQuery(query))
    return json.dumps(result_list)

@app.route("/url", methods=['POST'])
def url():
    if request.method == 'POST':
        content = request.get_json(silent=True)
        if 'url' in content:
            url = content['url']
            if postUrl(url):
                return json.dumps({'url': url, 'indexed': True})
            else:
                return json.dumps({'url': url,'indexed' : False, 'error' : 'Serialization error!'})
        else:
            return json.dumps({'error': 'Not a valid request body!'})
        
if __name__=="__main__":
    app.run(host=HOST, port=PORT, debug=True)
    
