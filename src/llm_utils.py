import logging, os, textwrap
from typing import Dict
from google import genai
from dotenv import load_dotenv

load_dotenv()
_client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])

_SYSTEM_PROMPT = textwrap.dedent("""
あなたは優秀な科学編集者です。次の条件にマッチする論文を「興味あり: yes/no」で答えてください。
条件: AI4Science — 物理・化学・材料科学と機械学習や大規模言語モデルの融合研究
""").strip()

def _gemini(prompt: str) -> str:
    res = _client.models.generate_content(
        model="gemini-2.0-flash",
        contents=prompt
    )
    return res.text.strip()

def is_relevant(paper: Dict) -> bool:
    q = f"{_SYSTEM_PROMPT}\n---\nタイトル: {paper['title']}\n概要: {paper['summary']}\n---\n興味あり:"
    ans = _gemini(q).lower()
    logging.debug("Filter result for %s: %s", paper['id'], ans)
    return "yes" in ans

def translate_abstract(paper: Dict) -> str:
    prompt = (f"以下の英語 Abstract を日本語に翻訳してください。\n"
              f"---\n{paper['summary']}\n---")
    return _gemini(prompt)
