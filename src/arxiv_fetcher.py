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

def _jst_range_for_last_cycle(now_utc: dt.datetime) -> tuple[str, str]:
    """
    arXiv は JST10:00 更新。前日の10:00 ～ 今日の10:00 の 24h の論文を取得する。
    Returns date strings in YYYYMMDDHHMM format for arXiv API.
    """
    now_jst = now_utc.astimezone(JST)
    today10 = now_jst.replace(hour=10, minute=0, second=0, microsecond=0)
    yesterday10 = today10 - dt.timedelta(days=1)
    
    start_str = yesterday10.strftime("%Y%m%d%H%M")
    end_str = today10.strftime("%Y%m%d%H%M")
    
    return start_str, end_str

def fetch_new_papers() -> List[Dict]:
    utc_now = dt.datetime.utcnow()
    start_str, end_str = _jst_range_for_last_cycle(utc_now)
    
    start_dt = dt.datetime.strptime(start_str, "%Y%m%d%H%M").replace(tzinfo=JST)
    end_dt = dt.datetime.strptime(end_str, "%Y%m%d%H%M").replace(tzinfo=JST)
    
    logging.info("Query window JST: %s - %s", start_dt, end_dt)
    logging.info("Using query format: submittedDate:[%s+TO+%s]", start_str, end_str)
    
    papers: List[Dict] = []
    seen_ids = set()  # Track seen paper IDs to avoid duplicates
    
    for cat in CATEGORIES:
        url = BASE_URL.format(cat=cat, start=start_str, end=end_str)
        feed = feedparser.parse(requests.get(url, timeout=30).text)
        
        category_papers = 0
        for entry in feed.entries:
            paper_id = entry.id.split('/')[-1]
            
            if paper_id in seen_ids:
                continue
                
            seen_ids.add(paper_id)
            papers.append({
                "id":      paper_id,
                "title":   entry.title.strip(),
                "link":    entry.link,
                "summary": entry.summary.strip(),
                "authors": [a.name for a in entry.authors],
                "category": cat,
                "updated": entry.updated
            })
            category_papers += 1
            
        logging.info("Fetched %s papers for category %s (%s unique)", 
                    len(feed.entries), cat, category_papers)
    
    logging.info("Total papers fetched: %s", len(papers))
    return papers
