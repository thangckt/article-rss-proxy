import sys
import os
import logging

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.html_parser import extract, _get_html_soup
from bs4 import BeautifulSoup

logging.basicConfig(level=logging.INFO, 
                    format='%(asctime)s - %(levelname)s - %(message)s')

def parse_arxiv_html(arxiv_id):
    """
    Parse HTML content for a given arXiv ID and display extracted information.
    
    Args:
        arxiv_id: arXiv paper ID (e.g., "2304.12345")
    """
    logging.info(f"Parsing HTML for arXiv ID: {arxiv_id}")
    
    status, soup = _get_html_soup(arxiv_id)
    
    if status != 200:
        logging.error(f"Failed to fetch HTML for paper {arxiv_id}, status: {status}")
        return None
    
    extracted_data = extract(arxiv_id)
    
    print(f"\nExtracted data for arXiv ID: {arxiv_id}")
    
    print(f"\nFigures ({len(extracted_data['figs'])}):")
    for i, fig in enumerate(extracted_data['figs'][:3], 1):
        print(f"  Figure {i}:")
        print(f"    URL: {fig['src']}")
        print(f"    Caption: {fig['caption'][:100]}..." if len(fig['caption']) > 100 else f"    Caption: {fig['caption']}")
    
    print(f"\nAuthors ({len(extracted_data['authors'])}):")
    for author in extracted_data['authors'][:10]:
        print(f"  - {author}")
    if len(extracted_data['authors']) > 10:
        print(f"  ... and {len(extracted_data['authors']) - 10} more")
    
    print(f"\nAffiliations ({len(extracted_data['affils'])}):")
    for affil in extracted_data['affils'][:5]:
        print(f"  - {affil}")
    if len(extracted_data['affils']) > 5:
        print(f"  ... and {len(extracted_data['affils']) - 5} more")
    
    return extracted_data

def demo_with_mock_data():
    """
    Demonstrate HTML parsing with mock data when network access is unavailable.
    """
    logging.info("Demonstrating HTML parsing with mock data")
    
    mock_html = """
    <html>
    <body>
        <div class="ltx_authors">
            <span class="ltx_personname">John Doe<sup>1</sup></span>
            <span class="ltx_personname">Jane Smith<sup>2</sup></span>
            <span class="ltx_contact">University of Science</span>
            <span class="ltx_contact">Research Institute</span>
        </div>
        <div class="ltx_figure">
            <img src="figure1.png" />
            <figcaption>This is figure 1 caption</figcaption>
        </div>
        <div class="ltx_figure">
            <img src="figure2.png" />
            <figcaption>This is figure 2 caption</figcaption>
        </div>
    </body>
    </html>
    """
    
    mock_soup = BeautifulSoup(mock_html, 'html.parser')
    
    mock_data = {
        "figs": [
            {"src": "https://arxiv.org/html/2505.12345/figure1.png", "caption": "This is figure 1 caption"},
            {"src": "https://arxiv.org/html/2505.12345/figure2.png", "caption": "This is figure 2 caption"}
        ],
        "authors": ["John Doe", "Jane Smith"],
        "affils": ["Research Institute", "University of Science"]
    }
    
    print("\nMock extracted data:")
    
    print(f"\nFigures ({len(mock_data['figs'])}):")
    for i, fig in enumerate(mock_data['figs'], 1):
        print(f"  Figure {i}:")
        print(f"    URL: {fig['src']}")
        print(f"    Caption: {fig['caption']}")
    
    print(f"\nAuthors ({len(mock_data['authors'])}):")
    for author in mock_data['authors']:
        print(f"  - {author}")
    
    print(f"\nAffiliations ({len(mock_data['affils'])}):")
    for affil in mock_data['affils']:
        print(f"  - {affil}")
    
    return mock_data

if __name__ == "__main__":
    arxiv_id = "2304.12345"  # Example arXiv ID
    
    try:
        extracted_data = parse_arxiv_html(arxiv_id)
        if not extracted_data or not extracted_data['authors']:
            print("\nFalling back to mock data demonstration...")
            demo_with_mock_data()
    except Exception as e:
        logging.error(f"Error in parsing HTML: {e}")
        print("\nFalling back to mock data demonstration...")
        demo_with_mock_data()
