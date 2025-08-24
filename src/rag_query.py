# src/rag_query.py


from langchain.vectorstores import Chroma
from langchain.embeddings import HuggingFaceEmbeddings



# load the same embedding function used during preprocessing
embedding_func = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

# connect to the existing DB


vector_store = Chroma(collection_name="langchain", embedding_function=embedding_func,persist_directory='../db')
retriever = vector_store.as_retriever(search_kwargs={"k": 4})
def search_papers(query: str, n_results: int = 3):
    """Search papers in ChromaDB and return top matches with metadata"""
    #results = vector_store.similarity_search(
        #query,
        #k=5
        
    #)
    docs = retriever.get_relevant_documents(query)
    out = []
    print(docs)
    for i, d in enumerate(docs):
        out.append({
            "rank": i + 1,
            "text": d.page_content,
            "title": d.metadata.get("title"),
            "authors": d.metadata.get("authors", []),
            "affiliations": d.metadata.get("affiliations", []),
            "pdf_url": d.metadata.get("pdf_url"),
            "chunk_index": d.metadata.get("chunk_index"),
        })
    return out
    print(results)
    #return results
    # format results for readability
    papers = []
    for ids, metadata, doc in zip(results["ids"][0], results["metadatas"][0], results["documents"][0]):
        papers.append({
            "id": ids,
            "title": metadata.get("title", "N/A"),
            "authors": metadata.get("authors", []),
            "affiliations": metadata.get("affiliations", []),
            "snippet": doc[:300] + "..."  # just a preview
        })

    return papers