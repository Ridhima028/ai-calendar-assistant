import google.generativeai as genai
import json
import os
from dotenv import load_dotenv
from datetime import datetime, timedelta

load_dotenv()

# 🔐 Gemini config
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

def get_prompt_with_context():
    """Generate prompt with current date context"""
    today = datetime.now().date()
    tomorrow = today + timedelta(days=1)
    
    return f"""
You are a calendar assistant.

Convert the user sentence into STRICT JSON.
Do NOT explain anything.
Do NOT add markdown.

Important: Today is {today.strftime('%Y-%m-%d')} (a {today.strftime('%A')})

Rules:
- If user says "tomorrow", use {tomorrow.strftime('%Y-%m-%d')}
- If user says "today", use {today.strftime('%Y-%m-%d')}
- If duration not mentioned, assume 1 hour
- Output time in ISO format: YYYY-MM-DDTHH:MM:SS
- Assume timezone IST (UTC+5:30)
- For relative dates like "tomorrow 9pm", calculate the absolute date

Return ONLY this JSON format (no markdown, no code blocks):
{{
  "title": "",
  "start": "",
  "end": ""
}}

User sentence:
"""

def parse_event(user_input):
    model = genai.GenerativeModel("gemini-flash-latest")
    
    prompt = get_prompt_with_context()
    response = model.generate_content(
        prompt + user_input,
        generation_config={"temperature": 0}
    )

    try:
        # Clean response text - remove markdown code blocks if present
        response_text = response.text.strip()
        if response_text.startswith("```"):
            # Remove markdown code blocks
            response_text = response_text.split("```")[1]
            if response_text.startswith("json"):
                response_text = response_text[4:]
            response_text = response_text.strip()
        
        return json.loads(response_text)
    except json.JSONDecodeError as e:
        print(f"[PARSE ERROR] Failed to parse JSON: {e}")
        print(f"[PARSE ERROR] Raw response: {response.text}")
        return {
            "error": "Invalid response from Gemini",
            "raw": response.text
        }
    except Exception as e:
        print(f"[PARSE ERROR] Unexpected error: {e}")
        return {
            "error": str(e),
            "raw": response.text if hasattr(response, 'text') else ""
        }

# 🔍 TEST BLOCK
if __name__ == "__main__":
    text = "Kal 5 baje project meeting 1 ghante ki"
    result = parse_event(text)
    print(result)
