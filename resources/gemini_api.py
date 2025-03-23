import google.generativeai as genai


def summarize_text(text, api_key="api_key"):
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel("gemini-2.0-flash")
    response = model.generate_content(f"Tóm tắt: {text}")
    return response.text
