from langchain.embeddings import HuggingFaceEmbeddings
import chromadb

from langchain.vectorstores import Chroma
client = chromadb.PersistentClient(path="../db")
embedding_func = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

vector_store_from_client = Chroma(
    client=client,
    collection_name="langchain",
    embedding_function=embedding_func,
)

results = vector_store_from_client.similarity_search(
        "domain shift",
        k=5
        
    )
print(results[0])
