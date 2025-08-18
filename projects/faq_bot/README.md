# FAQ Bot MVP

## Project Overview
The FAQ Bot automates answering repetitive customer questions using Python scripting and, in the future, GPT integration.  
It’s designed for small and medium businesses to **save 5–10 hours per month** on customer support.

This project demonstrates practical automation, portfolio-ready Python skills, and measurable ROI for SMBs.

---

## Goals
- Provide fast, accurate answers to frequently asked questions.
- Demonstrate practical automation using Python (non-AI MVP) and GPT (future AI upgrade).
- Deliver measurable ROI for SMBs.

---

## Steps / Implementation Plan
1. **Load FAQs**  
   Load questions and answers from a JSON file (or CSV) to create the knowledge base.

2. **Non-AI Query Matching (Day 2 MVP)**  
   - Match user input to the closest FAQ using string similarity (`SequenceMatcher`).  
   - Normalize text for case, punctuation, and whitespace.  
   - Return answer if similarity score ≥ threshold (default: 0.55).

3. **Return Output**  
   - Display the answer in the terminal.  
   - Show “no match found” if no FAQ meets the threshold.  

4. **Future GPT Integration**  
   - Replace string matching with GPT-based question understanding.  
   - Handle partial matches, synonyms, and flexible phrasing.  

---

## Notes
- This is the **first portfolio automation**, showcasing Python scripting and initial AI readiness.  
- Day 2 MVP focuses on **CLI-based keyword matching**.  
- Future improvements include a simple web interface or integration with email/chat platforms.

---

## Test Results (Day 2)

We implemented a **30-test suite** to evaluate the non-AI MVP.  
- **Total tests:** 30  
- **Passed:** 24  
- **Failed:** 6 (expected due to partial matches or alternate phrasing)

### ✅ Passing Cases
- Exact questions  
- Case-insensitive input  
- Punctuation-tolerant input  
- Empty or nonsensical input (returns None as expected)  

### ❌ Failing Cases (Expected for Day 2 MVP)
- Partial matches, short keywords, or alternate phrasing:  
  - `"hours"` → `"We are open from 9 AM to 6 PM, Monday to Friday."`  
  - `"delivery"` → `"Yes, we offer free delivery on orders above $50."`  
  - `"open hours"`, `"hours of operation"`, `"delivery service"`, `"business open times"`  

> These failures highlight the **limitations of string similarity**. All edge cases will be handled by GPT in Day 3.

---

## How to Run (Local)

From the repo root (with virtual environment active):

```bash
# Activate venv if not active
# Windows
.venv\Scripts\activate
# macOS/Linux
source .venv/bin/activate

# Run the FAQ Bot CLI
python projects/faq_bot/faq_bot.py
