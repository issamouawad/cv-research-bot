# CS.CV Research Paper Assistant (Proof-of-Concept)

## Overview

This project is a **work in progress** - **proof-of-concept pipeline** for semantic search and retrieval-augmented generation (RAG) over recent Computer Vision papers from arXiv. It demonstrates:

- **ArXiv ingestion** → fetch metadata and PDFs  
- **Text extraction** → extract full text from PDFs  
- **Author / affiliation extraction** → using LangExtract with backend-agnostic LLM (Ollama or others)  
- **Vector embeddings** → generate embeddings of paper text using Hugging Face models  
- **Vector DB indexing** → store enriched documents in ChromaDB for retrieval  
- **RAG-ready query interface** → retrieve papers semantically and optionally answer questions  

This project emphasizes **modularity and backend abstraction**, allowing you to swap LLMs (Ollama, OpenAI, Hugging Face) without changing the pipeline.
