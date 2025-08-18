import os
from faq_bot import load_faqs_from_json, find_best_answer

# Path to FAQs
base_dir = os.path.dirname(__file__)
faqs_path = os.path.join(base_dir, "faqs.json")
faqs = load_faqs_from_json(faqs_path)

# Edge-case / normal / tricky questions
tests = [
    # 1–5: Normal exact questions
    ("what are your business hours?", "We are open from 9 AM to 6 PM, Monday to Friday."),
    ("do you offer delivery?", "Yes, we offer free delivery on orders above $50."),
    ("What are your business hours?", "We are open from 9 AM to 6 PM, Monday to Friday."),  # case
    ("Do you offer delivery?", "Yes, we offer free delivery on orders above $50."),          # case
    ("WHAT ARE YOUR BUSINESS HOURS?", "We are open from 9 AM to 6 PM, Monday to Friday."), # uppercase

    # 6–10: Minor punctuation / spacing
    ("what are your hours", "We are open from 9 AM to 6 PM, Monday to Friday."),
    ("what are your hours!!!", "We are open from 9 AM to 6 PM, Monday to Friday."),
    ("do you deliver?", "Yes, we offer free delivery on orders above $50."),
    ("do you deliver  ", "Yes, we offer free delivery on orders above $50."),
    ("  do you deliver", "Yes, we offer free delivery on orders above $50."),

    # 11–15: Partial matches
    ("hours", "We are open from 9 AM to 6 PM, Monday to Friday."),
    ("delivery", "Yes, we offer free delivery on orders above $50."),
    ("business hours", "We are open from 9 AM to 6 PM, Monday to Friday."),
    ("offer delivery", "Yes, we offer free delivery on orders above $50."),
    ("open hours", "We are open from 9 AM to 6 PM, Monday to Friday."),

    # 16–20: Questions that shouldn’t match
    ("refund policy", None),
    ("return items", None),
    ("shipping cost", None),
    ("contact support", None),
    ("hello bot", None),

    # 21–25: Empty / whitespace / nonsense
    ("", None),
    ("     ", None),
    ("!!!???", None),
    ("12345", None),
    ("$%^&*", None),

    # 26–30: Slightly tricky word order / synonyms
    ("hours of operation", "We are open from 9 AM to 6 PM, Monday to Friday."),
    ("do you have delivery?", "Yes, we offer free delivery on orders above $50."),
    ("delivery service", "Yes, we offer free delivery on orders above $50."),
    ("business open times", "We are open from 9 AM to 6 PM, Monday to Friday."),
    ("can you deliver?", "Yes, we offer free delivery on orders above $50."),
]

success = 0
for i, (q, expected) in enumerate(tests, 1):
    result = find_best_answer(q, faqs)
    answer = result["answer"] if result else None
    if answer == expected:
        print(f"Test {i:02d} ✅ Passed")
        success += 1
    else:
        print(f"Test {i:02d} ❌ Failed - got: {answer}, expected: {expected}")

print(f"\n{success}/{len(tests)} tests passed")
