import os
import json
from flask import Flask, request, jsonify
from flask_cors import CORS
from transformers import pipeline, set_seed
from difflib import SequenceMatcher  # New import for string similarity


# IMPORTANT: You need to install the following libraries first:
# pip install Flask transformers torch flask-cors sentence-transformers

# --- 1. Load the knowledge base ---
def load_faqs_from_json(file_path: str) -> list:
    """Loads FAQs from a JSON file."""
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"Error: The file {file_path} was not found.")
        return []
    except json.JSONDecodeError:
        print(f"Error: Could not decode JSON from {file_path}.")
        return []


# Load the FAQ data once when the app starts
base_dir = os.path.dirname(__file__)
faqs_path = os.path.join(base_dir, "faqs.json")
faqs_data = load_faqs_from_json(faqs_path)

# Create a simple, clear string of your FAQs to include in the prompt
faqs_str = "\n".join([f"Q: {item['question']}\nA: {item['answer']}\n" for item in faqs_data])

# --- 2. Initialize the AI Model and Similarity Function ---
try:
    print("Loading AI model...")
    model_name = "google/flan-t5-small"
    text_generator = pipeline("text2text-generation", model=model_name)
    print("AI model loaded successfully!")
except Exception as e:
    print(f"Error loading AI model: {e}")
    text_generator = None


def get_similarity_score(a: str, b: str) -> float:
    """Calculates a similarity score between two strings."""
    # We'll normalize the strings to ignore case and punctuation
    norm_a = "".join(filter(str.isalnum, a.lower()))
    norm_b = "".join(filter(str.isalnum, b.lower()))
    return SequenceMatcher(None, norm_a, norm_b).ratio()


# --- 3. Create the Flask App ---
app = Flask(__name__)
CORS(app)  # Enable CORS for all routes on the app


@app.route("/ask", methods=["POST"])
def ask():
    """
    Endpoint for asking the bot a question.
    It expects a JSON payload with a 'question' key.
    """
    data = request.get_json()
    user_q = data.get("question")

    if not user_q:
        return jsonify({"answer": "Error: Please provide a 'question' in the request body."}), 400

    # First, try to find a direct match using string similarity
    for item in faqs_data:
        score = get_similarity_score(user_q, item['question'])
        if score > 0.8:  # We'll set a high threshold for a direct match
            return jsonify({"answer": item['answer']})

    # If no direct match is found, use the AI model
    if not text_generator:
        return jsonify({"answer": "Error: AI model failed to load."}), 500

    prompt = f"""
Given the following FAQs, answer the user's question. If the answer is not in the FAQs, respond with "I'm not sure yet. Please try rephrasing your question or contact support.".
FAQs:
{faqs_str}
Question: {user_q}
Answer:"""

    try:
        # Generate a response using the new model
        set_seed(42)
        generated_text = text_generator(prompt, max_length=150, min_length=10, do_sample=False)
        answer = generated_text[0]['generated_text']

        return jsonify({"answer": answer})

    except Exception as e:
        return jsonify({"answer": f"An error occurred while processing your request: {e}"}), 500


if __name__ == "__main__":
    if faqs_data:
        print("Starting the FAQ bot web service...")
        print(
            "To run, open your terminal and run this file. The service will be available at http://127.0.0.1:5000/ask")
        print("You can send a POST request to this URL with a JSON body like: {\"question\": \"What are your hours?\"}")
        app.run(debug=True)
    else:
        print("Web service cannot start due to an error loading FAQs.")
