from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI#langchain ka gemini wrapper
from langchain_core.prompts import ChatPromptTemplate, PromptTemplate
from langchain_core.runnables import RunnablePassthrough, RunnableLambda
from rag.rag_store import load_rag

load_dotenv()

# LLM
llm = ChatGoogleGenerativeAI(
    model="gemini-flash-latest",
    temperature=0#no creativity only factual answers
)

# Prompt
prompt_template = PromptTemplate.from_template("""
Answer the question using ONLY the context below.

<context>
{context}
</context>

Question: {input}
""")

# Lazy load vector DB - will be loaded only when first used
_vectorstore = None
_retriever = None

def get_vectorstore():
    global _vectorstore
    if _vectorstore is None:
        print("[RAG] Loading vector store (first use)...")
        _vectorstore = load_rag()
    return _vectorstore

def get_retriever():
    global _retriever
    if _retriever is None:
        vectorstore = get_vectorstore()
        _retriever = vectorstore.as_retriever()
    return _retriever

# Create a simple RAG chain using LCEL (LangChain Expression Language)
_rag_chain = None

def get_rag_chain():
    global _rag_chain
    if _rag_chain is None:
        retriever = get_retriever()
        
        # Define the RAG chain using LCEL
        def format_docs(docs):
            return "\n\n".join(doc.page_content for doc in docs)
        
        _rag_chain = (
            {"context": retriever | RunnableLambda(format_docs), "input": RunnablePassthrough()}
            | prompt_template
            | llm
        )
    return _rag_chain

# Export function for use in handlers
def rag_chain_invoke(input_dict):
    chain = get_rag_chain()
    result = chain.invoke(input_dict.get("input", input_dict))
    return {"answer": result.content if hasattr(result, "content") else str(result)}

# Only run this when rag_pipeline.py is executed directly
if __name__ == "__main__":
    rag_chain = get_rag_chain()
    response = rag_chain_invoke({"input": "What is RAG?"})
    print(response["answer"])


#rag isme retriever se context nikalta hai aur doc_chain me llm ke sath us context ko use karke answer generate karta hai.,,,woh knowledge.txt se retrieve karke context nikalta h fir gemini ke through hume structured data milta h
#gemini ko 3 cheezein milti h pahelei context, dusri question, teesri prompt template, fir gemini in teeno cheezo ko use karke answer generate karta h


# User Message
#      ↓
# LangChain Retrieval
#      ↓
# Knowledge.txt (FAISS)
#      ↓
# Relevant Context
#      ↓
# Prompt Template
#      ↓
# Gemini LLM
#      ↓
# Structured Output

#above is the langchain pipeline manager which manages the flow of data from user input to final output using various components like retriever, prompt template, and LLM.

# Agar LangChain nahi hota toh?

# Tumhe manually likhna padta:

# embeddings generation

# similarity search

# prompt formatting

# chunk management

# LLM invocation

# response parsing

# 💀 10x zyada code
# 💀 10x zyada bugs

