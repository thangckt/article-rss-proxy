#%%
import logging
import json
import datetime as dt
from zoneinfo import ZoneInfo

import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent.resolve()))

from src.arxiv_fetcher import fetch_papers_for_date
from src.rss_generator import generate

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

JST = ZoneInfo("Asia/Tokyo")
#%%
"""
step1. fetch
"""
papers = fetch_papers_for_date(dt.datetime(2025, 5, 14, tzinfo=JST))

# with open(Path(__file__).parent/"fetched_example_250501.jsonl", "w") as f:
#     for paper in papers:
#         json.dump(paper, f, ensure_ascii=False)
#         f.write("\n")

# papers = []
# with open(Path(__file__).parent/"fetched_example_250501.jsonl", "r", encoding="utf-8") as f:
#     for line in f:
#         paper = json.loads(line)
#         papers.append(paper)
#%%
"""
step2. filter
"""
from src.llm_utils import filter_papers

filter_bools = filter_papers(papers)

for filter_bool, paper in zip(filter_bools, papers):
    if filter_bool:
        print(f"yes: {paper['title']}")
    else:
        print(f"no: {paper['title']}")

filtered_papers = [paper for filter_bool, paper in zip(filter_bools, papers) if filter_bool]
other_papers = [paper for filter_bool, paper in zip(filter_bools, papers) if not filter_bool]
#%%
"""
step3. translate
"""
from src.llm_utils import translate_abstracts

abstract_jas = translate_abstracts(filtered_papers)
for abstract_ja, paper in zip(abstract_jas, filtered_papers):
    print(paper["title"])
    print(f"ja: {abstract_ja}")
    print("-----")

for paper, abstract_ja in zip(filtered_papers, abstract_jas):
    paper["summary_ja"] = abstract_ja
translated_papers = filtered_papers

# with open(Path(__file__).parent/"translated_example_250514.jsonl", "w") as f:
#     for paper in translated_papers:
#         json.dump(paper, f, ensure_ascii=False)
#         f.write("\n")

# translated_papers = []
# with open(Path(__file__).parent/"translated_example_250514.jsonl", "r", encoding="utf-8") as f:
#     for line in f:
#         paper = json.loads(line)
#         translated_papers.append(paper)
#%%
"""
step4. parse
"""
from src.html_parser import extract_parallel

extracted_results = extract_parallel(translated_papers)
for extracted, paper in zip(extracted_results, translated_papers):
    paper["fig1"] = extracted["figs"][0]["src"] if extracted["figs"] else ""
    paper["authors"] = extracted["authors"]
    paper["affils"] = extracted["affils"]


#%%
"""
step5. generate
"""
generate(translated_papers, other_papers, Path(__file__).parent/"rss_example_250514.xml")

# %%
