import joblib 
import re

dataset_2500 = joblib.load("data/50_topics_dataset.joblib")

def extract_reference_section(text):
    reference_labels = ["References", "Reference", "Bibliography", "Works Cited", "Literature Cited", "Citations"]
    references_index = -1
    for label in reference_labels:
        references_index = text.find(label)
        if references_index != -1:
            break

    reference_section = text[references_index:]
    reference_lines = reference_section.split('\n')
    year_pattern = r'\b(?:19|20)\d{2}\b'  # Matches years in the range 1900-2099
    reference_lines_with_years = [line.strip() for line in reference_lines if re.search(year_pattern, line)]
    references = '\n'.join(reference_lines_with_years)

    
    return references


found = 0
not_found = 0
for paper_metadata in dataset_2500:
    try:
        references = extract_reference_section(paper_metadata["Content"])
        print(references)
        found+=1
    except:
        print("No text section..")
        not_found+=1


print(f"Found={found}, Not Found={not_found}")
    
