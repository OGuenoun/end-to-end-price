import time
import csv
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup

BASE = "https://books.toscrape.com/"
HEADERS = {"User-Agent": "Mozilla/5.0 "}

def get_categories():
    soup = get_soup(BASE)
    cats = []
    # side category class , access to href, and get name of category
    for a in soup.select(".side_categories ul a"): # skip ul and a
        href = a.get("href", "")
        if "catalogue/category" in href:
            cats.append((a.get_text(strip=True), urljoin(BASE, href)))
    return cats

def get_soup(url: str) :
    r = requests.get(url, headers=HEADERS, timeout=20)
    r.raise_for_status() # Check error 
    return BeautifulSoup(r.text, "html.parser")

def parse_price(text: str):
    digits = "".join(ch for ch in text if ch.isdigit() or ch == ".") # Use regexp next
    return float(digits) if digits else None

def parse_rating(star_div) :
    if not star_div:
        return None
    names = star_div.get("class", [])
    mapping = {"One":1, "Two":2, "Three":3, "Four":4, "Five":5}
    for k, v in mapping.items():
        if k in names:
            return v
    return None

def scrape_category(cat_name: str, cat_url: str):
    rows = []
    url = cat_url
    while url:
        soup = get_soup(url)
        for li in soup.select("ol.row li"): #same for categories 
            a = li.select_one("h3 a")   
            title = a.get("title", "").strip()
            rel_link = a.get("href", "")
            detail_url = urljoin(urljoin(BASE, "catalogue/"), rel_link)

            price_el = li.select_one(".price_color")
            price = parse_price(price_el.get_text(strip=True)) if price_el else None

            rating = parse_rating(li.select_one(".star-rating"))

            availability = li.select_one(".availability").get_text(strip=True)

            rows.append({
                "category": cat_name,
                "title": title,
                "price": price,
                "rating": rating,
                "availability": availability,
                "detail_url": detail_url
            })

        # pagination: look for "li.next a"
        next_a = soup.select_one("li.next a")
        url = urljoin(url, next_a.get("href")) if next_a else None

        time.sleep(0.3)  # be polite
    return rows



def main():
    print("Scraping categories")
    categories = get_categories()
    print(f"Found {len(categories)} categories")

    all_rows: list[dict] = []
    for name, url in categories:
        print(f"{name}")
        all_rows.extend(scrape_category(name, url))

    out_path = "./data/books_simple.csv"
    fieldnames = ["category", "title", "price", "rating", "availability", "detail_url"]
    with open(out_path, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fieldnames)
        w.writeheader()
        w.writerows(all_rows)

    print(f"Saved {len(all_rows)} rows → {out_path}")

if __name__ == "__main__":
    main()