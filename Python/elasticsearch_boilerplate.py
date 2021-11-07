from datetime import datetime
from elasticsearch import Elasticsearch, helpers

PORT=9200
ENDPOINT=f"http://localhost:{PORT}"
index_name = "my_index"


def get_instance(ENDPOINT):
    return Elasticsearch(ENDPOINT)

def create_instance():
    es = get_instance()

    # add `indexed_at` field
    pipeline_id = "add_ts_pipeline"
    pipeline_body = {
        "description": "Creates a timestamp when a document is initially indexed",
        "processors": [{
            "set": {"field": "_source.indexed_at", "value": "{{_ingest.timestamp}}"}
            }]
        }
    es.ingest.put_pipeline(id=pipeline_id, body=pipeline_body)
    
    request_body = {
        "settings": {
            "default_pipeline": pipeline_id,
            }, "mappings": {
                "properties": {
                    "data": {"type": "text"},
                    "uri": {"type": "text"},
                    },
                }
        }
    response = es.indices.create(index=index_name, body=request_body, ignore=400)
    if 'acknowledged' in response:
        if response['acknowledged'] == True:
            print("INDEX MAPPING SUCCESS FOR INDEX:", response['index'])
    return es

def get_insert_dict(filepath):
    with open(filepath) as f:
        data = f.read()
    return {
        "data": data,
        "uri": filepath,
        }

def index_file(filepath):
    doc = get_insert_dict(filepath)
    es = get_instance()
    es.index(index=index_name, document=doc)