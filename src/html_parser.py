import requests, logging
from bs4 import BeautifulSoup
from typing import List, Tuple, Dict

def _get_html_soup(arxiv_id: str) -> Tuple[int, BeautifulSoup]:
    url = f"https://arxiv.org/html/{arxiv_id}"
    try:
        resp = requests.get(url, timeout=30)
        logging.info(f"Fetched HTML for paper {arxiv_id}, status: {resp.status_code}")
        return resp.status_code, BeautifulSoup(resp.text, 'html.parser')
    except Exception as e:
        logging.error(f"Failed to fetch HTML for paper {arxiv_id}: {e}")
        return 500, BeautifulSoup("", 'html.parser')

def extract(arxiv_id: str) -> Dict:
    status, soup = _get_html_soup(arxiv_id)
    if status != 200:
        return {"figs": [], "authors": [], "affils": []}

    figs = []
    try:
        figure_imgs = soup.select('.ltx_figure > img')
        figure_captions = soup.select('.ltx_figure > figcaption')
        logging.info(f"Found {len(figure_imgs)} figures for paper {arxiv_id}")
        
        for img, cap in zip(figure_imgs, figure_captions):
            try:
                figs.append({
                    "src": f"https://arxiv.org/html/{arxiv_id}/{img['src']}",
                    "caption": cap.get_text(strip=True)
                })
            except Exception as e:
                logging.error(f"Error processing figure for paper {arxiv_id}: {e}")
    except Exception as e:
        logging.error(f"Error extracting figures for paper {arxiv_id}: {e}")

    authors, affils = set(), set()
    section = soup.find('div', class_='ltx_authors')
    if section:
        person_spans = section.find_all('span', class_='ltx_personname')
        logging.info(f"Found {len(person_spans)} author elements for paper {arxiv_id}")
        for p in person_spans:
            if p:  # Check if p is not empty
                try:
                    for t in p.find_all(['sup', 'span']): 
                        t.decompose()
                    authors.update([n.strip() for n in
                                  p.get_text(" ", strip=True).replace(' and ', ',').split(',')
                                  if n.strip()])
                except Exception as e:
                    logging.error(f"Error processing author element for paper {arxiv_id}: {e}")
            
        contact_spans = section.find_all('span', class_='ltx_contact')
        logging.info(f"Found {len(contact_spans)} affiliation elements for paper {arxiv_id}")
        for c in contact_spans:
            if c:  # Check if c is not empty
                try:
                    txt = c.get_text(" ", strip=True)
                    if '@' not in txt.lower():
                        affils.add(txt)
                except Exception as e:
                    logging.error(f"Error processing affiliation element for paper {arxiv_id}: {e}")

    return {"figs": figs, "authors": sorted(authors), "affils": sorted(affils)}
