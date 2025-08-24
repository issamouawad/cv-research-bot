import requests
import json
import os
from datetime import datetime, timedelta
import xml.etree.ElementTree as ET
import langextract as lx
import tempfile
from PyPDF2 import PdfReader
from langchain.docstore.document import Document
DATA_DIR = "../data"
os.makedirs(DATA_DIR, exist_ok=True)

#gets top 50 papers from last month in cs.CV
def _fetch_arxiv_cs_cv(max_results=50):
    base_url = "http://export.arxiv.org/api/query?"
    last_month = (datetime.now() - timedelta(days=30)).strftime("%Y-%m-%d")
    query = f"search_query=cat:cs.CV+AND+submittedDate:[{last_month}0000+TO+{datetime.now().strftime('%Y%m%d')}2359]&start=0&max_results={max_results}"
    url = base_url + query
    response = requests.get(url)
    return response.text

#parse xml results from arxiv
def _parse_arxiv_xml(xml_string):
    ns = {"atom": "http://www.w3.org/2005/Atom"}
    root = ET.fromstring(xml_string)
    papers = []
    for entry in root.findall("atom:entry", ns):
        title = entry.find("atom:title", ns).text.strip()
        abstract = entry.find("atom:summary", ns).text.strip()
        authors = [a.find("atom:name", ns).text for a in entry.findall("atom:author", ns)]
        published = entry.find("atom:published", ns).text
        pdf_url = next(link.attrib["href"] for link in entry.findall("atom:link", ns) if link.attrib.get("title") == "pdf")
        papers.append({
            "title": title,
            "authors": authors,
            "abstract": abstract,
            "published": published,
            "pdf_url": pdf_url
        })
    return papers
#use langextract (llm-powered) to infer affiliations for the authors, doesn't appear in a reliable way for manual extraction
def _extract_author_affiliations(paper):
    prompt = "Extract authors and their affiliations from the given document."
    examples = [
        lx.data.ExampleData(
            text="John Doe, University of Example; johnd@example.com , Jane Smith, Example Institute, jsmith@example.edu",
            extractions=[
                lx.data.Extraction(
                    extraction_class="author",
                    extraction_text="John Doe",
                    attributes={"affiliation": "University of Example",'email':'johnd@example.com'}
                ),
                lx.data.Extraction(
                    extraction_class="author",
                    extraction_text="Jane Smith",
                    attributes={"affiliation": "Example Institute",'email':'jsmith@example.edu'}
                )
            ]
        )
    ]
    with tempfile.NamedTemporaryFile(suffix=".pdf") as temp_pdf:
        response = requests.get(paper['pdf_url'])
        temp_pdf.write(response.content)
        temp_pdf.flush() 
        reader = PdfReader(temp_pdf)   
        pdf_text = ""     
        for page in reader.pages[0:1]: #only need the first page to find authors and affiliations
            pdf_text += page.extract_text() + "\n"
    
    
    result = lx.extract(
        text_or_documents=pdf_text[0:700], #adhoc trimming, to reduce extraction time, double check 
        prompt_description=prompt,
        examples=examples,
        model_id="gemma3:1b",  # Automatically selects Ollama provider
        model_url="http://localhost:11434",
        use_schema_constraints=True
        )
    authors = []
    affiliations = []
    for ext in result.extractions:
        authors.append(ext.extraction_text)
        affiliations.append(ext.attributes['affiliation'])
    doc = Document(
        page_content=paper['abstract'],
        metadata={
            "title": paper["title"],
            "abstract": paper["abstract"],
            "authors": ','.join(authors),
            "affiliations": ','.join(affiliations),
            "published": paper["published"],
            "pdf_url": paper["pdf_url"]
        }
    )
    return doc
#entry point
def ingest_documents(max_count = 1):
    raw_data = _fetch_arxiv_cs_cv(max_results=2)
    papers = _parse_arxiv_xml(raw_data)
    documents = []
    for i in range(max_count):
        documents.append(_extract_author_affiliations(papers[i]))
    return documents
if __name__ == "__main__":
    print("Fetching CS.CV papers from arXiv...")
    raw_data = _fetch_arxiv_cs_cv()
    papers = _parse_arxiv_xml(raw_data)
    
    
    result = _extract_author_affiliations(papers[0])
    
    
    