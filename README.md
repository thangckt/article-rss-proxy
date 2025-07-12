# article-rss-proxy

arXivの論文を取得し、Geminiでフィルタリング・翻訳した上でRSS フィードとして配信するツールです。

## 特徴

- arXiv APIから指定カテゴリの論文を取得
- Gemini APIを使用して興味のある論文のみにフィルタリング
- 英語のAbstractを日本語に翻訳
- 論文の図・著者・所属情報を取得
- RSSフィードとして配信（GitHub Pages）
- GitHub Actionsによる自動更（毎日11:17JST）

## セットアップ

```bash
# 環境構築
uv sync

# 環境変数の設定
# .env.example をコピーして .env を作成し、GEMINI_API_KEY を設定
cp .env.example .env
# .env ファイルを編集して API キーを設定
```

## 使用方法

```bash
# RSS フィードの生成
uv run src/main.py
# docs/index.xml が生成されます
```

## GitHub Pages での配信

1. gh-pagesブランチを作成

2. リポジトリの Settings > Pages で以下を設定:
   - Source: Deploy from a branch
   - Branch: gh-pages
   - Folder: /docs

3. 設定後、RSS フィードは以下の URL で配信されます:
   `https://<user>.github.io/article-rss-proxy/index.xml`

## 自動更新

デフォルトでは GitHub Actions により毎日 11:17 JST (02:17 UTC) に自動更新されます。
必要に応じて `.github/workflows/arxiv_rss.yml` のスケジュールやフィルタ条件を調整してください。
