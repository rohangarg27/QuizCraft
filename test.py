import google.generativeai as genai
import os

genai.configure(api_key="AIzaSyAO86e0TpXhfZLfwNigs7qv-bIV47MzSMU")


model = genai.GenerativeModel("gemini-1.5-flash")

try:
    response = model.generate_content("Hello Gemini, say hi in one short sentence.")
    print("✅ API Key works! Response:", response.text)
except Exception as e:
    print("API Key test failed. Error:", e)
