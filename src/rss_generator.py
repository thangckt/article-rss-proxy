from feedgen.feed import FeedGenerator
from typing import List, Dict
import pathlib, datetime as dt, logging

def _format_paper_entry(paper: Dict, with_translation: bool = False) -> str:
    """Format a single paper entry for the RSS feed description."""
    parts = [
        f"[{paper['title']}]({paper['link']})",
        ""
    ]
    
    if with_translation and "summary_ja" in paper:
        parts.append(paper["summary_ja"])
    else:
        parts.append(paper["summary"])
        
    parts.append("")
    return "\n".join(parts)

def _format_other_papers_description(papers: List[Dict]) -> str:
    """Format a description containing all non-filtered papers."""
    parts = []
    
    for p in papers:
        parts.append(_format_paper_entry(p, with_translation=False))
        parts.append("---")
        
    return "\n".join(parts)

def generate(filtered_papers: List[Dict], other_papers: List[Dict], path: str):
    fg = FeedGenerator()
    fg.id("https://example.com/arxiv_ai4sci_rss")
    fg.title("arXiv today filtered")
    fg.description("Daily filtered arXiv papers for AI4Science")
    fg.link(href="https://arxiv.org", rel="alternate")
    fg.language("ja")

    for p in filtered_papers:
        fe = fg.add_entry()
        fe.id(p["id"])
        fe.title(p["title"])
        fe.link(href=p["link"])
        fe.pubDate(p["updated"])
        fe.description(_format_paper_entry(p, with_translation=True))

    if other_papers:
        now = dt.datetime.now(dt.timezone.utc)
        fe = fg.add_entry()
        fe.id("other-papers-" + now.strftime("%Y-%m-%d"))
        fe.title(f"その他の論文 {now.strftime('%Y-%m-%d')}")
        fe.link(href="https://arxiv.org")
        fe.pubDate(now)
        fe.description(_format_other_papers_description(other_papers))

    out = pathlib.Path(path)
    out.parent.mkdir(parents=True, exist_ok=True)
    fg.rss_file(out)
    logging.info("RSS written to %s", out)
