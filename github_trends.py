import os
import json
import time
import requests
from bs4 import BeautifulSoup
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

GROQ_API_KEY = os.environ.get("GROQ_API_KEY")
if not GROQ_API_KEY:
    raise EnvironmentError("GROQ_API_KEY not found. Add it to your .env file.")

client = Groq(api_key=GROQ_API_KEY)

# Number of repos to fetch
TOP_N = 10

def scrape_github_trending():
    # Scrape GitHub trending page
    url = "https://github.com/trending?since=weekly"
    headers = {"User-Agent": "Mozilla/5.0"}

    print("Fetching GitHub trending page...")
    response = requests.get(url, headers=headers, timeout=10)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")

    # Try main selector, fallback if structure changes
    repo_cards = soup.select("article.Box-row")
    if not repo_cards:
        repo_cards = soup.select("div[data-hpc] article")

    repo_cards = repo_cards[:TOP_N]

    repos = []
    for card in repo_cards:
        # Extract repo name
        name_tag = card.select_one("h2 a")
        full_name = name_tag["href"].strip("/") if name_tag else "N/A"

        # Extract description
        desc_tag = card.select_one("p")
        description = desc_tag.get_text(strip=True) if desc_tag else "No description"

        # Extract language
        lang_tag = card.select_one('[itemprop="programmingLanguage"]')
        language = lang_tag.get_text(strip=True) if lang_tag else "Unknown"

        # Extract stars
        stars_tag = card.select_one('a[href$="/stargazers"]')
        stars = stars_tag.get_text(strip=True) if stars_tag else "N/A"

        # Extract stars today
        today_tag = card.select_one("span.d-inline-block.float-sm-right")
        stars_today = today_tag.get_text(strip=True) if today_tag else "N/A"

        repos.append({
            "name": full_name,
            "description": description,
            "language": language,
            "stars": stars,
            "stars_today": stars_today,
        })

    print(f"Scraped {len(repos)} repos.\n")
    return repos

def generate_summary(repo: dict) -> str:
    # Create prompt for LLM
    prompt = (
        f"Repo: {repo['name']}\n"
        f"Description: {repo['description']}\n"
        f"Language: {repo['language']}\n\n"
        "Write a 2-line plain-English summary of what this repo does and why developers might find it useful."
    )

    try:
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {"role": "system", "content": "You summarize GitHub repos briefly and clearly."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=100,
            temperature=0.5,
        )
        return response.choices[0].message.content.strip()
    except Exception:
        return "Summary unavailable."

def print_results(repos: list):
    # Print formatted output
    print("=" * 70)
    print(f"{'GitHub Trending Repos — Today':^70}")
    print("=" * 70)

    for i, repo in enumerate(repos, start=1):
        print(f"\n#{i}  {repo['name']}")
        print(f" Stars: {repo['stars']}  |  Today: {repo['stars_today']}  |  Lang: {repo['language']}")
        print(f" {repo['description']}")
        print(f" AI Summary: {repo['ai_summary']}")
        print("-" * 70)

def main():
    # Scrape data
    repos = scrape_github_trending()

    # Generate summaries
    print("Generating AI summaries via Groq...\n")
    for repo in repos:
        print(f"  Summarizing: {repo['name']}...")
        repo["ai_summary"] = generate_summary(repo)
        time.sleep(0.5)  # prevent rate limiting

    # Display results
    print_results(repos)

    # Save to JSON
    with open("trending_results.json", "w", encoding="utf-8") as f:
        json.dump(repos, f, indent=2, ensure_ascii=False)

    print("\nResults saved to trending_results.json")

if __name__ == "__main__":
    main()