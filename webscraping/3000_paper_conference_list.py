import requests
from bs4 import BeautifulSoup
import csv

def scrape_bangla_nlp_papers(topic, num_papers):
    url = f'https://scholar.google.com/scholar?q={topic}+Bangla+NLP'
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    papers = []
    results = soup.find_all('div', class_='gs_r gs_or gs_scl')
    
    for result in results[:num_papers]:
        title = result.find('h3', class_='gs_rt').text
        journal_elem = result.find('div', class_='gs_a')
        if journal_elem:
            journal = journal_elem.text.split(' - ')[0]
        else:
            journal = "Unknown"
        year_elem = result.find('span', class_='gs_oph')
        if year_elem:
            year = year_elem.text.split()[-1]
        else:
            year = "Unknown"
        conf_elem = result.find('div', class_='gs_a')
        if conf_elem:
            conf_info = conf_elem.text.split(' - ')[1:]
            conference = ''.join(conf_info)
        else:
            conference = "Unknown"
        papers.append({'title': title, 'journal': journal, 'year': year, 'conference': conference})
    
    return papers

def save_to_csv(papers, filename):
    with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['Title', 'Journal', 'Conference', 'Year']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for paper in papers:
            writer.writerow({'Title': paper['title'], 'Journal': paper['journal'], 'Conference': paper['conference'], 'Year': paper['year']})

def main():
    nlp_topics = [
    "Stemming",
    "Sign Language",
    "Hate Speech",
    "POS Tagging",
    "Sentiment Analysis",
    "Named Entity Recognition (NER)",
    "Machine Translation",
    "Speech Recognition",
    "Text Summarization",
    "Word Segmentation",
    "Dependency Parsing",
    "Morphological Analysis",
    "Sentiment Classification",
    "Emotion Detection",
    "Part-of-Speech (POS) Tagging",
    "Question Answering",
    "Topic Modeling",
    "Language Generation",
    "Code-Switching Detection",
    "Text Classification",
    "Lexicon-based Sentiment Analysis",
    "Diacritic Restoration",
    "Pronoun Resolution",
    "Discourse Analysis",
    "Opinion Mining",
    "Author Profiling",
    "Text Clustering",
    "Document Classification",
    "Word Sense Disambiguation",
    "Text Normalization",
    "Paraphrase Identification",
    "Syntax Analysis",
    "Emotion Classification",
    "Style Transfer",
    "Dialogue Systems",
    "Multilingual NLP",
    "Semantic Role Labeling",
    "Relation Extraction",
    "Speech Synthesis",
    "Named Entity Disambiguation",
    "Coreference Resolution",
    "Irony Detection",
    "Sarcasm Detection",
    "Text Generation",
    "Plagiarism Detection",
    "Abstractive Summarization",
    "Semantic Parsing",
    "Grammatical Error Correction",
    "Natural Language Understanding",
    "Natural Language Generation"
    ]
    num_papers = 20  # Adjust the number of papers to scrape for each topic
    all_papers = []

    for topic in nlp_topics:
        print(f"Scraping papers for topic: {topic}")
        papers = scrape_bangla_nlp_papers(topic, num_papers)
        all_papers.extend(papers)
    
    filename = 'bangla_nlp_papers.csv'
    save_to_csv(all_papers, filename)
    print(f"{len(all_papers)} papers scraped and saved to {filename}")

if __name__ == "__main__":
    main()

