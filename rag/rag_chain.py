from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate
from rag.rag_store import load_rag

load_dotenv()

# LLM
llm = ChatGoogleGenerativeAI(
    model="gemini-flash-latest",
    temperature=0
)

# Prompt
prompt = ChatPromptTemplate.from_template("""
Answer the question using ONLY the context below.

<context>
{context}
</context>

Question: {input}
""")

# Load vector DB
vectorstore = load_rag()
retriever = vectorstore.as_retriever()

# Document + LLM chain
doc_chain = create_stuff_documents_chain(llm, prompt)

# Retrieval chain
rag_chain = create_retrieval_chain(retriever, doc_chain)
