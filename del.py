import arxiv
from semanticscholar import SemanticScholar


client = arxiv.Client()

search = arxiv.Search(
  query = "Playing Atari with Deep Reinforcement Learning",
  max_results = 1,
  sort_by = arxiv.SortCriterion.Relevance
)

results = list(client.results(search))
result = results[0]
id = result

sch = SemanticScholar()
papers = sch.get_paper()
for r in papers:
    print(r)
