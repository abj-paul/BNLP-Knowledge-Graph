import requests
import xml.etree.ElementTree as ET

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
        'publication_date': paper_entry.find('{http://www.w3.org/2005/Atom}published').text
    }
    return metadata

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

# Example usage
query = 'cat:cs.CV AND submittedDate:[202201010000 TO 202201312359]'
max_results = 5
papers_metadata = extract_metadata_from_arxiv(query, max_results)
if papers_metadata:
    for idx, paper_metadata in enumerate(papers_metadata, start=1):
        print(f"Paper {idx}:")
        print("Title:", paper_metadata['title'])
        print("Authors:", ", ".join(paper_metadata['authors']))
        print("Abstract:", paper_metadata['abstract'])
        print("Publication Date:", paper_metadata['publication_date'])
        print()
else:
    print("No papers found or error occurred.")
