from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from dotenv import load_dotenv
import os

load_dotenv()

# LLM setup
llm = ChatGoogleGenerativeAI(
    model="gemini-flash-latest",
    temperature=0
)

parser = JsonOutputParser()

prompt = ChatPromptTemplate.from_template("""
You are a calendar event deletion parser.

Extract the event details to delete from the user's message.

Return ONLY valid JSON in this format:
{{
  "event_title": "title or keywords to search for",
  "time_reference": "today/tomorrow/specific date if mentioned",
  "time": "specific time if mentioned (e.g., 3pm, 14:00)"
}}

Examples:
- "Delete my 3pm event today" -> {{"event_title": "", "time_reference": "today", "time": "3pm"}}
- "Delete the meeting tomorrow" -> {{"event_title": "meeting", "time_reference": "tomorrow", "time": ""}}
- "Delete group discussion meet" -> {{"event_title": "group discussion meet", "time_reference": "", "time": ""}}

User message: {input}
""")

delete_chain = prompt | llm | parser

def parse_delete_request(user_message: str) -> dict:
    """
    Parse delete request using Gemini
    """
    try:
        result = delete_chain.invoke({"input": user_message})
        print(f"[DELETE_PARSER] Parsed: {result}")
        return result
    except Exception as e:
        print(f"[DELETE_PARSER] Error: {e}")
        return {"error": str(e)}
