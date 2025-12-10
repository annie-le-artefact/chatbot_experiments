import os
import json
from langchain_google_genai import ChatGoogleGenerativeAI

# --- Configuration ---
PROCESSED_CONTENT_DIR = "data/crawled/processed/"
PROGRESS_FILE = "data/crawled/progress.json"
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY not found in environment variables. Please set it in your .env file.")

llm = ChatGoogleGenerativeAI(model="gemini-pro-latest", google_api_key=GEMINI_API_KEY, temperature=0.0)

# --- Functions ---

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

def translate_document(filepath, target_language="English"):
    """
    Reads a text file and translates its entire content using the LLM.
    """
    with open(filepath, 'r', encoding='utf-8') as f:
        text_dk = f.read()

    if not text_dk or not text_dk.strip():
        print(f"  - Skipping translation for empty file: {filepath}")
        return "", False

    print(f"  - Translating document ({len(text_dk)} characters)...")
    prompt = f"Translate the following Danish text to {target_language}. Do not add any commentary, preamble, or markdown formatting. Provide only the translated text directly:\n\n---\n{text_dk}\n---"
    
    try:
        response = llm.invoke(prompt)
        translated_text = response.content.strip()
        return translated_text, True
    except Exception as e:
        print(f"  [Translation Error] Could not translate document {filepath}. Error: {e}")
        return f"[Translation Failed] {text_dk}", False

def translate_all_processed_files(progress):
    """
    Orchestrates the translation of all new clean Danish text files.
    """
    print("Starting document-level translation with progress tracking...")
    
    for url, status in progress.items():
        if status.get("processed") and not status.get("translated"):
            filepath_dk = status.get("processed_filepath_dk")
            if filepath_dk and os.path.exists(filepath_dk):
                print(f"Processing for translation: {filepath_dk}")
                
                translated_text_en, success = translate_document(filepath_dk)
                
                if success and translated_text_en:
                    base_name = os.path.splitext(os.path.basename(filepath_dk))[0].replace('_dk', '')
                    output_filename = f"{base_name}_en.txt"
                    output_filepath = os.path.join(PROCESSED_CONTENT_DIR, output_filename)
                    
                    with open(output_filepath, 'w', encoding='utf-8') as f:
                        f.write(translated_text_en)
                    
                    # Update progress
                    status["translated"] = True
                    status["processed_filepath_en"] = output_filepath
                    save_progress(progress)
                    print(f"  - Saved translated text to: {output_filepath}")
            else:
                print(f"Skipping translation for {url} as file does not exist: {filepath_dk}")

    print("Translation complete.")

if __name__ == "__main__":
    progress_data = load_progress()
    translate_all_processed_files(progress_data)
