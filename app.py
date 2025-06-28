from flask import Flask, request, jsonify
from quiz_generator import extract_text_from_pdf, generate_quiz_from_text
import requests  # We need to import requests here now
import traceback

app = Flask(__name__)


@app.route('/', methods=['GET'])
def health_check():
    return "Python backend is alive and running!"


# --- THIS IS OUR FINAL EXPERIMENT ---
# This endpoint will try to call a simple, public API that is NOT on Hugging Face.
@app.route('/test-internet', methods=['GET'])
def test_internet_access():
    try:
        print("--- /test-internet: Making request to public API (ipify.org)... ---", flush=True)
        # We will call a public API that just returns our server's IP address.
        response = requests.get('https://api.ipify.org?format=json', timeout=10)
        response.raise_for_status()  # Check for errors

        print("--- /test-internet: SUCCESS! Got response from public API. ---", flush=True)
        # If this works, we return the data from the public API.
        return jsonify(response.json())

    except Exception as e:
        print(f"--- /test-internet: CATASTROPHIC ERROR ---", flush=True)
        print(traceback.format_exc(), flush=True)
        return jsonify({"error": f"Failed to call public API: {str(e)}"}), 500


@app.route('/generate-quiz', methods=['POST'])
def handle_quiz_generation():
    # This is your original code
    # ...
    pass