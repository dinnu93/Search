from flask import Flask, jsonify, request
app = Flask(__name__)

@app.route("/search")
def hello():
    return jsonify({'working' : request.args.get('q')})

if __name__=="__main__":
    app.run(debug=True)
    
