import scipdf
import tqdm
import os
import joblib
# First start scipdf server by running the grobid-service.sh
research_paper_list = []
for filename in os.listdir("./"):
    if filename.endswith("pdf"):
        research_paper_list.append(filename)

parsing_results = []
for research_paper_name in tqdm.tqdm(research_paper_list):
    article_dict = scipdf.parse_pdf_to_dict(f'./{research_paper_name}')
    parsing_results.append(article_dict)


joblib.dump(parsing_results, "parsed_papers.joblib")
