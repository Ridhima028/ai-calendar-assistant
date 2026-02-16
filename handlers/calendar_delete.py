# handlers/calendar_delete.py

from services.calendar_service import get_calendar_service, delete_event, list_events
from gemini_delete_parser import parse_delete_request
from flask import session as flask_session
from datetime import datetime, timedelta

def handle_delete_event(user_message, session=None):
    """
    Delete event based on user's natural language request
    """
    # Parse the delete request
    delete_info = parse_delete_request(user_message)
    
    if "error" in delete_info:
        return {"error": f"Could not understand delete request: {delete_info['error']}"}
    
    try:
        creds_source = session if session is not None else flask_session
        
        # Check if credentials exist
        if "credentials" not in creds_source:
            return {"error": "Not authenticated. Please login with Google Calendar."}
        
        service = get_calendar_service(creds_source["credentials"])

        # Get upcoming events
        events = list_events(service, max_results=50)
        
        if not events:
            return {"response": "❌ No events found in your calendar. Make sure you're logged in and have events scheduled."}
        
        # Search for matching event
        event_title = delete_info.get("event_title", "").lower()
        time_ref = delete_info.get("time_reference", "").lower()
        time_str = delete_info.get("time", "").lower()
        
        print(f"[DELETE] Searching for: title='{event_title}', time_ref='{time_ref}', time='{time_str}'")
        
        matching_events = []
        
        for event in events:
            event_summary = event.get("summary", "").lower()
            event_start = event.get("start", {}).get("dateTime", "")
            
            # Check if title matches (if title was specified)
            title_match = True
            if event_title:
                title_match = event_title in event_summary
            
            # Check if time matches (if time was specified)
            time_match = True
            if time_str:
                # Extract hour from time string
                time_clean = time_str.replace("pm", "").replace("am", "").replace(":", "").strip()
                # Check if the hour appears in the event start time
                # For "3pm", check for "15:" or "T15" in the datetime
                if "pm" in time_str.lower():
                    hour = int(time_clean) if time_clean.isdigit() else 0
                    if hour < 12:
                        hour += 12  # Convert to 24-hour format
                    hour_str = f"T{hour:02d}:"
                    time_match = hour_str in event_start
                elif "am" in time_str.lower():
                    hour = int(time_clean) if time_clean.isdigit() else 0
                    hour_str = f"T{hour:02d}:"
                    time_match = hour_str in event_start
                else:
                    # Just check if the number appears
                    time_match = time_clean in event_start.replace(":", "").replace("-", "")
            
            # Check if date matches (if date reference was specified)
            date_match = True
            if time_ref:
                event_date = event_start.split("T")[0] if "T" in event_start else ""
                today = datetime.now().date().isoformat()
                tomorrow = (datetime.now() + timedelta(days=1)).date().isoformat()
                
                if "today" in time_ref:
                    date_match = event_date == today
                elif "tomorrow" in time_ref:
                    date_match = event_date == tomorrow
            
            print(f"[DELETE] Checking: {event.get('summary')} at {event_start}")
            print(f"[DELETE]   title_match={title_match}, time_match={time_match}, date_match={date_match}")
            
            if title_match and time_match and date_match:
                matching_events.append(event)
                print(f"[DELETE] ✓ Match found: {event.get('summary')} at {event_start}")
        
        if not matching_events:
            return {"response": "❌ No matching events found. Please be more specific."}
        
        if len(matching_events) > 1:
            # Multiple matches - list them
            event_list = "\n".join([f"• {e.get('summary', 'Untitled')} at {e.get('start', {}).get('dateTime', 'Unknown')}" 
                                   for e in matching_events[:5]])
            return {
                "response": f"⚠️ Found {len(matching_events)} matching events:\n{event_list}\n\nPlease be more specific about which one to delete."
            }
        
        # Delete the single matching event
        event_to_delete = matching_events[0]
        event_id = event_to_delete.get("id")
        event_name = event_to_delete.get("summary", "Untitled Event")
        
        success, result = delete_event(service, event_id)
        
        if success:
            return {
                "response": f"✅ Deleted event: {event_name}"
            }
        
        return {"error": f"Failed to delete event: {result}"}
    
    except Exception as e:
        print(f"[DELETE] Exception: {str(e)}")
        import traceback
        traceback.print_exc()
        return {"error": f"Failed to delete event: {str(e)}"}
