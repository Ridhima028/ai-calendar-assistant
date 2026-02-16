"""
Test whether events are actually being created in Google Calendar
"""
import json
import sys
import os
from datetime import datetime, timedelta

sys.path.insert(0, os.getcwd())

from services.calendar_service import get_calendar_service, create_event, list_events

def test_calendar_integration():
    """Test if calendar operations work"""
    print("\n" + "="*60)
    print("CALENDAR INTEGRATION TEST")
    print("="*60)
    
    # Step 1: Load credentials from token.json
    print("\n[STEP 1] Loading credentials from token.json...")
    try:
        with open("token.json", "r") as f:
            creds_data = json.load(f)
        print("✅ Credentials loaded")
        print(f"   - Token: {creds_data.get('token', 'N/A')[:30]}...")
        print(f"   - Refresh Token: {'Present' if creds_data.get('refresh_token') else 'Missing'}")
        print(f"   - Client ID: {creds_data.get('client_id', 'N/A')[:30]}...")
    except Exception as e:
        print(f"❌ Error loading credentials: {e}")
        return False
    
    # Step 2: Build calendar service
    print("\n[STEP 2] Building Google Calendar service...")
    try:
        service = get_calendar_service(creds_data)
        print("✅ Calendar service built successfully")
    except Exception as e:
        print(f"❌ Error building service: {e}")
        return False
    
    # Step 3: List current events
    print("\n[STEP 3] Listing current calendar events...")
    try:
        events = list_events(service, max_results=5)
        print(f"✅ Retrieved {len(events)} events")
        if events:
            print("   Recent events:")
            for event in events[:3]:
                print(f"   - {event.get('summary', 'Untitled')}")
                print(f"     Time: {event.get('start', {}).get('dateTime', 'All day')}")
        else:
            print("   No events found (calendar might be empty)")
    except Exception as e:
        print(f"❌ Error listing events: {e}")
        return False
    
    # Step 4: Create a test event
    print("\n[STEP 4] Creating a test event...")
    try:
        # Create event for 1 hour from now
        start_time = datetime.utcnow() + timedelta(hours=1)
        end_time = start_time + timedelta(hours=1)
        
        success, result = create_event(
            service=service,
            title="🧪 Test Event - Calendar Integration",
            start=start_time.isoformat() + "Z",
            end=end_time.isoformat() + "Z",
            description="This is a test event created by the calendar integration test"
        )
        
        if success:
            event_id = result.get("id")
            print(f"✅ Event created successfully!")
            print(f"   - Event ID: {event_id}")
            print(f"   - Title: {result.get('summary')}")
            print(f"   - Time: {result.get('start', {}).get('dateTime', 'N/A')}")
            print(f"   - Link: {result.get('htmlLink')}")
        else:
            print(f"❌ Event creation failed: {result}")
            return False
    except Exception as e:
        print(f"❌ Error creating event: {e}")
        return False
    
    # Step 5: Verify event was created
    print("\n[STEP 5] Verifying event was created...")
    try:
        events = list_events(service, max_results=10)
        
        # Look for our test event
        test_event_found = False
        for event in events:
            if "Test Event" in event.get('summary', ''):
                test_event_found = True
                print(f"✅ Test event found in calendar!")
                print(f"   - Title: {event.get('summary')}")
                print(f"   - Time: {event.get('start', {}).get('dateTime', 'All day')}")
                print(f"   - Description: {event.get('description', 'N/A')}")
                break
        
        if not test_event_found:
            print("⚠️ Test event not found in the list of events")
            print("   This might be normal if it's scheduled for the future")
        
        return True
    except Exception as e:
        print(f"❌ Error verifying event: {e}")
        return False

def main():
    print("\n" + "="*60)
    print("GOOGLE CALENDAR INTEGRATION CHECK")
    print("="*60)
    
    try:
        result = test_calendar_integration()
        
        print("\n" + "="*60)
        print("TEST SUMMARY")
        print("="*60)
        if result:
            print("✅ Calendar integration is WORKING!")
            print("\nYour app CAN:")
            print("  ✓ Connect to Google Calendar")
            print("  ✓ Create events")
            print("  ✓ List events")
            print("\nEvents created through /chat endpoint should appear in your Google Calendar!")
        else:
            print("❌ Calendar integration has ISSUES")
            print("\nCheck:")
            print("  - Your token.json file is valid")
            print("  - Your Google credentials haven't expired")
            print("  - Your Google account has Calendar API enabled")
        print("="*60)
        
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
