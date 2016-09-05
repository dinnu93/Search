from flask import Flask, jsonify, request
import json
app = Flask(__name__)

@app.route("/search")
def search():
    query = request.args.get('q')
    return json.dumps([{'urlResult' : 'http://google.com/',
                        'textResult' : query }])

@app.route("/url", methods=['POST'])
def url():
    if request.method == 'POST':
        content = request.get_json(silent=True)
        if 'url' in content:
            url = content['url']
            return json.dumps({'url': url, 'indexed': True})
        else:
            return json.dumps({'error': 'Not a valid request body!'})
        
if __name__=="__main__":
    app.run(debug=True)
    
