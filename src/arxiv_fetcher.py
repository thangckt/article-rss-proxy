from __future__ import annotations
import time, logging, requests, feedparser, datetime as dt
from zoneinfo import ZoneInfo
from typing import List, Dict

CATEGORIES = [
    "cond-mat.mtrl-sci", "physics.chem-ph", "physics.comp-ph",
    "cs.AI", "cs.LG", "cs.CL"
]
BASE_URL = ("http://export.arxiv.org/api/query?"
            "search_query=cat:{cat}+AND+submittedDate:[{start}+TO+{end}]"
            "&start=0&max_results=1000")

JST = ZoneInfo("Asia/Tokyo")

def _jst_range_for_last_cycle(now_utc: dt.datetime) -> tuple[int, int]:
    """
    arXiv は JST10:00 更新。前日の10:00 ～ 今日の10:00 の 24h の論文を取得する。
    """
    now_jst = now_utc.astimezone(JST)
    today10 = now_jst.replace(hour=10, minute=0, second=0, microsecond=0)
    yesterday10 = today10 - dt.timedelta(days=1)
    
    return int(yesterday10.timestamp()), int(today10.timestamp())

def fetch_new_papers() -> List[Dict]:
    utc_now = dt.datetime.utcnow()
    start, end = _jst_range_for_last_cycle(utc_now)
    logging.info("Query window JST: %s - %s",
                 dt.datetime.fromtimestamp(start, JST),
                 dt.datetime.fromtimestamp(end,   JST))
    papers: List[Dict] = []
    for cat in CATEGORIES:
        url = BASE_URL.format(cat=cat, start=start, end=end)
        feed = feedparser.parse(requests.get(url, timeout=30).text)
        for entry in feed.entries:
            papers.append({
                "id":      entry.id.split('/')[-1],
                "title":   entry.title.strip(),
                "link":    entry.link,
                "summary": entry.summary.strip(),
                "authors": [a.name for a in entry.authors],
                "category": cat,
                "updated": entry.updated
            })
    logging.info("Fetched %s papers", len(papers))
    return papers
