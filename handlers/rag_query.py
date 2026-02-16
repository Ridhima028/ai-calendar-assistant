# handlers/rag_query.py

from rag.rag_pipeline import get_rag_chain

def handle_query(user_message):
    """
    Answer general questions using RAG
    """
    rag_chain = get_rag_chain()
    response = rag_chain.invoke({
        "input": user_message
    })

    return {
        "response": response.get("answer", response)
    }


def handle_rag_query(user_message):
    """Alias for handle_query - compatibility for router"""
    return handle_query(user_message)
