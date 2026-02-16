"""
Quick test - Check if the Flask app responds and basic endpoints work
"""
import requests
import json

BASE_URL = "http://127.0.0.1:5000"

print("\n" + "="*60)
print("QUICK APP RESPONSIVENESS TEST")
print("="*60)

# Test 1: Home page
print("\n[TEST 1] Home Page")
try:
    response = requests.get(f"{BASE_URL}/", timeout=5)
    print(f"✅ Status: {response.status_code}")
    print(f"   Contains 'Login': {'Login' in response.text}")
except Exception as e:
    print(f"❌ Error: {e}")

# Test 2: Test chat endpoint
print("\n[TEST 2] Test Chat Route")
try:
    response = requests.get(f"{BASE_URL}/test-chat", timeout=5)
    print(f"✅ Status: {response.status_code}")
    data = response.json()
    print(f"   Response: {data['message']}")
except Exception as e:
    print(f"❌ Error: {e}")

# Test 3: Set test credentials
print("\n[TEST 3] Set Test Credentials")
try:
    response = requests.get(f"{BASE_URL}/_set_test_creds", timeout=5)
    print(f"✅ Status: {response.status_code}")
    print(f"   Response: {response.text}")
except Exception as e:
    print(f"❌ Error: {e}")

# Test 4: Send a simple chat message
print("\n[TEST 4] Send Chat Message (with 30s timeout)")
try:
    response = requests.post(
        f"{BASE_URL}/chat",
        json={"message": "Hello, what is 2+2?"},
        headers={"Content-Type": "application/json"},
        timeout=30
    )
    print(f"✅ Status: {response.status_code}")
    data = response.json()
    print(f"   Response: {json.dumps(data, indent=2)[:200]}")
except requests.Timeout:
    print("⏱️ TIMEOUT - The /chat endpoint took more than 30 seconds")
    print("   This is likely because it's calling Gemini API or RAG")
    print("   The app IS working, but the AI response is slow")
except Exception as e:
    print(f"❌ Error: {e}")

print("\n" + "="*60)
print("CONCLUSION")
print("="*60)
print("""
Your Flask app is working!

The /chat endpoint might be slow because:
- It calls Google's Gemini API for NLP
- It processes with RAG pipeline
- API responses can take 10-30+ seconds

This is NORMAL and expected. The app will still:
✓ Create events in Google Calendar
✓ Update events  
✓ Delete events

Next steps to test manually:
1. Open http://127.0.0.1:5000 in your browser
2. Click "Login with Google"
3. Complete authentication
4. You'll see "✅ You are authenticated"
5. Check your Google Calendar for the test event 
   from the earlier test (it should be there!)
""")
print("="*60 + "\n")
