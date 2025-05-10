import requests, logging
from bs4 import BeautifulSoup
from typing import List, Tuple, Dict

def _get_html_soup(arxiv_id: str) -> Tuple[int, BeautifulSoup]:
    url = f"https://arxiv.org/html/{arxiv_id}"
    resp = requests.get(url, timeout=30)
    return resp.status_code, BeautifulSoup(resp.text, 'html.parser')

def extract(arxiv_id: str) -> Dict:
    status, soup = _get_html_soup(arxiv_id)
    if status != 200:
        return {"figs": [], "authors": [], "affils": []}

    figs = []
    for img, cap in zip(soup.select('.ltx_figure > img'),
                        soup.select('.ltx_figure > figcaption')):
        figs.append({
            "src": f"https://arxiv.org/html/{arxiv_id}/{img['src']}",
            "caption": cap.get_text(strip=True)
        })

    authors, affils = set(), set()
    section = soup.find('div', class_='ltx_authors')
    if section:
        for p in section.find_all('span', class_='ltx_personname'):
            for t in p.find_all(['sup', 'span']): t.decompose()
            authors.update([n.strip() for n in
                            p.get_text(" ", strip=True).replace(' and ', ',').split(',')
                            if n.strip()])
        for c in section.find_all('span', class_='ltx_contact'):
            txt = c.get_text(" ", strip=True)
            if '@' not in txt.lower():
                affils.add(txt)

    return {"figs": figs, "authors": sorted(authors), "affils": sorted(affils)}
