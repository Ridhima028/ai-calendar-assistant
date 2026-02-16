from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from datetime import datetime


def get_calendar_service(credentials_dict):
    """
    Build and return Google Calendar service from credentials dict
    
    Args:
        credentials_dict: Dictionary containing OAuth credentials
        
    Returns:
        Google Calendar service object
    """
    # Convert credentials dict to Credentials object
    credentials = Credentials(
        token=credentials_dict.get("token"),
        refresh_token=credentials_dict.get("refresh_token"),
        token_uri=credentials_dict.get("token_uri"),
        client_id=credentials_dict.get("client_id"),
        client_secret=credentials_dict.get("client_secret"),
        scopes=credentials_dict.get("scopes")
    )
    
    # Only try to refresh if we have all required fields
    if credentials.expired and credentials.refresh_token:
        try:
            if credentials.token_uri and credentials.client_id and credentials.client_secret:
                credentials.refresh(Request())
                print("[CALENDAR_SERVICE] Token refreshed successfully")
            else:
                print("[CALENDAR_SERVICE] Warning: Missing fields for token refresh, using existing token")
        except Exception as e:
            print(f"[CALENDAR_SERVICE] Token refresh failed: {e}")
            # Continue with existing token
    
    # Build and return calendar service
    service = build("calendar", "v3", credentials=credentials)
    return service


def create_event(service, title, start, end, description=""):
    """
    Create a calendar event
    
    Args:
        service: Google Calendar service object
        title: Event title
        start: Start datetime (string in ISO format or datetime object)
        end: End datetime (string in ISO format or datetime object)
        description: Event description (optional)
        
    Returns:
        Tuple (success: bool, result: dict)
    """
    try:
        # Convert datetime objects to ISO format strings if needed
        if isinstance(start, datetime):
            start = start.isoformat()
        if isinstance(end, datetime):
            end = end.isoformat()
        
        # Create event body
        event = {
            "summary": title,
            "description": description,
            "start": {
                "dateTime": start,
                "timeZone": "UTC",
            },
            "end": {
                "dateTime": end,
                "timeZone": "UTC",
            },
        }
        
        # Insert event into primary calendar
        event_result = service.events().insert(
            calendarId="primary",
            body=event
        ).execute()
        
        return True, event_result
        
    except Exception as e:
        return False, str(e)


def check_conflicts(service, start, end):
    """
    Check if there are any conflicting events in the given time range
    
    Args:
        service: Google Calendar service object
        start: Start datetime (string in ISO format or datetime object)
        end: End datetime (string in ISO format or datetime object)
        
    Returns:
        List of conflicting events
    """
    try:
        # Convert datetime objects to ISO format strings if needed
        if isinstance(start, datetime):
            start_str = start.isoformat()
        else:
            start_str = start
            
        if isinstance(end, datetime):
            end_str = end.isoformat()
        else:
            end_str = end
        
        # Ensure timezone is included (add Z if not present)
        if 'Z' not in start_str and '+' not in start_str and '-' not in start_str[-6:]:
            start_str = start_str + 'Z'
        if 'Z' not in end_str and '+' not in end_str and '-' not in end_str[-6:]:
            end_str = end_str + 'Z'
        
        print(f"[CHECK_CONFLICTS] Querying events from {start_str} to {end_str}")
        
        # Get events that overlap with the requested time
        # We need to check a wider range to catch all overlapping events
        from datetime import datetime as dt, timedelta
        
        # Parse the start time to get a wider search range
        start_dt = dt.fromisoformat(start_str.replace('Z', '+00:00'))
            
        # Search from 24 hours before to 24 hours after
        search_start = (start_dt - timedelta(days=1)).isoformat().replace('+00:00', 'Z')
        search_end = (start_dt + timedelta(days=1)).isoformat().replace('+00:00', 'Z')
        
        print(f"[CHECK_CONFLICTS] Expanded search range: {search_start} to {search_end}")
        
        # Query events in the expanded time range
        events_result = service.events().list(
            calendarId="primary",
            timeMin=search_start,
            timeMax=search_end,
            singleEvents=True,
            orderBy="startTime"
        ).execute()
        
        all_events = events_result.get("items", [])
        print(f"[CHECK_CONFLICTS] Found {len(all_events)} total events in expanded range")
        
        # Filter to only events that actually overlap with our requested time
        conflicting_events = []
        for event in all_events:
            event_start = event.get("start", {}).get("dateTime")
            event_end = event.get("end", {}).get("dateTime")
            
            if not event_start or not event_end:
                continue
            
            # Check if events overlap
            # Events overlap if: event_start < our_end AND event_end > our_start
            if event_start < end_str and event_end > start_str:
                print(f"[CHECK_CONFLICTS] CONFLICT: {event.get('summary', 'No title')} ({event_start} to {event_end})")
                conflicting_events.append(event)
            else:
                print(f"[CHECK_CONFLICTS] No overlap: {event.get('summary', 'No title')} ({event_start} to {event_end})")
        
        print(f"[CHECK_CONFLICTS] Returning {len(conflicting_events)} conflicting events")
        return conflicting_events
        
    except Exception as e:
        print(f"[CHECK_CONFLICTS] Error checking conflicts: {e}")
        import traceback
        traceback.print_exc()
        return []


def delete_event(service, event_id):
    """
    Delete a calendar event
    
    Args:
        service: Google Calendar service object
        event_id: ID of the event to delete
        
    Returns:
        Tuple (success: bool, result: str)
    """
    try:
        service.events().delete(
            calendarId="primary",
            eventId=event_id
        ).execute()
        
        return True, f"Event {event_id} deleted successfully"
        
    except Exception as e:
        return False, str(e)


def list_events(service, max_results=50):
    """
    List calendar events (past, present, and future)
    
    Args:
        service: Google Calendar service object
        max_results: Maximum number of events to return
        
    Returns:
        List of event dictionaries
    """
    try:
        from datetime import datetime, timedelta
        
        # Get events from 7 days ago to 30 days in the future
        time_min = (datetime.utcnow() - timedelta(days=7)).isoformat() + 'Z'
        time_max = (datetime.utcnow() + timedelta(days=30)).isoformat() + 'Z'
        
        print(f"[LIST_EVENTS] Querying events from {time_min} to {time_max}")
        
        events_result = service.events().list(
            calendarId="primary",
            timeMin=time_min,
            timeMax=time_max,
            maxResults=max_results,
            singleEvents=True,
            orderBy="startTime"
        ).execute()
        
        events = events_result.get("items", [])
        print(f"[LIST_EVENTS] Found {len(events)} events")
        
        for event in events:
            print(f"[LIST_EVENTS] - {event.get('summary', 'No title')} at {event.get('start', {}).get('dateTime', 'No time')}")
        
        return events
        
    except Exception as e:
        print(f"[LIST_EVENTS] Error listing events: {e}")
        import traceback
        traceback.print_exc()
        # Return empty list instead of raising error
        return []
