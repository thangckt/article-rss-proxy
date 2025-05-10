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
    arXiv は JST9:00 更新。9:00 ～ 翌 9:00 の 24h を 1 サイクルと定義し、
    直近終了したサイクルを返す。
    """
    now_jst = now_utc.astimezone(JST)
    today9  = now_jst.replace(hour=9, minute=0, second=0, microsecond=0)
    if now_jst < today9:
        end   = today9
    else:
        end   = today9 + dt.timedelta(days=1)
    start = end - dt.timedelta(days=1)
    return int(start.timestamp()), int(end.timestamp())

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
