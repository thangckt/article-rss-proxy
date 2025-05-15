from datetime import datetime
from zoneinfo import ZoneInfo

# for rss gen
TODAY_JST = datetime.now(ZoneInfo("Asia/Tokyo"))
DEPLOY_URL = "https://hommage-ebi.github.io/article-rss-proxy/"

# for arxiv fetch
CATEGORIES = [
    "cond-mat.mtrl-sci", "physics.chem-ph", "physics.comp-ph",
    "cs.AI", "cs.LG", "cs.CL"
]

# for llm
INTERESTS = """\
- DFT・MD・MCなどの計算化学手法を機械学習で高速化する研究
- DFTの精度限界を超えるための新しい計算手法・機械学習手法の開発
- 機械学習ポテンシャルを活用して材料の現象開明や探索を行う研究(この項目に関しては、機械学習ポテンシャルが関わらないものには興味がない)
- 計算化学手法を活用して半導体デバイス中の材料の現象開明や探索を行う研究
- 固相・液相・気相を問わず、合成可能性・合成レシピを計算化学で設計・予測する研究
- LLMの材料研究への活用
- LLMを用いた研究の自動化(アイデア生成・文献調査・コーディングエージェントなど)\
"""

BATCH_SIZE = 25
MAX_NJOBS = 8
