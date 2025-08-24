from langchain.vectorstores import Chroma
from langchain.embeddings import HuggingFaceEmbeddings
from arxiv_ingestion import ingest_documents
def persist_database(documents):
    
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    vectordb = Chroma.from_documents(documents, embeddings, persist_directory='../db')
    vectordb.persist()
    print("Indexed all papers with authors, affiliations, and embeddings!")

if __name__ == "__main__":
    print("Fetching CS.CV papers from arXiv...")
    documents = ingest_documents(1)
    persist_database(documents)