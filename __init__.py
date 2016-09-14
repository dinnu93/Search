from flask import *
from searchEngine import *
import json
import cgi

app = Flask(__name__)
HOST = '139.59.26.210'

@app.route("/search")
def search():
    query = request.args.get('q')
    result_list = map(lambda x :{'textResults': map(lambda s : s.encode('utf-8').decode('unicode_escape').encode('ascii','ignore') , list(x[1])),
                                  'cacheLink' : 'http://' + HOST + url_for('static', filename = str(x[2])+'.html'),
                                  'urlResult' : x[0]} , searchQuery(query))
    return Response(json.dumps(result_list, indent=4), mimetype='application/json')

@app.route("/url", methods=['POST'])
def url():
    if request.method == 'POST':
        content = request.get_json(silent=True)
        if 'url' in content:
            url = content['url']
            if postUrl(url):
                return Response(json.dumps({'url': url, 'indexed': True}, indent=4), mimetype='application/json')
            else:
                return Response(json.dumps({'url': url,'indexed' : False,
                                            'error' : 'Serialization error!'}, indent=4), mimetype='application/json') 
        else:
            return Response(json.dumps({'error': 'Not a valid request body!'}, indent=4), mimetype='application/json')

        
if __name__=="__main__":
    app.run()
    
