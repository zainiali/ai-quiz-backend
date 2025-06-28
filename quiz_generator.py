import os
import requests
import fitz  # PyMuPDF
from dotenv import load_dotenv
import traceback

load_dotenv()

API_URL = "https://api-inference.huggingface.co/models/mistralai/Mistral-7B-Instruct-v0.2"
HF_API_TOKEN = os.getenv("HF_API_TOKEN")
headers = {"Authorization": f"Bearer {HF_API_TOKEN}"}


def extract_text_from_pdf(pdf_file_stream):
    print("--- extract_text_from_pdf: START ---", flush=True)
    try:
        # We explicitly load the library here to ensure it works.
        print("--- extract_text_from_pdf: Opening PDF with fitz... ---", flush=True)
        pdf_document = fitz.open(stream=pdf_file_stream, filetype="pdf")
        text = "".join(page.get_text() for page in pdf_document)
        print(f"--- extract_text_from_pdf: SUCCESS, extracted {len(text)} characters. ---", flush=True)
        return text
    except Exception as e:
        print("--- extract_text_from_pdf: CRITICAL ERROR ---", flush=True)
        print(traceback.format_exc(), flush=True)
        return None


def generate_quiz_from_text(text, num_questions=5):
    print("--- generate_quiz_from_text: START ---", flush=True)
    if not text: return None

    prompt = f'Based on the text below, generate a quiz with {num_questions} questions. Provide 4 options and the correct answer. Text: "{text[:2000]}" Quiz:'
    payload = {"inputs": prompt, "parameters": {"max_new_tokens": 1024}}  # Increased tokens for safety

    print("--- generate_quiz_from_text: Preparing to make API call... ---", flush=True)
    try:
        response = requests.post(API_URL, headers=headers, json=payload, timeout=100)  # Added explicit request timeout
        print(f"--- generate_quiz_from_text: API responded with status: {response.status_code} ---", flush=True)
        response.raise_for_status()

        generated_text = response.json()[0]['generated_text']
        print("--- generate_quiz_from_text: SUCCESS, got response from AI. ---", flush=True)
        return generated_text.split("Quiz:")[-1].strip()
    except Exception as e:
        print("--- generate_quiz_from_text: CRITICAL API ERROR ---", flush=True)
        print(traceback.format_exc(), flush=True)
        return None