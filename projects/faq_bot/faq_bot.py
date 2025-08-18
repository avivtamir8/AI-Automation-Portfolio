import json

def load_faqs_from_json(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        return json.load(f)


import os
import re
from difflib import SequenceMatcher

def normalize(text: str) -> str:
    text = text.lower().strip()
    text = re.sub(r"[^a-z0-9\s]", " ", text)  # keep letters/numbers/spaces
    text = re.sub(r"\s+", " ", text)
    return text

def similarity(a: str, b: str) -> float:
    return SequenceMatcher(None, a, b).ratio()

def find_best_answer(user_q: str, faqs: list, threshold: float = 0.55) -> dict | None:
    user_norm = normalize(user_q)
    best = {"score": 0.0, "faq": None}

    for item in faqs:
        q_norm = normalize(item["question"])
        score = similarity(user_norm, q_norm)
        if score > best["score"]:
            best = {"score": score, "faq": item}

    return best["faq"] if best["score"] >= threshold else None

if __name__ == "__main__":
    # Load data (path relative to this script)
    base_dir = os.path.dirname(__file__)
    faqs_path = os.path.join(base_dir, "faqs.json")
    faqs = load_faqs_from_json(faqs_path)
    print(f"Loaded {len(faqs)} FAQs. Ask me something! (type 'q' to quit)")

    while True:
        user_q = input("> ").strip()
        if user_q.lower() in {"q", "quit", "exit"}:
            print("Bye!")
            break
        if not user_q:
            continue

        if user_q.lower() in {"help", "h"}:
            print("Try asking about hours, delivery, returns, pricing. Type 'q' to quit.\n")
            continue
        
        match = find_best_answer(user_q, faqs)
        if match:
            print(f"Answer: {match['answer']}\n")
        else:
            print("Hmm, I’m not sure yet. (No close match found)\n")

