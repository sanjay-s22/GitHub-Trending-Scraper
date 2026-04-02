# GitHub Trending Scraper with AI Summaries

A Python script that scrapes the top 10 repositories from [GitHub Trending](https://github.com/trending) and uses **Groq API (llama-3.1-8b-instant)** to generate a simple-English 2-line summary for each repo. Results are printed to the console and saved to a JSON file.

---

## What the script does

1. Fetches the GitHub Trending page and extracts the top 10 repos
2. For each repo, collects the name, description, language, total stars, and stars today
3. Calls the Groq API to generate a short AI summary per repo
4. Prints a formatted table to the console
5. Saves all results to `trending_results.json`

---

## Installation

**Clone the repo and set up a virtual environment:**

```bash
git clone https://github.com/sanjay-s22/Github-Trending-Scraper.git
cd Github-Trending-Scraper
python -m venv venv
venv\Scripts\activate  # Windows
# source venv/bin/activate  # Mac/Linux
```

**Install dependencies:**

```bash
pip install -r requirements.txt
```

---

## Setting up the API key

Get your free Groq API key from [console.groq.com](https://console.groq.com).

Create a `.env` file in the project root:

```
GROQ_API_KEY=your_key_here
```

The script loads it automatically via `python-dotenv`. Never commit your `.env` file — it's already in `.gitignore`.

---

## Usage

```bash
python github_trends.py
```

---

## Example output

```
======================================================================
                  GitHub Trending Repos — Today
======================================================================

#1  obra/superpowers
    Stars: 91,649  |  Today: 3,050 stars today  |  Lang: Shell
    An agentic skills framework & software development methodology that works.
    AI Summary: The obra/superpowers repo provides a framework and methodology
    for software development that focuses on empowering teams to work effectively.
    Developers might find it useful for streamlining their workflow and improving
    collaboration.
----------------------------------------------------------------------

#2  codecrafters-io/build-your-own-x
    Stars: 479,587  |  Today: 2,011 stars today  |  Lang: Markdown
    Master programming by recreating your favorite technologies from scratch.
    AI Summary: This repository provides a collection of projects that allow
    developers to recreate popular technologies from scratch, helping them master
    programming skills.
----------------------------------------------------------------------
```

Results are also saved to `trending_results.json`.

---

## Project structure

```
Github-Trending-Scraper/
├── github_trends.py       # Main scraper + AI summary script
├── requirements.txt       # Python dependencies
├── .env                   # API key (gitignored)
├── .gitignore
└── README.md
```

---

## Tech stack

- **Python 3.12**
- **BeautifulSoup4** — HTML parsing
- **Groq API** — AI summaries via llama-3.1-8b-instant
- **python-dotenv** — environment variable management
