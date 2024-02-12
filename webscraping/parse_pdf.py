import fitz  # PyMuPDF
import re
import os

def extract_text_from_pdf(pdf_path):
    doc = fitz.open(pdf_path)
    text = ''
    for page_num in range(doc.page_count):
        page = doc[page_num]
        text += page.get_text()
    doc.close()
    return text

def extract_sections(text):
    # Regular expressions to extract sections
    author_pattern = re.compile(r'Author[s]*:(.*?)(?=(Abstract|Citation)|$)', re.DOTALL | re.IGNORECASE)
    abstract_pattern = re.compile(r'Abstract:(.*?)(?=(Author|Citation)|$)', re.DOTALL | re.IGNORECASE)
    citation_pattern = re.compile(r'Citation[s]*:(.*?)(?=(Author|Abstract)|$)', re.DOTALL | re.IGNORECASE)

    # Extracting sections
    author_match = author_pattern.search(text)
    abstract_match = abstract_pattern.search(text)
    citation_match = citation_pattern.search(text)

    author_section = author_match.group(1).strip() if author_match else None
    abstract_section = abstract_match.group(1).strip() if abstract_match else None
    citation_section = citation_match.group(1).strip() if citation_match else None

    return author_section, abstract_section, citation_section

def extract_information_from_papers_for_topic(topic):
    for filename in os.listdir(f"./data/{topic}"):
        if filename.endswith(".pdf"):
            pdf_path = f"./data/{topic}/{filename}"

            pdf_text = extract_text_from_pdf(pdf_path)
            author, abstract, citation = extract_sections(pdf_text)

            print("Author:", author)
            print("Abstract:", abstract)
            print("Citation:", citation)
            print()

topic = "Word Embedding in Bangla, Word2Vec"
extract_information_from_papers_for_topic(topic)
