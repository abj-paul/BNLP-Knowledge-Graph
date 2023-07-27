import arxiv

search = arxiv.Search(
  query = "Word Embedding in Bangla",
  id_list = [],
  max_results = float('inf'),
  sort_by = arxiv.SortCriterion.Relevance,
  sort_order = arxiv.SortOrder.Descending
)
for result in search.results():
    print(result.title)
    result.download_pdf()
