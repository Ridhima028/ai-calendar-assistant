# handlers/calendar_create.py

from gemini_parser import parse_event
from services.calendar_service import get_calendar_service, create_event, check_conflicts
from flask import session as flask_session

def handle_create_event(user_message, session=None):
    """
    Create calendar event from user message with conflict detection
    """

    # 1. Gemini se structured data nikaalo
    event_data = parse_event(user_message)

    # Check for errors in parsing
    if not event_data or "error" in event_data:
        error_msg = event_data.get("error", "Could not understand event details") if isinstance(event_data, dict) else "Could not understand event details"
        print(f"[CREATE_EVENT] Parse error: {error_msg}")
        if isinstance(event_data, dict) and "raw" in event_data:
            print(f"[CREATE_EVENT] Raw response: {event_data.get('raw')}")
        return {"error": error_msg}
    
    # Validate that required fields are present
    if not all(key in event_data for key in ["title", "start", "end"]):
        return {"error": "Missing required event details (title, start, or end)"}

    try:
        creds_source = session if session is not None else flask_session
        service = get_calendar_service(creds_source["credentials"])

        # 2. Check for conflicts
        print(f"[CREATE_EVENT] Checking conflicts for time range: {event_data['start']} to {event_data['end']}")
        conflicts = check_conflicts(service, event_data["start"], event_data["end"])
        print(f"[CREATE_EVENT] Found {len(conflicts)} conflicting events")
        
        if conflicts:
            # Format conflict information
            conflict_info = []
            for event in conflicts:
                event_title = event.get("summary", "Untitled Event")
                event_start = event.get("start", {}).get("dateTime", "Unknown time")
                print(f"[CREATE_EVENT] Conflict: {event_title} at {event_start}")
                conflict_info.append(f"• {event_title} at {event_start}")
            
            conflict_message = "\n".join(conflict_info)
            
            print(f"[CREATE_EVENT] Returning conflict response")
            return {
                "response": f"⚠️ Time conflict detected!\n\nExisting events:\n{conflict_message}\n\nWould you like me to:\n1. Delete the existing event(s) and create the new one?\n2. Create anyway (double booking)?\n3. Cancel?\n\nPlease reply with 'delete and create', 'create anyway', or 'cancel'.",
                "conflict_detected": True,
                "conflicts": conflicts,
                "pending_event": event_data
            }

        # 3. No conflicts - create event
        print(f"[CREATE_EVENT] No conflicts found, creating event")
        success, result = create_event(
            service=service,
            title=event_data["title"],
            start=event_data["start"],
            end=event_data["end"],
            description=event_data.get("description", "")
        )

        if success:
            return {
                "response": f"✅ Created event: {event_data['title']}",
                "event_created": {
                    "name": event_data["title"],
                    "start": event_data["start"],
                    "description": event_data.get("description", ""),
                    "id": result["id"]
                }
            }

        return {"error": result}
    
    except Exception as e:
        print(f"[CREATE_EVENT] Exception: {str(e)}")
        import traceback
        traceback.print_exc()
        return {"error": f"Failed to create event: {str(e)}"}
