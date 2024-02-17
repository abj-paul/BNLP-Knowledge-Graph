import arxiv
import os 


def download_pdfs_from_topic(topic):
  if not os.path.exists("./data"):
    os.mkdir("./data")
  
  if not os.path.exists(f"./data/{topic}"):
    os.mkdir(f"./data/{topic}")

  search = arxiv.Search(
    query = topic,
    id_list = [],
    max_results = 10,
    sort_by = arxiv.SortCriterion.Relevance,
    sort_order = arxiv.SortOrder.Descending
  )
  for result in search.results():
      print(result.title)
      result.download_pdf(f"./data/{topic}/")


download_pdfs_from_topic("Word Embedding AND Bangla")
