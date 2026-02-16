from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from dotenv import load_dotenv
import os

load_dotenv()

# ---------------- LLM SETUP ----------------
llm = ChatGoogleGenerativeAI(
    model="gemini-flash-latest",
    temperature=0
)

parser = JsonOutputParser()

prompt = ChatPromptTemplate.from_template("""
You are an intent classifier for a calendar chatbot.

Classify the user's message into ONE of the following intents:

- create_event
- update_event
- delete_event
- query

Return ONLY valid JSON in this format:

{{
  "intent": "<one_of_the_above>"
}}

User message:
{input}
""")

intent_chain = prompt | llm | parser

# ---------------- MAIN FUNCTION ----------------
def detect_intent(user_message: str) -> dict:
    """
    Detect intent using Gemini
    """
    # 🔹 TEST MODE (optional)
    test_intent = os.getenv("TEST_INTENT")
    if test_intent:
        return {"intent": test_intent}

    return intent_chain.invoke({"input": user_message})
