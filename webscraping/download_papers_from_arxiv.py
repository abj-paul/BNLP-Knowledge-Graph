import arxiv
# max_results = float('inf'),
search = arxiv.Search(
  query = "Word Embedding in Bangla",
  id_list = [],
  max_results = 10,
  sort_by = arxiv.SortCriterion.Relevance,
  sort_order = arxiv.SortOrder.Descending
)
for result in search.results():
    print(result.title)
    result.download_pdf()
