# Creating a llama index

import llama_index
from llama_index import VectorStoreIndex,Document

index = VectorStoreIndex(nodes=[
    {"host": "localhost", "port": 8000},
    {"host": "another-node", "port": 8000},
])

# Initialize the vectors first

index = VectorStoreIndex(index_struct={
    "vectors": [[0.1, 0.2, 0.3], [0.4, 0.5, 0.6], [0.7, 0.8, 0.9]],
    "document_ids": [1, 2, 3],
})


# Add documents to the index
index.add(Document(id=1,text="This is a first document"))
index.add(Document(id=2,text="This is a second document"))
index.add(Document(id=3,text="This is a third document"))

# save the index into a file

index.save('index.dat')