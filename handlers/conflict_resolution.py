# handlers/conflict_resolution.py

from services.calendar_service import get_calendar_service, create_event, delete_event
from flask import session as flask_session

def handle_conflict_resolution(user_message, pending_event, conflicts, session=None):
    """
    Handle user's decision on how to resolve calendar conflicts
    
    Args:
        user_message: User's response (e.g., "delete and create", "create anyway", "cancel")
        pending_event: The event data that was pending due to conflict
        conflicts: List of conflicting events
        session: Flask session containing credentials
        
    Returns:
        Response dictionary
    """
    user_message_lower = user_message.lower().strip()
    
    try:
        creds_source = session if session is not None else flask_session
        service = get_calendar_service(creds_source["credentials"])
        
        # Option 1: Delete existing events and create new one
        if "delete" in user_message_lower and "create" in user_message_lower:
            deleted_count = 0
            for conflict in conflicts:
                event_id = conflict.get("id")
                if event_id:
                    success, _ = delete_event(service, event_id)
                    if success:
                        deleted_count += 1
            
            # Now create the new event
            success, result = create_event(
                service=service,
                title=pending_event["title"],
                start=pending_event["start"],
                end=pending_event["end"],
                description=pending_event.get("description", "")
            )
            
            if success:
                return {
                    "response": f"✅ Deleted {deleted_count} conflicting event(s) and created: {pending_event['title']}",
                    "event_created": {
                        "name": pending_event["title"],
                        "start": pending_event["start"],
                        "id": result["id"]
                    }
                }
            else:
                return {"error": f"Deleted conflicts but failed to create new event: {result}"}
        
        # Option 2: Create anyway (double booking)
        elif "create anyway" in user_message_lower or "anyway" in user_message_lower:
            success, result = create_event(
                service=service,
                title=pending_event["title"],
                start=pending_event["start"],
                end=pending_event["end"],
                description=pending_event.get("description", "")
            )
            
            if success:
                return {
                    "response": f"✅ Created event (double booked): {pending_event['title']}",
                    "event_created": {
                        "name": pending_event["title"],
                        "start": pending_event["start"],
                        "id": result["id"]
                    }
                }
            else:
                return {"error": f"Failed to create event: {result}"}
        
        # Option 3: Cancel
        elif "cancel" in user_message_lower:
            return {
                "response": "❌ Event creation cancelled. No changes made to your calendar."
            }
        
        # Unclear response
        else:
            return {
                "response": "I didn't understand your choice. Please reply with:\n• 'delete and create' - to remove conflicts and create new event\n• 'create anyway' - to double book\n• 'cancel' - to cancel",
                "conflict_pending": True
            }
    
    except Exception as e:
        print(f"[CONFLICT_RESOLUTION] Exception: {str(e)}")
        import traceback
        traceback.print_exc()
        return {"error": f"Failed to resolve conflict: {str(e)}"}
