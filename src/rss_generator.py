from feedgen.feed import FeedGenerator
from typing import List, Dict
import datetime as dt, logging
from pathlib import Path
from zoneinfo import ZoneInfo


def generate(filtered_papers: List[Dict], other_papers: List[Dict], xml_path: Path):
    fg = FeedGenerator()
    fg.id("https://<user>.github.io/article-rss-proxy")
    fg.title("今日のarXiv-AI4Science")
    fg.link(href="https://<user>.github.io/article-rss-proxy", rel="alternate")
    fg.description("今日のarXiv-AI4Science")
    fg.language("ja")

    for p in filtered_papers:
        fe = fg.add_entry()
        fe.id(p["id"])
        fe.title(p["title"])
        fe.link(href=p["link"])
        fe.pubDate(p["updated"])
        fe.description(
            p.get("summary_ja", p["summary"])
            + "\n\n" + f'<img src="{p["fig1"]}"/>'
            + "\n\n" + ", ".join(p["authors"])
            + "\n\n" + "\n".join(p["affils"])
        )

    if other_papers:
        today = dt.datetime.utcnow().astimezone(ZoneInfo("Asia/Tokyo"))
        fe = fg.add_entry()
        fe.id("other-papers")
        fe.title(f"other arxiv papers {today.strftime('%Y-%m-%d')}")
        fe.link(href="https://arxiv.org")
        fe.pubDate(today)
        fe.description(
            "\n\n".join(
                [f"- [{p['title']}]({p['link']})" for p in other_papers]
            )
        )

    fg.rss_file(xml_path)
    logging.info("RSS written to %s", xml_path)
