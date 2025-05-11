import sys
import os
import logging
import datetime as dt
from zoneinfo import ZoneInfo

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.arxiv_fetcher import CATEGORIES
import requests
import feedparser

logging.basicConfig(level=logging.INFO, 
                    format='%(asctime)s - %(levelname)s - %(message)s')

def fetch_papers_for_date(target_date_str):
    """
    Fetch papers from arXiv for a specific date.
    
    Args:
        target_date_str: Date string in format YYYY/MM/DD
    
    Returns:
        List of paper dictionaries
    """
    year, month, day = map(int, target_date_str.split('/'))
    
    target_date = dt.datetime(year, month, day, tzinfo=dt.timezone.utc)
    next_date = target_date + dt.timedelta(days=1)
    
    start_str = f"{target_date.year}{target_date.month:02d}{target_date.day:02d}0100"
    end_str = f"{next_date.year}{next_date.month:02d}{next_date.day:02d}0100"
    
    date_url = ("http://export.arxiv.org/api/query?"
                "search_query=cat:{cat}+AND+submittedDate:[{start}+TO+{end}]"
                "&start=0&max_results=100")
    
    logging.info(f"Query date range: {start_str} to {end_str}")
    
    papers = []
    for cat in CATEGORIES:
        url = date_url.format(cat=cat, start=start_str, end=end_str)
        logging.info(f"Fetching from URL: {url}")
        
        try:
            response = requests.get(url, timeout=30)
            feed = feedparser.parse(response.text)
            
            for entry in feed.entries:
                papers.append({
                    "id": entry.id.split('/')[-1],
                    "title": entry.title.strip(),
                    "link": entry.link,
                    "summary": entry.summary.strip(),
                    "authors": [a.name for a in entry.authors],
                    "category": cat,
                    "updated": entry.updated
                })
            
            logging.info(f"Fetched {len(feed.entries)} papers for category {cat}")
        except Exception as e:
            logging.error(f"Error fetching papers for category {cat}: {e}")
    
    logging.info(f"Total papers fetched: {len(papers)}")
    return papers

def create_mock_papers(target_date_str):
    """
    Create mock paper data for demonstration when real data is not available.
    
    Args:
        target_date_str: Date string in format YYYY/MM/DD
    
    Returns:
        List of mock paper dictionaries
    """
    year, month, day = map(int, target_date_str.split('/'))
    base_date = dt.datetime(year, month, day, tzinfo=dt.timezone.utc)
    
    logging.info(f"Creating mock data for date: {target_date_str}")
    
    mock_papers = []
    for i, cat in enumerate(CATEGORIES):
        for j in range(2):
            paper_id = f"{year}{month:02d}.{10000 + i*10 + j}"
            paper_date = base_date + dt.timedelta(hours=i*2 + j)
            
            paper = {
                "id": paper_id,
                "title": f"Mock Paper {i*2+j+1}: {cat} Research on {target_date_str}",
                "link": f"https://arxiv.org/abs/{paper_id}",
                "summary": f"This is a mock paper abstract for {cat} category. It discusses various aspects of research in this field, focusing on novel methodologies and recent advancements.",
                "authors": [f"Author {k+1}" for k in range(3)],
                "category": cat,
                "updated": paper_date.strftime("%Y-%m-%dT%H:%M:%SZ")
            }
            mock_papers.append(paper)
    
    logging.info(f"Created {len(mock_papers)} mock papers")
    return mock_papers

if __name__ == "__main__":
    target_date = "2025/5/1"
    papers = fetch_papers_for_date(target_date)
    
    if not papers:
        logging.info("No papers found for %s, using mock data", target_date)
        papers = create_mock_papers(target_date)
    
    print(f"\nSample of papers fetched for {target_date}:")
    for i, paper in enumerate(papers[:3], 1):
        print(f"\n--- Paper {i} ---")
        print(f"Title: {paper['title']}")
        print(f"Authors: {', '.join(paper['authors'])}")
        print(f"Category: {paper['category']}")
        print(f"Link: {paper['link']}")
        print(f"Summary: {paper['summary'][:150]}...")
    
    print(f"\nTotal papers fetched: {len(papers)}")
