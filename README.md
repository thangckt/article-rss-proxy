# article-rss-proxy

A tool that fetches papers from arXiv, filters and translates them using Gemini, and delivers them as an RSS feed.

## Features

- Fetches papers from specific categories via the arXiv API
- Filters papers using the Gemini API to include only those of interest
- Translates English abstracts into Japanese
- Retrieves figures, authors, and affiliation information
- Publishes as an RSS feed via GitHub Pages
- Automatically updates daily at 7:00 KST via GitHub Actions

## Setup

```bash
# Set up the environment
uv sync

# Configure environment variables
# Copy .env.example to .env and set GEMINI_API_KEY
cp .env.example .env
# Then edit the .env file to set your API key
```

## Usage

```bash
# Generate the RSS feed
uv run src/main.py
# This will generate docs/index.xml
```

## Publishing via GitHub Pages

1. Create a `gh-pages` branch

2. In your repository, go to `Settings` > `Pages` and set:
- Source: Deploy from a branch
- Branch: `gh-pages`
- Folder: `/docs`

3. After setting it up, the RSS feed will be available at:
`https://<user>.github.io/article-rss-proxy/index.xml`

## Automatic Updates

By default, GitHub Actions automatically updates the feed daily at 11:17 JST (02:17 UTC).
Adjust the schedule or filtering criteria in .github/workflows/arxiv_rss.yml if needed.
