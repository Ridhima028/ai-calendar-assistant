"""
OAuth Flow Test - Simulates the login and callback process
"""
import requests
import json
from urllib.parse import urlparse, parse_qs

BASE_URL = "http://127.0.0.1:5000"

def test_oauth_flow():
    """Simulate OAuth login flow"""
    print("\n" + "="*60)
    print("OAUTH FLOW TEST")
    print("="*60)
    
    # Create a session to maintain cookies
    session = requests.Session()
    
    print("\n[STEP 1] Visit login page...")
    try:
        response = session.get(f"{BASE_URL}/login", allow_redirects=False)
        print(f"✅ Status Code: {response.status_code}")
        
        if response.status_code == 302:
            auth_url = response.headers.get('Location')
            print(f"✅ Redirected to: {auth_url[:100]}...")
            
            # Parse the auth URL to extract state
            parsed = urlparse(auth_url)
            params = parse_qs(parsed.query)
            state = params.get('state', [None])[0]
            
            if state:
                print(f"✅ OAuth State extracted: {state}")
                return state
            else:
                print("❌ No state found in auth URL")
                return None
        else:
            print(f"❌ Unexpected status code: {response.status_code}")
            return None
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return None

def test_callback_simulation(state):
    """Simulate OAuth callback (note: won't actually get valid Google code)"""
    print("\n" + "="*60)
    print("OAUTH CALLBACK SIMULATION")
    print("="*60)
    
    if not state:
        print("❌ No state provided")
        return False
    
    print(f"\n[STEP 1] State to callback: {state}")
    
    # Check if state was saved
    try:
        import sys
        import os
        sys.path.insert(0, os.getcwd())
        from app import get_oauth_data
        
        oauth_data = get_oauth_data(state)
        if oauth_data:
            print(f"✅ State found in storage: {oauth_data}")
            return True
        else:
            print(f"❌ State not found in storage")
            return False
    except Exception as e:
        print(f"❌ Error checking state: {e}")
        return False

def main():
    print("\n" + "="*60)
    print("OAUTH INTEGRATION TEST")
    print("="*60)
    
    # Test 1: OAuth Flow
    state = test_oauth_flow()
    
    # Test 2: Callback Simulation
    if state:
        callback_ok = test_callback_simulation(state)
    else:
        callback_ok = False
    
    # Summary
    print("\n" + "="*60)
    print("OAUTH TEST SUMMARY")
    print("="*60)
    print(f"Login Flow: {'✅ PASSED' if state else '❌ FAILED'}")
    print(f"State Storage: {'✅ PASSED' if callback_ok else '❌ FAILED'}")
    print("="*60)
    
    if state and callback_ok:
        print("\n✅ OAuth flow is working correctly!")
        print("\nNote: To complete authentication, you need to:")
        print("1. Visit http://127.0.0.1:5000/login in a browser")
        print("2. Click 'Login with Google' link")
        print("3. Grant permissions in Google's OAuth consent screen")
        print("4. You'll be redirected back and should see '✅ Logged in'")
    else:
        print("\n⚠️ OAuth flow has issues - check config and state storage")

if __name__ == "__main__":
    main()
