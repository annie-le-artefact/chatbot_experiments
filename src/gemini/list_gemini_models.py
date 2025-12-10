import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

print("Available Gemini Models:")
for m in genai.list_models():
    print(f"  Name: {m.name}")
    print(f"  Display Name: {m.display_name}")
    print(f"  Supported Methods: {m.supported_generation_methods}")
    if "embedContent" in m.supported_generation_methods:
        print("  Supports Embedding: Yes")
    else:
        print("  Supports Embedding: No")
    print("  ---")
