import json
import os
import re
import asyncio
from urllib.parse import urlparse
from playwright.async_api import async_playwright

STRUCTURED_CONTENT_DIR = "data/crawled/structured/"
PROGRESS_FILE = "data/crawled/progress.json"
os.makedirs(STRUCTURED_CONTENT_DIR, exist_ok=True)

def load_progress():
    """Loads the progress tracking file."""
    if os.path.exists(PROGRESS_FILE):
        with open(PROGRESS_FILE, 'r') as f:
            return json.load(f)
    return {}

def save_progress(progress):
    """Saves the progress tracking file."""
    with open(PROGRESS_FILE, 'w') as f:
        json.dump(progress, f, indent=2)

def load_data_sources(file_path="data/data_sources.json"):
    """Loads the data sources from the specified JSON file."""
    with open(file_path, 'r') as f:
        return json.load(f)

def infer_metadata_from_source(url, source_details):
    """Infers metadata from the URL and the source configuration."""
    metadata = {
        "jurisdiction": "DK",
        "doc_type": source_details.get("type", "unknown"),
        "source": urlparse(url).netloc
    }
    
    if "retsinformation.dk" in url:
        match = re.search(r'/lta/(\d{4})/', url)
        if match:
            metadata["year"] = int(match.group(1))

    return metadata

def generate_filename(url, metadata):
    """Generates a descriptive filename from the URL and metadata."""
    doc_type = metadata.get("doc_type", "doc")
    year = metadata.get("year", "YYYY")
    
    path_parts = urlparse(url).path.strip('/').split('/')
    doc_id = path_parts[-1] if path_parts else "index"
    
    return f"DK-{doc_type.upper()}-{year}-{doc_id}.json"

async def crawl_with_playwright(url):
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()
        try:
            await page.goto(url, wait_until='domcontentloaded')
            await page.wait_for_timeout(3000)
            content = await page.content()
            return content
        except Exception as e:
            print(f"  [Playwright Error] Could not fetch {url}: {e}")
            return None
        finally:
            await browser.close()

async def crawl_and_structure_urls(data_sources, progress):
    """
    Fetches fully rendered HTML for new URLs and updates the progress file.
    """
    print("Starting metadata-aware web crawling with progress tracking...")
    
    for domain, details in data_sources.items():
        if "pages" in details:
            for page_entry in details["pages"]:
                url = page_entry["url"]
                if progress.get(url, {}).get("crawled"):
                    print(f"Skipping already crawled URL: {url}")
                    continue

                try:
                    print(f"Fetching: {url}")
                    metadata = infer_metadata_from_source(url, details)
                    raw_html_content = await crawl_with_playwright(url)
                    
                    if raw_html_content:
                        filename = generate_filename(url, metadata)
                        filepath = os.path.join(STRUCTURED_CONTENT_DIR, filename)
                        
                        structured_data = {
                            "source_url": url,
                            "metadata": metadata,
                            "raw_html": raw_html_content
                        }
                        
                        with open(filepath, 'w', encoding='utf-8') as f:
                            json.dump(structured_data, f, indent=2, ensure_ascii=False)
                        print(f"Saved structured data to: {filepath}")

                        # Update progress
                        if url not in progress:
                            progress[url] = {}
                        progress[url]["crawled"] = True
                        progress[url]["structured_filepath"] = filepath
                        save_progress(progress)
                    else:
                        print(f"Skipping {url} due to fetch error.")

                except Exception as e:
                    print(f"An unexpected error occurred for {url}: {e}")
    
    print("Web crawling complete.")

if __name__ == "__main__":
    progress_data = load_progress()
    sources = load_data_sources()
    asyncio.run(crawl_and_structure_urls(sources, progress_data))