from feedgen.feed import FeedGenerator
from typing import List, Dict
import pathlib, datetime as dt, logging

def _format_description(paper: Dict) -> str:
    parts = [
        paper["title"],
        "",
        paper["summary_ja"],
        ""
    ]
    if paper["figs"]:
        fig = paper["figs"][0]
        parts.extend([f'<img src="{fig["src"]}" alt="Figure 1" />', "", fig["caption"], ""])
    parts.append("著者: " + ", ".join(paper["authors"]))
    parts.append("所属: " + ", ".join(paper["affils"]))
    return "\n".join(parts)

def generate(papers: List[Dict], path: str):
    fg = FeedGenerator()
    fg.id("https://example.com/arxiv_ai4sci_rss")
    fg.title("Daily arXiv AI4Science (JST)")
    fg.link(href="https://arxiv.org", rel="alternate")
    fg.language("ja")

    for p in papers:
        fe = fg.add_entry()
        fe.id(p["id"])
        fe.title(p["title"])
        fe.link(href=p["link"])
        fe.pubDate(p["updated"])
        fe.description(_format_description(p))

    out = pathlib.Path(path)
    out.parent.mkdir(parents=True, exist_ok=True)
    fg.rss_file(out)
    logging.info("RSS written to %s", out)
