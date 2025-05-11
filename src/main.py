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
    
    filtered = []
    others = []
    
    for p in raw:
        if is_relevant(p):
            filtered.append(p)
            p["summary_ja"] = translate_abstract(p)
            extra = extract(p["id"])
            p["authors"] = extra["authors"] or p["authors"]
            p["affils"] = extra["affils"]
            p["figs"] = extra["figs"]
        else:
            others.append(p)
            
    logging.info("Papers after filter: %s filtered, %s others", len(filtered), len(others))
    
    generate(filtered, others, OUTPUT)

if __name__ == "__main__":
    main()
