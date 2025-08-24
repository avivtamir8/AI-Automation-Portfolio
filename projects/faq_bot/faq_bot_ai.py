import json
import os
import sys
from sentence_transformers import SentenceTransformer, util

# --- 1. Load FAQs ---
# A function to load the questions and answers from a JSON file.
# This function is the same as the original, as it's a good approach.
def load_faqs_from_json(file_path):
    """
    Loads FAQs from a JSON file.

    Args:
        file_path (str): The path to the JSON file.

    Returns:
        list: A list of dictionaries, where each dictionary represents an FAQ.
    """
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"Error: The file at {file_path} was not found.")
        return []

# --- 2. Initialize the AI Model ---
# This part is new. We'll use a pre-trained model for sentence embeddings.
# This allows the bot to understand the meaning of a sentence, not just the words.
# We're using a small, efficient model that works well offline.
# The model will download the first time the script is run.
print("Initializing AI model... (This may take a moment the first time)")
try:
    model = SentenceTransformer('all-MiniLM-L6-v2')
    print("Model loaded successfully!")
except Exception as e:
    print(f"Error loading model: {e}")
    print("This might be due to a network issue. Please check your connection and try again.")
    # Exit gracefully if the model can't be loaded, as the rest of the script won't work.
    sys.exit(1)


def find_best_answer_ai(user_q: str, faqs: list, threshold: float = 0.5) -> dict | None:
    """
    Finds the best answer to a user question using an AI model for semantic similarity.

    Args:
        user_q (str): The user's question.
        faqs (list): A list of FAQ dictionaries.
        threshold (float): The minimum similarity score required for a match.

    Returns:
        dict | None: The best matching FAQ dictionary, or None if no good match is found.
    """
    # Create a list of just the FAQ questions for embedding
    faq_questions = [item["question"] for item in faqs]

    # Compute embeddings for the user question and all FAQ questions
    user_embedding = model.encode(user_q, convert_to_tensor=True)
    faq_embeddings = model.encode(faq_questions, convert_to_tensor=True)

    # Compute cosine-similarity scores between the user question and all FAQs
    # The cosine-similarity is a measure of how similar the two embeddings are.
    cosine_scores = util.cos_sim(user_embedding, faq_embeddings)[0]

    # Find the index of the highest score
    best_match_index = cosine_scores.argmax()
    best_score = cosine_scores[best_match_index]

    # Check if the highest score is above our set threshold
    if best_score >= threshold:
        best_match = faqs[best_match_index]
        print(f"(Match confidence: {best_score:.2f})")
        return best_match
    else:
        return None


if __name__ == "__main__":
    # --- 3. Main Bot Loop ---
    # Load FAQ data
    base_dir = os.path.dirname(__file__)
    faqs_path = os.path.join(base_dir, "faqs.json")
    faqs = load_faqs_from_json(faqs_path)

    if not faqs:
        print("Exiting bot due to no FAQs found.")
    else:
        print(f"Loaded {len(faqs)} FAQs. Ask me something! (type 'q' to quit)")
        print("Note: The bot uses AI, so it understands similar phrases and typos.")

        while True:
            user_q = input("> ").strip()
            if user_q.lower() in {"q", "quit", "exit"}:
                print("Bye!")
                break
            if not user_q:
                continue

            found_faq = find_best_answer_ai(user_q, faqs)

            if found_faq:
                print(f"Bot: {found_faq['answer']}")
            else:
                print("Bot: Sorry, I don't have an answer for that. Please try rephrasing your question.")

