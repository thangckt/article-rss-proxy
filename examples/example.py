#%%
import logging
from datetime import datetime
from zoneinfo import ZoneInfo
from pathlib import Path
from joblib import Parallel, delayed

from src.config import MAX_NJOBS

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

YYMMDD = "250515"
#%%
"""
step1. fetch
"""
from src.arxiv_fetcher import fetch_papers_for_date

papers = fetch_papers_for_date(datetime.strptime(YYMMDD, "%y%m%d").replace(tzinfo=ZoneInfo("Asia/Tokyo")))

print(len(papers))
#%%
"""
step1.5. save and load
"""
import json

with open(Path(__file__).parent/f"fetched_example_{YYMMDD}.jsonl", "w") as f:
    for paper in papers:
        json.dump(paper, f, ensure_ascii=False)
        f.write("\n")

papers = []
with open(Path(__file__).parent/f"fetched_example_{YYMMDD}.jsonl", "r", encoding="utf-8") as f:
    for line in f:
        paper = json.loads(line)
        papers.append(paper)
#%%
"""
step2. recommend
"""
from src.llm_utils import recommend_papers

are_recommended = recommend_papers(papers)

recommended_papers = []
other_papers = []
for is_recommended, paper in zip(are_recommended, papers):
    if is_recommended:
        recommended_papers.append(paper)
        print(f"yes: {paper['title']}")
    else:
        other_papers.append(paper)
        print(f"no: {paper['title']}")

print(len(recommended_papers))
#%%
"""
step3. translate
"""
from src.llm_utils import translate_abstract

abstract_jas = Parallel(n_jobs=MAX_NJOBS, backend="threading")(
    delayed(translate_abstract)(paper) for paper in recommended_papers
)

for abstract_ja, paper in zip(abstract_jas, recommended_papers):
    paper["summary_ja"] = abstract_ja
    print(paper["title"])
    print(f"ja: {abstract_ja}")
    print("-----")

translated_papers = recommended_papers

#%%
"""
step3.5. save and load
"""
import json

with open(Path(__file__).parent/f"translated_example_{YYMMDD}.jsonl", "w") as f:
    for paper in translated_papers:
        json.dump(paper, f, ensure_ascii=False)
        f.write("\n")

translated_papers = []
with open(Path(__file__).parent/f"translated_example_{YYMMDD}.jsonl", "r", encoding="utf-8") as f:
    for line in f:
        paper = json.loads(line)
        translated_papers.append(paper)
#%%
"""
step4. parse
"""
from src.arxiv_html_parser import extract_fig1_authors_affils

extracted_results = Parallel(n_jobs=MAX_NJOBS, backend="threading")(
    delayed(extract_fig1_authors_affils)(paper["id"]) for paper in papers
    )

for extracted, paper in zip(extracted_results, translated_papers):
    paper["fig1"] = extracted["fig1"]
    paper["authors"] = extracted["authors"]
    paper["affils"] = extracted["affils"]

pushing_papers = translated_papers
#%%
"""
step5. generate
"""
from src.rss_generator import generate_rss_file

generate_rss_file(pushing_papers, other_papers, Path(__file__).parent/f"rss_example_{YYMMDD}.xml")

# %%
