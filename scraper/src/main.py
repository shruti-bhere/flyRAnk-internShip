import os
import re
import json
import time
import html
from datetime import datetime, timezone
from urllib.parse import urljoin
import requests
from bs4 import BeautifulSoup
from pydantic import BaseModel, HttpUrl, Field
from typing import Optional

BASE_URL = "https://books.toscrape.com/"
START_URL = "https://books.toscrape.com/catalogue/page-1.html"
USER_AGENT = "FlyRankInternshipA9/1.0 (+https://github.com/shruti-bhere/scraper)"
TIMEOUT = 10
DELAY = 0.5  # Polite delay between network requests

# Ensure output & cache directories exist
os.makedirs("cache", exist_ok=True)
os.makedirs("output", exist_ok=True)

# Pydantic Schema Definition for Book Record Validation
class BookSchema(BaseModel):
    title: str
    product_url: HttpUrl
    price_text: str
    price_gbp: float = Field(..., ge=0)
    availability_text: str
    rating_text: str
    description: Optional[str] = None
    source_page: HttpUrl
    fetched_at: str

def fetch_page(url: str, cache_filename: str, metrics: dict) -> str:
    """Fetch HTML with polite headers, forced UTF-8 encoding, caching, and retry logic."""
    cache_path = os.path.join("cache", cache_filename)
    if os.path.exists(cache_path):
        metrics["cache_hits"] += 1
        print(f"CACHE HIT: {cache_filename}")
        with open(cache_path, "r", encoding="utf-8") as f:
            return f.read()

    metrics["pages_fetched"] += 1
    print(f"FETCH: {url}")
    headers = {"User-Agent": USER_AGENT}
    
    # Retry mechanism for temporary server or network issues
    for attempt in range(2):
        try:
            response = requests.get(url, headers=headers, timeout=TIMEOUT)
            if response.status_code == 200:
                # Force UTF-8 encoding to prevent character corruption
                response.encoding = 'utf-8'
                with open(cache_path, "w", encoding="utf-8") as f:
                    f.write(response.text)
                time.sleep(DELAY)
                return response.text
            elif response.status_code in [404, 403]:
                break  # Stop retry for 404/403
        except requests.RequestException:
            if attempt == 1:
                raise
            time.sleep(1)
            
    raise Exception(f"Failed to fetch {url}")

def run_scraper():
    """Execute 7-stage polite web scraper."""
    start_time = datetime.now(timezone.utc)
    metrics = {
        "pages_fetched": 0,
        "cache_hits": 0,
        "valid_records": 0,
        "invalid_records": 0,
        "failed_pages": 0
    }
    
    discovered_urls = []
    current_page_url = START_URL
    pages_crawled = 0

    # Stage 2: Discover first 3 catalogue pages
    while current_page_url and pages_crawled < 3:
        pages_crawled += 1
        cache_file = f"catalogue-page-{pages_crawled}.html"
        try:
            html_content = fetch_page(current_page_url, cache_file, metrics)
            soup = BeautifulSoup(html_content, "html.parser")
            
            for h3 in soup.select("article.product_pod h3 a"):
                rel_url = h3.get("href")
                abs_url = urljoin(current_page_url, rel_url)
                if abs_url not in discovered_urls:
                    discovered_urls.append(abs_url)
            
            next_a = soup.select_one("li.next a")
            if next_a:
                current_page_url = urljoin(current_page_url, next_a.get("href"))
            else:
                current_page_url = None
        except Exception as e:
            print(f"Catalogue Fetch Failed: {e}")
            metrics["failed_pages"] += 1
            break

    print(f"catalogue_pages={pages_crawled}, discovered={len(discovered_urls)}, unique_urls={len(discovered_urls)}")

    validated_books = []
    errors = []

    # Stage 3 & 4: Extract and Validate Records
    for book_url in discovered_urls:
        clean_filename = re.sub(r'[^a-zA-Z0-9]', '_', book_url) + ".html"
        try:
            html_content = fetch_page(book_url, clean_filename, metrics)
            soup = BeautifulSoup(html_content, "html.parser")
            
            # Clean and unescape textual HTML entities
            title = html.unescape(soup.select_one("div.product_main h1").text.strip())
            price_text = html.unescape(soup.select_one("p.price_color").text.strip())
            
            # Extract clean float value for GBP price
            price_match = re.search(r"[\d\.]+", price_text)
            price_gbp = float(price_match.group(0)) if price_match else 0.0

            raw_avail = soup.select_one("p.instock.availability").text.strip()
            availability_text = re.sub(r'\s+', ' ', html.unescape(raw_avail))
            
            rating_cls = soup.select_one("p.star-rating")["class"]
            rating_text = [c for c in rating_cls if c != "star-rating"][0]
            
            desc_el = soup.select_one("#product_description ~ p")
            description = html.unescape(desc_el.text.strip()) if desc_el else None

            raw_record = {
                "title": title,
                "product_url": book_url,
                "price_text": price_text,
                "price_gbp": price_gbp,
                "availability_text": availability_text,
                "rating_text": rating_text,
                "description": description,
                "source_page": book_url,
                "fetched_at": datetime.now(timezone.utc).isoformat()
            }

            # Pydantic validation
            validated_obj = BookSchema(**raw_record)
            validated_books.append(json.loads(validated_obj.model_dump_json()))
            metrics["valid_records"] += 1

        except Exception as e:
            metrics["invalid_records"] += 1
            metrics["failed_pages"] += 1
            errors.append({"url": book_url, "error": str(e)})

    # Deduplicate records by canonical product_url
    unique_books_map = {b["product_url"]: b for b in validated_books}
    final_books = list(unique_books_map.values())

    # Write cleaned JSON results with UTF-8 encoding
    with open("output/books.json", "w", encoding="utf-8") as f:
        json.dump(final_books, f, indent=2, ensure_ascii=False)
        
    with open("output/errors.json", "w", encoding="utf-8") as f:
        json.dump(errors, f, indent=2, ensure_ascii=False)

    end_time = datetime.now(timezone.utc)
    report = {
        "start_time": start_time.isoformat(),
        "duration_seconds": round((end_time - start_time).total_seconds(), 2),
        "pages_fetched": metrics["pages_fetched"],
        "cache_hits": metrics["cache_hits"],
        "valid_records": len(final_books),
        "invalid_records": metrics["invalid_records"],
        "failed_pages": metrics["failed_pages"]
    }

    with open("output/run-report.json", "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2)

    print("Pipeline Execution Completed. Results written to output/")

if __name__ == "__main__":
    run_scraper()