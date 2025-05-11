import sys
import os
import logging
import datetime as dt
from pathlib import Path

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from examples.arxiv_fetcher_example import fetch_papers_for_date, create_mock_papers
from examples.html_parser_example import parse_arxiv_html, demo_with_mock_data
from examples.rss_generator_example import generate_rss_with_mock_data

from src.rss_generator import generate

logging.basicConfig(level=logging.INFO, 
                    format='%(asctime)s - %(levelname)s - %(message)s')

def run_combined_example(target_date="2025/5/1", use_mock_data=False, max_papers=10):
    """
    Run a combined example of all three modules.
    
    Args:
        target_date: Date string in format YYYY/MM/DD
        use_mock_data: Whether to use mock data instead of real API calls
        max_papers: Maximum number of papers to process
    """
    print("\n" + "="*50)
    print("COMBINED EXAMPLE: arXiv RSS Proxy Workflow")
    print("="*50)
    
    os.makedirs("./examples", exist_ok=True)
    
    print("\n--- STEP 1: Fetching Papers ---")
    if use_mock_data:
        print("Using mock data instead of real API calls")
        papers = create_mock_papers(target_date)
    else:
        print(f"Fetching papers for date: {target_date}")
        papers = fetch_papers_for_date(target_date)
        
        if not papers:
            print("No papers found, falling back to mock data")
            papers = create_mock_papers(target_date)
    
    papers = papers[:max_papers]
    print(f"Processing {len(papers)} papers")
    
    print("\n--- STEP 2: Parsing HTML ---")
    html_data = demo_with_mock_data()  # Get mock HTML data once
    
    for paper in papers:
        paper['html_data'] = {
            "figs": html_data['figs'],
            "authors": html_data['authors'],
            "affils": html_data['affils']
        }
    
    print("\n--- STEP 3: Adding Translations (Mock) ---")
    for paper in papers:
        paper['summary_ja'] = f"これは「{paper['title']}」の要約の日本語翻訳です。実際のシステムではGemini APIを使用して翻訳されます。"
        print(f"Added translation for paper: {paper['id']}")
    
    print("\n--- STEP 4: Generating RSS Feed ---")
    filtered_papers = papers[:5]  # First 5 papers as "filtered"
    other_papers = papers[5:]     # Remaining papers as "other"
    
    for paper in filtered_papers + other_papers:
        if isinstance(paper['updated'], str):
            paper['updated'] = dt.datetime.strptime(
                paper['updated'], "%Y-%m-%dT%H:%M:%SZ"
            ).replace(tzinfo=dt.timezone.utc)
    
    output_path = "./examples/combined_example_rss.xml"
    generate(filtered_papers, other_papers, output_path)
    
    print(f"\nRSS feed generated at: {output_path}")
    
    try:
        with open(output_path, 'r') as f:
            lines = f.readlines()
            print("\nFirst 10 lines of the generated RSS XML:")
            for i, line in enumerate(lines[:10]):
                print(f"{i+1}: {line.strip()}")
    except Exception as e:
        logging.error(f"Error reading generated RSS file: {e}")
    
    print("\n" + "="*50)
    print("COMBINED EXAMPLE COMPLETED SUCCESSFULLY")
    print("="*50)

if __name__ == "__main__":
    run_combined_example(target_date="2025/5/1", use_mock_data=False, max_papers=10)
