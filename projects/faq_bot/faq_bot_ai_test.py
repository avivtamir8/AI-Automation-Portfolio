import os
import sys
import json

# Ensure the parent directory is in the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# We import the AI version of the function to be consistent with the test run output.
from faq_bot_ai import load_faqs_from_json, find_best_answer_ai

# Path to FAQs
base_dir = os.path.dirname(__file__)
faqs_path = os.path.join(base_dir, "faqs.json")
faqs = load_faqs_from_json(faqs_path)

# Test cases based on the new, extensive FAQ list.
# We test for exact matches, case variations, punctuation, and partial matches.
tests = [
    # 1-10: Business Hours
    ("What are your business hours?", "We are open from 9 AM to 6 PM, Monday to Friday."),
    ("business hours?", "We are open from 9 AM to 6 PM, Monday to Friday."),
    ("HOURS?", "We are open from 9 AM to 6 PM, Monday to Friday."),
    ("what are your store hours?", "We are open from 9 AM to 6 PM, Monday to Friday."),
    ("What time do you open?", "We are open from 9 AM to 6 PM, Monday to Friday."),
    ("What time do you close?", "Our closing time is 6 PM."),
    ("are you open on weekends?", "No, we are closed on weekends."),
    ("days open?", "We are open from 9 AM to 6 PM, Monday to Friday."),
    ("hours of operation?", "We are open from 9 AM to 6 PM, Monday to Friday."),
    ("when do you open and close?", "We are open from 9 AM to 6 PM, Monday to Friday."),

    # 11-20: Delivery
    ("do you offer delivery?", "Yes, we offer free delivery on orders above $50."),
    ("delivery?", "Yes, we offer free delivery on orders above $50."),
    ("IS DELIVERY AVAILABLE?", "Yes, we offer free delivery on orders above $50."),
    ("what is the delivery fee?",
     "Delivery is free for orders over $50. A flat fee of $5 applies to all other orders."),
    ("how much does delivery cost?",
     "Delivery is free for orders over $50. A flat fee of $5 applies to all other orders."),
    ("free delivery?", "Yes, we offer free delivery on orders above $50."),
    ("do you deliver locally?", "Yes, we offer free delivery on orders above $50."),
    ("delivery service?", "Yes, we offer free delivery on orders above $50."),
    ("do you offer free shipping?", "We offer free standard shipping on all orders over $75."),
    ("shipping cost?", "We offer free standard shipping on all orders over $75."),

    # 21-30: Pricing & Payment
    ("how much does it cost?",
     "Pricing depends on the product. Please check our website or contact us directly for specific quotes."),
    ("price?", "Pricing depends on the product. Please check our website or contact us directly for specific quotes."),
    ("What is the price of your services?",
     "Pricing depends on the product. Please check our website or contact us directly for specific quotes."),
    ("What payment methods do you accept?", "We accept all major credit cards, PayPal, and Apple Pay."),
    ("payment methods?", "We accept all major credit cards, PayPal, and Apple Pay."),
    ("can I pay with paypal?", "We accept all major credit cards, PayPal, and Apple Pay."),
    ("do you take credit cards?", "We accept all major credit cards, PayPal, and Apple Pay."),
    ("what forms of payment are accepted?", "We accept all major credit cards, PayPal, and Apple Pay."),
    ("how do I find out the price?",
     "Pricing depends on the product. Please check our website or contact us directly for specific quotes."),
    ("what is the price?",
     "Pricing depends on the product. Please check our website or contact us directly for specific quotes."),

    # 31-40: Returns & Shipping
    ("What is your return policy?",
     "We accept returns for a full refund within 30 days of purchase with a valid receipt."),
    ("return policy?", "We accept returns for a full refund within 30 days of purchase with a valid receipt."),
    ("can i return an item?", "We accept returns for a full refund within 30 days of purchase with a valid receipt."),
    ("do you ship internationally?", "Currently, we only ship to addresses within the United States and Canada."),
    ("international shipping?", "Currently, we only ship to addresses within the United States and Canada."),
    ("How long does shipping take?", "Standard shipping usually takes 5-7 business days."),
    ("shipping time?", "Standard shipping usually takes 5-7 business days."),
    ("can I track my order?", "Yes, you will receive a tracking number via email once your order has shipped."),
    ("track order?", "Yes, you will receive a tracking number via email once your order has shipped."),
    ("how do i get my tracking number?",
     "Yes, you will receive a tracking number via email once your order has shipped."),

    # 41-50: Products & Services
    ("Do you offer gift cards?", "Yes, digital gift cards are available for purchase on our website."),
    ("gift cards?", "Yes, digital gift cards are available for purchase on our website."),
    ("are your products eco-friendly?",
     "We are committed to sustainability. Our products are made with recycled materials and our packaging is compostable."),
    ("eco-friendly?",
     "We are committed to sustainability. Our products are made with recycled materials and our packaging is compostable."),
    ("are all your products handmade?", "Yes, all of our products are lovingly handmade in our local workshop."),
    ("handmade?", "Yes, all of our products are lovingly handmade in our local workshop."),
    ("do you have a loyalty program?",
     "Yes, our loyalty program rewards you with points for every purchase, which can be redeemed for discounts."),
    ("loyalty program?",
     "Yes, our loyalty program rewards you with points for every purchase, which can be redeemed for discounts."),
    ("do you offer catering?",
     "We do not currently offer catering, but we have partnerships with local caterers we can recommend."),
    ("catering?", "We do not currently offer catering, but we have partnerships with local caterers we can recommend."),

    # 51-60: Contact & Location
    ("how do i contact customer support?",
     "You can reach our support team via email at support@example.com or by phone at (555) 123-4567."),
    ("contact?", "You can reach our support team via email at support@example.com or by phone at (555) 123-4567."),
    ("Where is your store located?", "Our main store is located at 123 Main Street, Anytown, USA."),
    ("location?", "Our main store is located at 123 Main Street, Anytown, USA."),
    ("what is your address?", "Our main store is located at 123 Main Street, Anytown, USA."),
    ("what is your email address?",
     "You can reach our support team via email at support@example.com or by phone at (555) 123-4567."),
    ("what is your phone number?",
     "You can reach our support team via email at support@example.com or by phone at (555) 123-4567."),
    ("how can I get in touch?",
     "You can reach our support team via email at support@example.com or by phone at (555) 123-4567."),
    ("can I visit your store?", "Our main store is located at 123 Main Street, Anytown, USA."),
    ("what is the typical response time for emails?", "We aim to respond to all emails within 24 business hours."),

    # 61-70: General & Policy
    ("how do i apply for a job?",
     "Please send your resume and cover letter to jobs@example.com with the position you are applying for in the subject line."),
    ("apply for a job?",
     "Please send your resume and cover letter to jobs@example.com with the position you are applying for in the subject line."),
    ("do you offer wholesale pricing?",
     "Yes, please fill out our wholesale inquiry form on our website to receive more information."),
    ("wholesale pricing?",
     "Yes, please fill out our wholesale inquiry form on our website to receive more information."),
    ("is your store wheelchair accessible?",
     "Yes, our store is fully wheelchair accessible, with ramps and wide aisles."),
    ("wheelchair accessible?", "Yes, our store is fully wheelchair accessible, with ramps and wide aisles."),
    ("can i place a special order?",
     "We do not currently offer special orders, but we are always adding new products to our collection."),
    ("special order?",
     "We do not currently offer special orders, but we are always adding new products to our collection."),
    ("do you offer student discounts?",
     "Yes, students with a valid student ID can receive a 10% discount on all purchases."),
    ("student discounts?", "Yes, students with a valid student ID can receive a 10% discount on all purchases."),

    # 71-80: More Policy & FAQs
    ("what is your privacy policy?",
     "Our privacy policy can be found on our website, detailing how we handle your personal information."),
    ("privacy policy?",
     "Our privacy policy can be found on our website, detailing how we handle your personal information."),
    ("what are your holiday hours?",
     "Our holiday hours vary. Please check our website or social media for the most up-to-date schedule."),
    ("holiday hours?",
     "Our holiday hours vary. Please check our website or social media for the most up-to-date schedule."),
    ("can i cancel my order?",
     "Orders can be canceled within 24 hours of being placed. Please contact customer support immediately."),
    ("cancel order?",
     "Orders can be canceled within 24 hours of being placed. Please contact customer support immediately."),
    ("what is your mission statement?",
     "Our mission is to create high-quality, sustainable products that bring joy to our customers."),
    ("mission statement?",
     "Our mission is to create high-quality, sustainable products that bring joy to our customers."),
    ("who are you?", "Our mission is to create high-quality, sustainable products that bring joy to our customers."),
    ("what do you do?", "Our mission is to create high-quality, sustainable products that bring joy to our customers."),

    # 81-100: Negative test cases (questions that shouldn't match) and general conversation
    ("hello bot", None),
    ("what's the weather like?", None),
    ("how do I cook pasta?", None),
    ("what is your name?", None),
    ("where are you from?", None),
    ("tell me a joke", None),
    ("     ", None),
    ("", None),
    ("Who is the CEO?", None),
    ("What are the best programming languages?", None),
    ("What is your favorite color?", None),
    ("What is the capital of France?", None),
    ("Do you like movies?", None),
    ("Can you write a poem?", None),
    ("What's a good book to read?", None),
    ("When was the internet invented?", None),
    ("How do I fix a broken car?", None),
    ("Tell me about yourself.", None),
    ("What is the meaning of life?", None),
    ("I need a therapist.", None),
]

success = 0
# A higher threshold to prevent weak matches from passing.
threshold = 0.5

for i, (q, expected) in enumerate(tests, 1):
    # Call the AI-powered function with a higher threshold
    result_faq = find_best_answer_ai(q, faqs, threshold=threshold)
    answer = result_faq["answer"] if result_faq else None

    print(f"Test {i}: Q: '{q}'")
    print(f"       A: '{answer}'")

    if answer == expected:
        print("       Status: ✅ Pass")
        success += 1
    else:
        print(f"       Status: ❌ Fail (Expected: '{expected}')")

print("\n--- Test Summary ---")
print(f"Total tests: {len(tests)}")
print(f"Passed: {success}")
print(f"Failed: {len(tests) - success}")
