from flask import Flask, jsonify, request
from search import postUrl
import json

app = Flask(__name__)
HOST = '127.0.0.1'
PORT = 5000

@app.route("/search")
def search():
    query = request.args.get('q')
    return json.dumps([{'urlResult' : 'http://google.com/',
                        'textResult' : query,
                        'cacheLink' : 'http://' + HOST + ':' + str(PORT) + '/static/temp.htm'}])

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
    
