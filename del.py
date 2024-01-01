import arxiv
from semanticscholar import SemanticScholar
from pprint import pprint 


# client = arxiv.Client()

# search = arxiv.Search(
#   query = "Playing Atari with Deep Reinforcement Learning",
#   max_results=3,
#   sort_by=arxiv.SortCriterion.Relevance
# )

# result = list(client.results(search))[0]
# id = result.get_short_id().split('v')[0]
# print(f'{id=}')

sch = SemanticScholar()
pag_res = sch.search_paper(
    query="Playing Atari with Deep Reinforcement Learning",
    limit=1
)
top_paper_id = pag_res[0]["paperId"]
top_paper = sch.get_paper(top_paper_id)
for ref in top_paper.references:
    print(ref['title'])


