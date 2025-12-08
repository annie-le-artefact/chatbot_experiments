import os
import json
from bs4 import BeautifulSoup
import re

STRUCTURED_CONTENT_DIR = "data/crawled/structured/"
PROCESSED_CONTENT_DIR = "data/crawled/processed/"
PROGRESS_FILE = "data/crawled/progress.json"
os.makedirs(PROCESSED_CONTENT_DIR, exist_ok=True)

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

def extract_clean_text_from_html(raw_html):
    """
    Extracts the main textual content from raw HTML, preserving line breaks.
    """
    soup = BeautifulSoup(raw_html, 'html.parser')
    
    content_area = soup.find(id='page') or soup.find('main') or soup.find('body') or soup

    for selector in ['nav', 'header', 'footer', 'aside', 'script', 'style', '.noprint']:
        for element in content_area.find_all(selector):
            element.extract()
            
    # Use '\n' to preserve line breaks, and strip extra whitespace from each line
    text = content_area.get_text(separator='\n', strip=True)
    return text

def process_all_structured_files(progress):
    """
    Orchestrates the processing of all new raw structured HTML files.
    """
    print("Starting HTML processing with progress tracking...")
    
    for url, status in progress.items():
        if status.get("crawled") and not status.get("processed"):
            filepath = status.get("structured_filepath")
            if filepath and os.path.exists(filepath):
                print(f"Processing: {filepath}")
                try:
                    with open(filepath, 'r', encoding='utf-8') as f:
                        structured_data = json.load(f)
                    
                    raw_html = structured_data["raw_html"]
                    clean_text_dk = extract_clean_text_from_html(raw_html)
                    
                    original_filename = os.path.basename(filepath)
                    base_name = os.path.splitext(original_filename)[0]
                    output_filename = f"{base_name}_dk.txt"
                    output_filepath = os.path.join(PROCESSED_CONTENT_DIR, output_filename)

                    with open(output_filepath, 'w', encoding='utf-8') as f:
                        f.write(clean_text_dk)
                    
                    # Update progress
                    status["processed"] = True
                    status["processed_filepath_dk"] = output_filepath
                    save_progress(progress)
                    print(f"  - Saved clean Danish text to: {output_filepath}")

                except Exception as e:
                    print(f"Error processing {filepath}: {e}")
            else:
                print(f"Skipping processing for {url} as file does not exist: {filepath}")

    print("Processing complete.")

if __name__ == "__main__":
    progress_data = load_progress()
    process_all_structured_files(progress_data)