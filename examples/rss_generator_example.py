import sys
import os
import logging
import datetime as dt
from pathlib import Path

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.rss_generator import generate, _format_paper_entry, _format_other_papers_description

logging.basicConfig(level=logging.INFO, 
                    format='%(asctime)s - %(levelname)s - %(message)s')

def create_mock_papers(date_str="2025/5/1", count=5):
    """
    Create mock paper data for demonstration.
    
    Args:
        date_str: Date string in format YYYY/MM/DD
        count: Number of mock papers to create
    
    Returns:
        List of mock paper dictionaries
    """
    year, month, day = map(int, date_str.split('/'))
    base_date = dt.datetime(year, month, day, tzinfo=dt.timezone.utc)
    
    mock_papers = []
    categories = ["cs.AI", "cs.LG", "physics.chem-ph", "cond-mat.mtrl-sci"]
    
    for i in range(1, count + 1):
        paper_id = f"2505.{10000 + i}"
        paper_date = base_date + dt.timedelta(hours=i)
        
        paper = {
            "id": paper_id,
            "title": f"Mock Paper {i}: Advanced AI for Scientific Discovery",
            "link": f"https://arxiv.org/abs/{paper_id}",
            "summary": f"This is a mock paper abstract for demonstration purposes. It discusses various aspects of AI applications in scientific research, focusing on novel methodologies for data analysis and pattern recognition in complex systems.",
            "summary_ja": f"これはデモンストレーション用のモック論文要約です。科学研究におけるAIアプリケーションの様々な側面について議論し、複雑なシステムにおけるデータ分析とパターン認識のための新しい方法論に焦点を当てています。",
            "authors": [f"Author {j}" for j in range(1, 4)],
            "category": categories[i % len(categories)],
            "updated": paper_date.strftime("%Y-%m-%dT%H:%M:%SZ")
        }
        mock_papers.append(paper)
    
    return mock_papers

def generate_rss_with_mock_data(output_path="./examples/mock_rss.xml"):
    """
    Generate an RSS feed using mock paper data.
    
    Args:
        output_path: Path where the RSS file will be saved
    """
    all_papers = create_mock_papers(date_str="2025/5/1", count=10)
    
    filtered_papers = all_papers[:5]  # First 5 papers as "filtered"
    other_papers = all_papers[5:]     # Remaining papers as "other"
    
    for paper in filtered_papers + other_papers:
        if isinstance(paper['updated'], str):
            paper['updated'] = dt.datetime.strptime(
                paper['updated'], "%Y-%m-%dT%H:%M:%SZ"
            ).replace(tzinfo=dt.timezone.utc)
    
    logging.info(f"Generating RSS feed with {len(filtered_papers)} filtered papers and {len(other_papers)} other papers")
    generate(filtered_papers, other_papers, output_path)
    
    print(f"\nRSS feed generated at: {output_path}")
    print("\nSample of filtered papers in RSS:")
    for i, paper in enumerate(filtered_papers[:2], 1):
        print(f"\n--- Filtered Paper {i} ---")
        print(f"Title: {paper['title']}")
        print(f"Link: {paper['link']}")
        print(f"Entry content: {_format_paper_entry(paper, with_translation=True)[:150]}...")
    
    print("\nSample of other papers in RSS:")
    other_description = _format_other_papers_description(other_papers[:2])
    print(f"{other_description[:200]}...")
    
    return output_path

if __name__ == "__main__":
    os.makedirs("./examples", exist_ok=True)
    
    rss_path = generate_rss_with_mock_data()
    
    try:
        with open(rss_path, 'r') as f:
            lines = f.readlines()
            print("\nFirst 10 lines of the generated RSS XML:")
            for i, line in enumerate(lines[:10]):
                print(f"{i+1}: {line.strip()}")
    except Exception as e:
        logging.error(f"Error reading generated RSS file: {e}")
