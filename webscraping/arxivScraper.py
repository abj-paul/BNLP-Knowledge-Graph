import requests
import xml.etree.ElementTree as ET
import joblib
import os
import PyPDF2

download_papers = True

def search_arxiv(query, max_results=10):
    url = 'http://export.arxiv.org/api/query'
    params = {
        'search_query': query,
        'max_results': max_results
    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        return response.text
    else:
        print(f"Error: {response.status_code}")
        return None

def extract_paper_metadata(paper_entry):
    metadata = {
        'title': paper_entry.find('{http://www.w3.org/2005/Atom}title').text,
        'authors': [author.find('{http://www.w3.org/2005/Atom}name').text for author in paper_entry.findall('{http://www.w3.org/2005/Atom}author')],
        'abstract': paper_entry.find('{http://www.w3.org/2005/Atom}summary').text,
        'publication_date': paper_entry.find('{http://www.w3.org/2005/Atom}published').text,
        'pdf_url': paper_entry.find('{http://www.w3.org/2005/Atom}link[@title="pdf"][@type="application/pdf"]').attrib['href'],
        'arxiv_id': paper_entry.find('{http://www.w3.org/2005/Atom}id').text.split('/')[-1]  # Extracting the identifier from the URL
    }
    return metadata

def download_paper(pdf_url, save_path):
    response = requests.get(pdf_url)
    if response.status_code == 200:
        with open(save_path, 'wb') as f:
            f.write(response.content)
        print(f"Paper downloaded: {save_path}")
    else:
        print(f"Error downloading paper. Status code: {response.status_code}")

def extract_metadata_from_arxiv(query, max_results=10):
    response_text = search_arxiv(query, max_results)
    if response_text:
        root = ET.fromstring(response_text)
        metadata_list = []
        for entry in root.findall('{http://www.w3.org/2005/Atom}entry'):
            metadata_list.append(entry)
        return [extract_paper_metadata(paper) for paper in metadata_list]
    else:
        return None
def extract_text_from_pdf(pdf_path):
    text = ""
    try:
        with open(pdf_path, 'rb') as f:
            reader = PyPDF2.PdfReader(f)
            for page_num in range(len(reader.pages)):
                page = reader.pages[page_num]
                text += page.extract_text()
    except PyPDF2.errors.PdfReadError as e:
        print(f"Error reading PDF file: {e}")
        text = None
    return text



def download_metadata_for_topics(topic_list):
    dataset = []
    for topic in topic_list:
        #query = 'cat:cs.CV AND submittedDate:[202201010000 TO 202201312359]'
        query = f'{topic} And Bangla'
        max_results = 50
        papers_metadata = extract_metadata_from_arxiv(query, max_results)
        topic_dataset = []
        if papers_metadata:
            for idx, paper_metadata in enumerate(papers_metadata, start=1):
                print(f"Paper {idx}:")
                print("Title:", paper_metadata['title'])
                print("Authors:", ", ".join(paper_metadata['authors']))
                print("Abstract:", paper_metadata['abstract'])
                print("Publication Date:", paper_metadata['publication_date'])
                print("Paper Link:", paper_metadata["pdf_url"])
                print()
        
                if download_papers:
                    if not os.path.exists(f"data/{query}"):
                        os.makedirs(f"data/{query}")
                    save_path = f"data/{query}/Paper_{idx}.pdf"
                    download_paper(paper_metadata['pdf_url'], save_path)
                    print(extract_text_from_pdf(save_path))

                item = {
                    "Title": paper_metadata['title'],
                    "Authors": ", ".join(paper_metadata['authors']),
                    "Abstract": paper_metadata['abstract'],
                    "Publication Date": paper_metadata['publication_date'],
                    "Link": paper_metadata['pdf_url'],
                    "arxiv_id": paper_metadata["arxiv_id"],
                    "Content": extract_text_from_pdf(save_path)
                }
                dataset.append(item)
                topic_dataset.append(item)
            joblib.dump(topic_dataset, f"data/{query}.joblib")
        else:
            print("No papers found or error occurred.")
    joblib.dump(dataset, f"data/{len(topic_list)}_topics_dataset.joblib")

nlp_topics = [
    "Stemming",
    "Part-of-Speech (POS) Tagging",
    "Named Entity Recognition (NER)",
    "Sentiment Analysis",
    "Machine Translation",
    "Dependency Parsing",
    "Coreference Resolution",
    "Semantic Role Labeling (SRL)",
    "Text Summarization",
    "Language Modeling",
    "Text Classification",
    "Entity Linking",
    "Information Extraction",
    "Question Answering",
    "Text Generation",
    "Document Clustering",
    "Text Normalization",
    "Emotion Analysis",
    "Opinion Mining",
    "Core NLP Pipeline",
    "Syntactic Parsing",
    "Dependency Trees",
    "Named Entity Disambiguation",
    "Semantic Parsing",
    "Speech Recognition",
    "Discourse Analysis",
    "Paraphrase Detection",
    "Knowledge Base Population",
    "Text Alignment",
    "Document Classification",
    "Text-to-Speech Synthesis",
    "Dialog Systems",
    "Cross-lingual Information Retrieval",
    "Multi-document Summarization",
    "Code-Switching Detection",
    "Semantic Similarity",
    "Error Detection and Correction",
    "Topic Modeling",
    "Information Retrieval",
    "Named Entity Normalization",
    "Morphological Analysis",
    "Anaphora Resolution",
    "Lexical Semantics",
    "Machine Reading Comprehension",
    "Machine Assisted Translation",
    "Sentiment Classification",
    "Argument Mining",
    "Domain Adaptation",
    "Automatic Text Simplification",
    "Semantic Search"
]

download_metadata_for_topics(nlp_topics)