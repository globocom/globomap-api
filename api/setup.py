import json

from models.constructor import Constructor
from models.document import Document

# Create Colls
with open('api/specs/load/collections_start.json', 'r') as fp:
    collections = json.load(fp)

for collection in collections['collections']:
    constructor = Constructor(collection)
    constructor.factory()

# Create Graph
with open('api/specs/load/graphs_start.json', 'r') as fp:
    graphs = json.load(fp)

for graph in graphs['graphs']:
    graph['type'] = 'graph'
    constructor = Constructor(graph)
    constructor.factory()

# Create Document
with open('api/specs/examples/document.json', 'r') as fp:
    documents = json.load(fp)


for document in documents['documents']:
    graph = {
        'type': 'collection',
        'name': document['collection']
    }

    constructor = Constructor(graph)
    collection = constructor.factory()
    document['content']['_key'] = '{}_{}'.format(
        document['content']['provider'],
        document['content']['id']
    )

    try:
        doc = Document(collection)
        doc.create_document(document['content'])
    except Exception as e:
        raise Exception(e)


# Create Egde
with open('api/specs/examples/edge.json', 'r') as fp:
    documents = json.load(fp)

for document in documents['edges']:
    graph = {
        'type': 'edges',
        'name': document['collection']
    }

    constructor = Constructor(graph)
    collection = constructor.factory()
    document['content']['_key'] = '{}_{}'.format(
        document['content']['provider'],
        document['content']['id']
    )
    document['content']['_to'] = '{}/{}_{}'.format(
        document['to']['collection'],
        document['to']['provider'],
        document['to']['id']
    )
    document['content']['_from'] = '{}/{}_{}'.format(
        document['from']['collection'],
        document['from']['provider'],
        document['from']['id']
    )

    try:
        doc = Document(collection)
        doc.create_document(document['content'])
    except Exception as e:
        raise Exception(e)
