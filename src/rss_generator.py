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

def _format_feed_description(filtered_papers: List[Dict], other_papers: List[Dict]) -> str:
    """Format the entire feed description with all papers."""
    parts = ["## AI4Science に関連する論文", ""]
    
    for p in filtered_papers:
        parts.append(_format_paper_entry(p, with_translation=True))
        parts.append("---")
        
    parts.append("")
    parts.append("## その他の論文", "")
    
    for p in other_papers:
        parts.append(_format_paper_entry(p, with_translation=False))
        parts.append("---")
        
    return "\n".join(parts)

def generate(filtered_papers: List[Dict], other_papers: List[Dict], path: str):
    fg = FeedGenerator()
    fg.id("https://example.com/arxiv_ai4sci_rss")
    fg.title("arXiv today filtered")
    fg.link(href="https://arxiv.org", rel="alternate")
    fg.language("ja")

    fe = fg.add_entry()
    fe.id("daily-arxiv-" + dt.datetime.now().strftime("%Y-%m-%d"))
    fe.title(f"arXiv 論文リスト {dt.datetime.now().strftime('%Y-%m-%d')}")
    fe.link(href="https://arxiv.org")
    fe.pubDate(dt.datetime.now())
    fe.description(_format_feed_description(filtered_papers, other_papers))

    out = pathlib.Path(path)
    out.parent.mkdir(parents=True, exist_ok=True)
    fg.rss_file(out)
    logging.info("RSS written to %s", out)
