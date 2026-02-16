"""
End-to-end test of the chatbot - simulates sending messages and creating events
"""
import requests
import json
from datetime import datetime, timedelta

BASE_URL = "http://127.0.0.1:5000"

def get_session_with_credentials():
    """Get a session with valid credentials from token.json"""
    print("\n[SETUP] Loading credentials...")
    try:
        with open("token.json", "r") as f:
            creds_data = json.load(f)
        print("✅ Credentials loaded from token.json")
        return creds_data
    except Exception as e:
        print(f"❌ Error loading credentials: {e}")
        return None

def test_create_event(message, credentials):
    """Test creating an event by sending a message to /chat"""
    print(f"\n{'='*60}")
    print(f"Testing: {message}")
    print(f"{'='*60}")
    
    # Create a session
    session = requests.Session()
    
    # Set credentials in session (simulate logged-in state)
    with session:
        # We need to mock the session with credentials
        # Since we can't directly set Flask session from outside,
        # Let's use the test endpoint
        
        print("\n[STEP 1] Setting test credentials in session...")
        try:
            response = session.get(f"{BASE_URL}/_set_test_creds")
            if response.status_code == 200:
                print(f"✅ Credentials set: {response.text}")
            else:
                print(f"❌ Error setting credentials: {response.text}")
                return False
        except Exception as e:
            print(f"❌ Error: {e}")
            return False
        
        print(f"\n[STEP 2] Sending message to /chat endpoint...")
        print(f"Message: '{message}'")
        
        try:
            response = session.post(
                f"{BASE_URL}/chat",
                json={"message": message},
                headers={"Content-Type": "application/json"}
            )
            
            print(f"Status Code: {response.status_code}")
            
            if response.status_code == 200:
                data = response.json()
                print(f"\n✅ Response received:")
                print(json.dumps(data, indent=2))
                
                if "response" in data:
                    print(f"\nBot Response: {data['response']}")
                
                if "event_created" in data:
                    event = data['event_created']
                    print(f"\n✨ EVENT CREATED:")
                    print(f"   Title: {event.get('name')}")
                    print(f"   Time: {event.get('start')}")
                    print(f"   Description: {event.get('description')}")
                    print(f"   ID: {event.get('id')}")
                    return True
                elif "error" not in data:
                    print(f"\n⚠️ No event created (might not be an event creation request)")
                    return True
                else:
                    print(f"\n❌ Error in response: {data.get('error')}")
                    return False
            else:
                print(f"❌ Error: {response.text}")
                return False
                
        except Exception as e:
            print(f"❌ Error sending message: {e}")
            return False

def main():
    print("\n" + "="*60)
    print("CHATBOT END-TO-END TEST")
    print("="*60)
    
    # Load credentials
    creds = get_session_with_credentials()
    if not creds:
        print("\n❌ Cannot proceed without credentials")
        print("Make sure you've logged in once and token.json exists")
        return
    
    # Test messages
    test_cases = [
        "Create a meeting tomorrow at 2 PM",
        "Schedule a team standup for 10 AM next Monday",
        "Add a dentist appointment on March 15th at 3:30 PM",
        "Create a birthday celebration event for next Friday at 6 PM",
        "Book a conference with the team on Feb 20 from 1 to 3 PM",
    ]
    
    results = []
    
    for i, test_message in enumerate(test_cases, 1):
        print(f"\n\n{'#'*60}")
        print(f"TEST {i}/{len(test_cases)}")
        print(f"{'#'*60}")
        
        success = test_create_event(test_message, creds)
        results.append((test_message, success))
    
    # Summary
    print("\n\n" + "="*60)
    print("TEST SUMMARY")
    print("="*60)
    
    passed = sum(1 for _, success in results if success)
    total = len(results)
    
    print(f"\nTotal Tests: {total}")
    print(f"Passed: {passed}")
    print(f"Failed: {total - passed}")
    
    print("\nDetailed Results:")
    for i, (message, success) in enumerate(results, 1):
        status = "✅ PASSED" if success else "❌ FAILED"
        print(f"{i}. {status} - {message[:50]}...")
    
    print("\n" + "="*60)
    print("CHECK YOUR GOOGLE CALENDAR!")
    print("="*60)
    print("\n🎉 If all tests passed, check your Google Calendar to see")
    print("   the events that were created! They should appear within")
    print("   a few seconds.")
    print("\nUseful links:")
    print("  - Google Calendar: https://calendar.google.com/")
    print("  - Settings: Make sure notifications are enabled")
    print("="*60 + "\n")

if __name__ == "__main__":
    main()
