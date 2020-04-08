import os
from pprint import pprint

from flask import Flask, render_template, jsonify, request
from elasticsearch import Elasticsearch
from bert_serving.client import BertClient
SEARCH_SIZE = 25
INDEX_NAME = os.environ['INDEX_NAME']
DEBUG = True

app = Flask(__name__)
app.config['ENV'] = 'development'
app.config['DEBUG'] = True
app.config['TESTING'] = True

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/status')
def status():
    bc = BertClient(ip='nlp-bert')
    return jsonify(bc.server_status)

@app.route('/search')
def analyzer():
    bc = BertClient(ip='nlp-bert', output_fmt='list')
    client = Elasticsearch('nlp-elasticsearch:9200')

    query = request.args.get('q')
    query_vector = bc.encode([query])[0]

    script_query = {
        "script_score": {
            "query": {"match_all": {}},
            "script": {
                "source": "cosineSimilarity(params.query_vector, doc['text_vector']) + 1.0",
                "params": {"query_vector": query_vector}
            }
        }
    }

    response = client.search(
        index=INDEX_NAME,
        body={
            "size": SEARCH_SIZE,
            "query": script_query,
            "_source": {"includes": ["title", "abstract", "authors","doi"]}
        }
    )

    print(query)

    return jsonify(response)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
