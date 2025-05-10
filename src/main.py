import logging, os
from dotenv import load_dotenv

from arxiv_fetcher import fetch_new_papers
from llm_utils      import is_relevant, translate_abstract
from html_parser    import extract
from rss_generator  import generate

logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s %(levelname)s %(message)s")

load_dotenv()
OUTPUT = os.getenv("RSS_OUTPUT_PATH", "docs/index.xml")

def main():
    raw = fetch_new_papers()
    logging.info("Filtering with Gemini …")
    filtered = [p for p in raw if is_relevant(p)]
    logging.info("Remaining after filter: %s", len(filtered))

    for p in filtered:
        p["summary_ja"] = translate_abstract(p)
        extra = extract(p["id"])
        p["authors"] = extra["authors"] or p["authors"]
        p["affils"]  = extra["affils"]
        p["figs"]    = extra["figs"]

    generate(filtered, OUTPUT)

if __name__ == "__main__":
    main()
