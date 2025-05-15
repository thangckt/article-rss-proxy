import re
import logging
import requests
import feedparser
from datetime import timezone, timedelta

from src.config import CATEGORIES

ARXIV_API_URL = ("http://export.arxiv.org/api/query?"
            "search_query=cat:{cat}+AND+submittedDate:[{start}+TO+{end}]"
            "&start=0&max_results=1000")


def jst_date_to_arxiv_range(date_jst):
    """
    arXivはJST9:00更新。前日の10:00~今日の10:00の24hの論文を取得するためのstringを返す。
    """
    date_jst10 = date_jst.replace(hour=10, minute=0, second=0, microsecond=0)
    end_utc = date_jst10.astimezone(timezone.utc)
    start_utc = end_utc - timedelta(days=1)
    return start_utc.strftime("%Y%m%d%H%M"), end_utc.strftime("%Y%m%d%H%M")


def fetch_papers_for_date(date_jst):
    start_str, end_str = jst_date_to_arxiv_range(date_jst)
    papers = []
    for cat in CATEGORIES:
        url = ARXIV_API_URL.format(cat=cat, start=start_str, end=end_str)
        try:
            response = requests.get(url, timeout=30)
            feed = feedparser.parse(response.text)
            for entry in feed.entries:
                papers.append({
                    "id": entry.id.split('/')[-1],
                    "title": re.sub(r'\s+', ' ', entry.title).strip(),
                    "link": entry.link,
                    "summary": entry.summary.strip(),
                    "authors": [a.name for a in entry.authors],
                    "category": cat,
                    "updated": entry.updated
                })
        except Exception as e:
            logging.error(f"Error fetching papers for category {cat}: {e}")
    unique_papers = list({paper["id"]: paper for paper in papers}.values())
    return unique_papers
