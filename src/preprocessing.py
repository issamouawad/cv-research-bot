from langchain.vectorstores import Chroma
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter

from arxiv_ingestion import ingest_documents
def persist_database(documents):
    
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    
    # try:
    #     collection = client.get_collection(name='cvpapers', embedding_function=embeddings)
    # except:
    #     collection = client.create_collection(name='cvpapers', embedding_function=embeddings)
    
    ids = [str(i) for i in range(len(documents))]

    vectordb = Chroma.from_documents(documents, embeddings, ids=ids,persist_directory='../db')
    #collection.add(ids=ids, documents=chunks, metadatas=metadatas)
    vectordb.persist()
    print("Indexed all papers with authors, affiliations, and embeddings!")

if __name__ == "__main__":
    print("Fetching CS.CV papers from arXiv...")
    documents = ingest_documents(20)
    print(documents)
    persist_database(documents)