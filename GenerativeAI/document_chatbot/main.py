# creating a document question answering chatbot 

# Import libraries
from langchain.embeddings import UniversalSentenceEncoder
from langchain.document_loaders import TextLoader
from langchain.vectorstores import GoogleVertexAI

# Define document loader and embedding model
document_loader = TextLoader(documents=["Thahseer is a good human being . He is a software engineer at Cubet. He is a BSc Maths graduate from Calicut University"])
embedding_model = UniversalSentenceEncoder()

# Create Google Vertex AI Vector Store instance
vector_store = GoogleVertexAI(
    endpoint="YOUR_VERTEX_ENDPOINT",
    deployment_id="YOUR_PALM_DEPLOYMENT_ID",
)

# Generate and store embeddings
embeddings = embedding_model.embed(document_loader)
vector_store.write_documents(embeddings, document_ids=["doc_id_1", "doc_id_2", ...])
