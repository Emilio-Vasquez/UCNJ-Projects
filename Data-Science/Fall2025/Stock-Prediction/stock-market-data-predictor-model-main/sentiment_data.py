import os
import csv
import time
import re
import requests
from bs4 import BeautifulSoup
from datetime import datetime
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from urllib.parse import urljoin
from concurrent.futures import ThreadPoolExecutor, as_completed

# --------------------------
# CONFIG
# --------------------------
tickers = ["jpm", "meta", "msft", "nvda", "tsla", "tsm", "xom"]
output_dir = "sentiment_data"
os.makedirs(output_dir, exist_ok=True)

start_limit = datetime(2024, 1, 1)
headers = {"User-Agent": "Mozilla/5.0 (SentimentBot)"}
timeout = 12
max_pages_per_site = 20
max_threads = 10
crawl_depth = 1
ticker_time_limit = 5 * 60  # seconds per ticker

analyzer = SentimentIntensityAnalyzer()

company_map = {
    "aapl": ["apple", "iphone", "mac", "aapl"],
    "jpm": ["jpmorgan", "jpm", "chase"],
    "meta": ["meta", "facebook", "instagram", "whatsapp"],
    "msft": ["microsoft", "msft", "windows", "azure", "xbox"],
    "nvda": ["nvidia", "nvda", "gpu", "geforce"],
    "tsla": ["tesla", "tsla", "elon musk"],
    "tsm": ["tsmc", "tsm", "taiwan semiconductor"],
    "xom": ["exxon", "xom", "exxonmobil"],
}

search_sites = {
    "fox": "https://www.foxbusiness.com/search?q={q}&page={p}",
    "cnn": "https://www.cnn.com/search?q={q}&size=50&page={p}",
    "msnbc": "https://www.msnbc.com/search?q={q}&page={p}",
    "yahoo": "https://finance.yahoo.com/search/?q={q}&p={p}",
}


# --------------------------
# UTILS
# --------------------------
def safe_get(url):
    try:
        r = requests.get(url, headers=headers, timeout=timeout)
        return r.text if r.status_code == 200 else None
    except:
        return None


def normalize_date(text):
    if not text:
        return None
    patterns = ["%Y-%m-%d", "%Y/%m/%d", "%b %d, %Y", "%B %d, %Y"]
    for p in patterns:
        try:
            return datetime.strptime(text.strip(), p)
        except:
            continue
    m = re.search(r"(\d{4}-\d{2}-\d{2})", text)
    if m:
        try:
            return datetime.strptime(m.group(1), "%Y-%m-%d")
        except:
            return None
    return None


def extract_headline_and_date_from_article(url):
    html = safe_get(url)
    if not html:
        return None, None
    soup = BeautifulSoup(html, "html.parser")
    headline = None
    selectors = [
        "h1",
        "h1.story-title",
        "meta[property='og:title']",
        "meta[name='title']",
    ]
    for sel in selectors:
        tag = soup.select_one(sel)
        if tag:
            headline = (
                tag["content"] if tag.name == "meta" else tag.get_text(strip=True)
            )
            if headline:
                break
    meta_keys = [
        "article:published_time",
        "pubdate",
        "publish-date",
        "date",
        "article:modified_time",
    ]
    for m in soup.find_all("meta"):
        for key in meta_keys:
            if m.get("name") == key or m.get("property") == key:
                dt = normalize_date(m.get("content"))
                if dt:
                    return headline, dt
    for t in soup.find_all("time"):
        dt = t.get("datetime") or t.get_text()
        dt = normalize_date(dt)
        if dt:
            return headline, dt
    return headline, None


def relevance(ticker, txt):
    txt = txt.lower()
    for term in company_map[ticker]:
        if term in txt:
            return True
    if re.search(rf"\b{ticker}\b", txt, re.I):
        return True
    return False


def sentiment(text):
    if not text:
        return None
    score = analyzer.polarity_scores(text)["compound"]
    return round(score * 10, 2)


# --------------------------
# CRAWLER
# --------------------------
def crawl_links(seed_url, depth=1):
    if depth == 0:
        return []
    html = safe_get(seed_url)
    if not html:
        return []
    soup = BeautifulSoup(html, "html.parser")
    found = [urljoin(seed_url, a["href"]) for a in soup.find_all("a", href=True)]
    return list(set(found))


# --------------------------
# SEARCH SCRAPER
# --------------------------
def scrape_site_for_ticker(ticker, time_limit=ticker_time_limit):
    start_time = time.time()
    all_results = []

    for site, template in search_sites.items():
        print(f"  → {site.upper()} searching for {ticker}…")

        for p in range(1, max_pages_per_site + 1):
            if time.time() - start_time > time_limit:
                print(f"Time limit reached for {ticker}. Stopping search.")
                return all_results

            url = template.format(q=ticker, p=p)
            html = safe_get(url)
            if not html:
                break

            soup = BeautifulSoup(html, "html.parser")
            links = soup.find_all("a", href=True)

            items = [
                (a.get_text(strip=True), urljoin(url, a["href"]))
                for a in links
                if len(a.get_text(strip=True)) > 4
                and relevance(ticker, a.get_text(strip=True))
            ]

            if not items:
                break

            # Crawl depth=1 only
            all_links = []
            for _, l in items:
                all_links.extend(crawl_links(l, depth=1))
            all_links = list(set(all_links))

            # Multithread article extraction

            with ThreadPoolExecutor(max_threads) as ex:
                futures = {
                    ex.submit(extract_headline_and_date_from_article, l): l
                    for l in all_links
                }
                for fut in as_completed(futures):
                    url_link = futures[fut]
                    article_headline, dt = fut.result()
                    score = sentiment(article_headline)
                    if score is None or score == 0:
                        continue  # skip articles with no sentiment or neutral sentiment
                    final_headline = article_headline or os.path.basename(url_link)
                    if dt is None:
                        dt = datetime.now()
                    if dt < start_limit:
                        continue
                    print(f"[{ticker}] {url_link} → {score}")
                    all_results.append((dt, final_headline, site, score))

    return all_results


# --------------------------
# MAIN
# --------------------------
def run():
    for tkr in tickers:
        print(f"\n===== {tkr.upper()} =====")
        results = scrape_site_for_ticker(tkr)

        # aggregate per day
        daily = {}
        for dt, txt, src, score in results:
            day = dt.strftime("%Y-%m-%d")
            daily.setdefault(day, []).append(score)

        # average multiple scores per day
        daily_avg = {d: round(sum(v) / len(v), 2) for d, v in daily.items() if v}

        # per-year CSV
        per_year = {}
        for d, s in daily_avg.items():
            y = d[:4]
            per_year.setdefault(y, []).append((d, s))

        for y, rows in per_year.items():
            path = f"{output_dir}/{tkr}_{y}.csv"
            with open(path, "w", newline="", encoding="utf-8") as f:
                w = csv.writer(f)
                w.writerow(["date", "sentiment"])
                for r in sorted(rows):
                    w.writerow(r)
            print(f"saved → {path}")


if __name__ == "__main__":
    run()
