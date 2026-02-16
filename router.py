from intent_detector import detect_intent
from handlers.calendar_create import handle_create_event
from handlers.calendar_delete import handle_delete_event
from handlers.rag_query import handle_rag_query
from handlers.conflict_resolution import handle_conflict_resolution

def route_message(user_message, session):
    # Check if there's a pending conflict resolution
    if "pending_event" in session and "conflicts" in session:
        # User is responding to a conflict
        result = handle_conflict_resolution(
            user_message=user_message,
            pending_event=session["pending_event"],
            conflicts=session["conflicts"],
            session=session
        )
        
        # Clear pending data unless still waiting for response
        if not result.get("conflict_pending"):
            session.pop("pending_event", None)
            session.pop("conflicts", None)
        
        return result
    
    # Normal intent detection
    intent_data = detect_intent(user_message)
    intent = intent_data["intent"]

    if intent == "create_event":
        result = handle_create_event(user_message, session)
        
        # If conflict detected, store in session
        if result.get("conflict_detected"):
            session["pending_event"] = result.get("pending_event")
            session["conflicts"] = result.get("conflicts")
        
        return result

    elif intent == "delete_event":
        return handle_delete_event(user_message, session)

    elif intent == "query":
        return handle_rag_query(user_message)

    else:
        return {"error": "Intent not supported yet"}
