import logging
import json
import datetime as dt
from zoneinfo import ZoneInfo

import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent.resolve()))

from src.arxiv_fetcher import fetch_papers_for_date
from src.html_parser import extract
from src.rss_generator import generate

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

JST = ZoneInfo("Asia/Tokyo")

"""
step1. fetch
"""
# papers = fetch_papers_for_date(dt.datetime(2025, 5, 1, tzinfo=JST))

# with open(Path(__file__).parent/"fetched_example_250501.jsonl", "w") as f:
#     for paper in papers:
#         json.dump(paper, f, ensure_ascii=False)
#         f.write("\n")

papers = []
with open(Path(__file__).parent/"fetched_example_250501.jsonl", "r", encoding="utf-8") as f:
    for line in f:
        paper = json.loads(line)
        papers.append(paper)

"""
step2. filter
"""
filtered_papers = papers[:2]


"""
step3. translate
"""
for paper in filtered_papers:
    paper["summary_ja"] = "これはテスト翻訳です"
translated_papers = filtered_papers


"""
step4. parse
"""
# for paper in translated_papers:
#     print("-----"+paper["id"]+"-----")
#     print(paper["title"])
#     extracted = extract(paper["id"])
#     print(f"fig1:{extracted['figs'][0]['src']}")
#     print("-----authors-----")
#     for author in extracted["authors"]:
#         print(author)
#     print("-----affils-----")
#     for affil in extracted["affils"]:
#         print(affil)
#     print("--------------------")

"""
step5. generate
"""
generate(translated_papers, [], Path(__file__).parent/"example_rss.xml")
