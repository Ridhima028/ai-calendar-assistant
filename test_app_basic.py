"""
Basic test script to verify the app is running without UI
"""
import requests
import json
import time

BASE_URL = "http://127.0.0.1:5000"

def test_home_route():
    """Test the home route"""
    print("\n" + "="*50)
    print("TEST 1: Home Route")
    print("="*50)
    try:
        response = requests.get(f"{BASE_URL}/")
        print(f"✅ Status Code: {response.status_code}")
        print(f"✅ Response: {response.text[:200]}")
        if "Login with Google" in response.text:
            print("✅ Home page showing login link (not authenticated)")
            return True
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_test_chat_route():
    """Test the test-chat route"""
    print("\n" + "="*50)
    print("TEST 2: Test Chat Route")
    print("="*50)
    try:
        response = requests.get(f"{BASE_URL}/test-chat")
        print(f"✅ Status Code: {response.status_code}")
        data = response.json()
        print(f"✅ Response: {json.dumps(data, indent=2)}")
        return True
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_config_loaded():
    """Test that config is loaded"""
    print("\n" + "="*50)
    print("TEST 3: Check Config File")
    print("="*50)
    try:
        from config import GOOGLE_CLIENT_ID, GOOGLE_CLIENT_SECRET, GOOGLE_REDIRECT_URI
        print(f"✅ GOOGLE_CLIENT_ID: {GOOGLE_CLIENT_ID[:20]}..." if GOOGLE_CLIENT_ID else "❌ GOOGLE_CLIENT_ID not set")
        print(f"✅ GOOGLE_CLIENT_SECRET: {GOOGLE_CLIENT_SECRET[:20]}..." if GOOGLE_CLIENT_SECRET else "❌ GOOGLE_CLIENT_SECRET not set")
        print(f"✅ GOOGLE_REDIRECT_URI: {GOOGLE_REDIRECT_URI}")
        return all([GOOGLE_CLIENT_ID, GOOGLE_CLIENT_SECRET, GOOGLE_REDIRECT_URI])
    except Exception as e:
        print(f"❌ Error loading config: {e}")
        return False

def test_modules_imported():
    """Test that all modules can be imported"""
    print("\n" + "="*50)
    print("TEST 4: Module Imports")
    print("="*50)
    modules = [
        "flask",
        "google_auth_oauthlib",
        "google.oauth2",
        "googleapiclient",
        "config",
        "gemini_parser",
        "router"
    ]
    
    all_good = True
    for module in modules:
        try:
            __import__(module)
            print(f"✅ {module}")
        except ImportError as e:
            print(f"❌ {module}: {e}")
            all_good = False
    return all_good

def test_oauth_state_storage():
    """Test the OAuth state storage mechanism"""
    print("\n" + "="*50)
    print("TEST 5: OAuth State Storage")
    print("="*50)
    try:
        import sys
        import os
        sys.path.insert(0, os.getcwd())
        
        from app import save_oauth_data, get_oauth_data, clear_oauth_data
        
        # Test state
        test_state = "test_state_12345"
        test_data = {"state": test_state, "test": "data"}
        
        # Save
        save_oauth_data(test_state, test_data)
        print(f"✅ Saved state: {test_state}")
        
        # Retrieve
        retrieved = get_oauth_data(test_state)
        if retrieved == test_data:
            print(f"✅ Retrieved state correctly: {retrieved}")
        else:
            print(f"❌ Retrieved state mismatch: {retrieved}")
            return False
        
        # Clear
        clear_oauth_data(test_state)
        retrieved_after_clear = get_oauth_data(test_state)
        if retrieved_after_clear is None:
            print(f"✅ Cleared state successfully")
        else:
            print(f"❌ State not cleared properly")
            return False
        
        return True
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def main():
    print("\n" + "="*60)
    print("BASIC APP TEST SUITE - No UI Required")
    print("="*60)
    
    results = []
    
    # Test 1: Modules
    print("\n[STEP 1] Testing module imports...")
    results.append(("Module Imports", test_modules_imported()))
    
    # Test 2: Config
    print("\n[STEP 2] Testing config...")
    results.append(("Config Loading", test_config_loaded()))
    
    # Test 3: OAuth State Storage
    print("\n[STEP 3] Testing OAuth state storage...")
    results.append(("OAuth State Storage", test_oauth_state_storage()))
    
    # Wait a moment for server to start
    print("\n[STEP 4] Waiting for Flask server to start...")
    time.sleep(2)
    
    # Test 4: Flask Server Routes
    print("\n[STEP 5] Testing Flask server routes...")
    try:
        results.append(("Home Route", test_home_route()))
        results.append(("Test Chat Route", test_test_chat_route()))
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to Flask server at http://127.0.0.1:5000")
        print("   Make sure the Flask app is running!")
        results.append(("Flask Server", False))
    
    # Summary
    print("\n" + "="*60)
    print("TEST SUMMARY")
    print("="*60)
    
    passed = 0
    failed = 0
    for test_name, result in results:
        status = "✅ PASSED" if result else "❌ FAILED"
        print(f"{test_name}: {status}")
        if result:
            passed += 1
        else:
            failed += 1
    
    print("="*60)
    print(f"Total: {passed} passed, {failed} failed")
    print("="*60)

if __name__ == "__main__":
    main()
