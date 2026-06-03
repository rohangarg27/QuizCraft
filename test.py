import google.generativeai as genai
import os

genai.configure(api_key="api-key")


model = genai.GenerativeModel("gemini-1.5-flash")

try:
    response = model.generate_content("Hello Gemini, say hi in one short sentence.")
    print("✅ API Key works! Response:", response.text)
except Exception as e:
    print("API Key test failed. Error:", e)
