from flask import Flask, redirect, request, session, jsonify, render_template
from google_auth_oauthlib.flow import Flow
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from datetime import datetime
import os
import json
import uuid

from config import *


app = Flask(__name__)
app.secret_key = "calendar_chatbot_secret_key_123"

# ---------------- CONFIG ----------------
from datetime import timedelta

app.config.update(
    SESSION_COOKIE_SAMESITE="Lax",
    SESSION_COOKIE_SECURE=False,
    SESSION_COOKIE_HTTPONLY=True,
    SESSION_PERMANENT=True,
    PERMANENT_SESSION_LIFETIME=timedelta(hours=24)
)

os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

# File-based state storage for OAuth
STATE_FILE = "oauth_state.json"

def save_oauth_data(state, data):
    """Save OAuth data indexed by state"""
    try:
        states = {}
        if os.path.exists(STATE_FILE):
            with open(STATE_FILE, 'r') as f:
                states = json.load(f)
        states[state] = data
        with open(STATE_FILE, 'w') as f:
            json.dump(states, f)
        print(f"[STATE] Saved data for state: {state}")
    except Exception as e:
        print(f"[STATE] Error saving data: {e}")

def get_oauth_data(state):
    """Retrieve OAuth data from file"""
    try:
        if os.path.exists(STATE_FILE):
            with open(STATE_FILE, 'r') as f:
                states = json.load(f)
            data = states.get(state)
            print(f"[STATE] Retrieved data for state: {state}")
            return data
    except Exception as e:
        print(f"[STATE] Error retrieving data: {e}")
    return None

def clear_oauth_data(state):
    """Clear OAuth data from file"""
    try:
        if os.path.exists(STATE_FILE):
            with open(STATE_FILE, 'r') as f:
                states = json.load(f)
            if state in states:
                del states[state]
                with open(STATE_FILE, 'w') as f:
                    json.dump(states, f)
            print(f"[STATE] Cleared data for state: {state}")
    except Exception as e:
        print(f"[STATE] Error clearing data: {e}")

SCOPES = [
    "https://www.googleapis.com/auth/calendar",
    "https://www.googleapis.com/auth/calendar.events"
]

CLIENT_CONFIG = {
    "web": {
        "client_id": GOOGLE_CLIENT_ID,
        "client_secret": GOOGLE_CLIENT_SECRET,
        "auth_uri": "https://accounts.google.com/o/oauth2/auth",
        "token_uri": "https://oauth2.googleapis.com/token",
        "redirect_uris": [GOOGLE_REDIRECT_URI]
    }
}

# ---------------- GOOGLE CALENDAR UTILS ----------------
def get_calendar_service(credentials_dict):
    credentials = Credentials(
        token=credentials_dict['token'],
        refresh_token=credentials_dict.get('refresh_token'),
        token_uri=credentials_dict['token_uri'],
        client_id=credentials_dict['client_id'],
        client_secret=credentials_dict['client_secret'],
        scopes=credentials_dict.get('scopes')
    )
    return build("calendar", "v3", credentials=credentials)


# ---------------- AUTH ROUTES ----------------
@app.route("/")
def home():
    print("[HOME] Session contents:")
    print(f"[HOME] Session keys: {list(session.keys())}")
    print(f"[HOME] Has credentials: {'credentials' in session}")

    # Render a user-facing homepage with accessible UI and chat
    authenticated = 'credentials' in session
    return render_template('index.html', authenticated=authenticated)


@app.route("/login")
def login():
    flow = Flow.from_client_config(
        CLIENT_CONFIG,
        scopes=SCOPES,
        redirect_uri=GOOGLE_REDIRECT_URI
    )

    auth_url, state = flow.authorization_url(
        access_type="offline",
        include_granted_scopes="true"
    )

    # Save the state to file (indexed by state itself)
    save_oauth_data(state, {
        "state": state,
        "timestamp": datetime.now().isoformat()
    })
    
    print(f"[LOGIN] OAuth state: {state}")
    print(f"[LOGIN] Auth URL: {auth_url}")
    
    return redirect(auth_url)


@app.route("/oauth2callback")
def oauth2callback():
    # Get state from request parameters (returned by Google)
    request_state = request.args.get("state")
    
    print(f"[CALLBACK] Request state: {request_state}")
    print(f"[CALLBACK] Request URL: {request.url}")
    
    if not request_state:
        print("[CALLBACK] ERROR: No state in request")
        return "Missing state parameter", 400
    
    # Retrieve saved OAuth data using state
    oauth_data = get_oauth_data(request_state)
    
    if not oauth_data:
        print("[CALLBACK] ERROR: No saved OAuth data found for state")
        return "Session expired. Please login again.", 400
    
    print("[CALLBACK] State validation passed!")
    
    # Create flow with correct state for token exchange
    flow = Flow.from_client_config(
        CLIENT_CONFIG,
        scopes=SCOPES,
        redirect_uri=GOOGLE_REDIRECT_URI,
        state=request_state
    )

    try:
        print("[CALLBACK] Fetching token...")
        flow.fetch_token(authorization_response=request.url)
        print("[CALLBACK] Token fetched successfully")
    except Exception as e:
        print(f"[CALLBACK] ERROR fetching token: {str(e)}")
        clear_oauth_data(request_state)
        return f"Authentication error: {str(e)}", 400

    creds = flow.credentials

    # Store credentials in session
    session.permanent = True
    session["credentials"] = {
        "token": creds.token,
        "refresh_token": creds.refresh_token,
        "token_uri": creds.token_uri,
        "client_id": creds.client_id,
        "client_secret": creds.client_secret,
        "scopes": creds.scopes
    }
    session.modified = True
    
    print(f"[CALLBACK] Credentials stored in session")
    print(f"[CALLBACK] Session now has: {list(session.keys())}")
    
    # Clear the saved state after successful authentication
    clear_oauth_data(request_state)

    with open("token.json", "w") as f:
        f.write(creds.to_json())

    print("[CALLBACK] Authentication successful, redirecting to /")
    return redirect("/")


@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")


# ---------------- CHAT ROUTE ----------------
@app.route("/chat", methods=["POST"])
def chat():
    try:
        if "credentials" not in session:
            return jsonify({"error": "Not authenticated"}), 401

        data = request.get_json()
        user_message = data.get("message")

        # Import routing lazily to avoid heavy/optional deps at startup
        from router import route_message
        response = route_message(
            user_message=user_message,
            session=session
        )

        return jsonify(response)
    except Exception as e:
        import traceback
        err_msg = str(e)
        err_trace = traceback.format_exc()
        print(f"[CHAT ERROR] {err_msg}\n{err_trace}")
        return jsonify({"error": f"Server error: {err_msg}"}), 500


@app.route("/test-chat")
def test_chat():
    return jsonify({
        "status": "working",
        "message": "test-chat route is alive"
    })




@app.route("/_set_test_creds")
def _set_test_creds():
    try:
        with open("token.json") as f:
            creds = json.load(f)
    except Exception as e:
        return f"token.json error: {e}", 400

    session["credentials"] = {
        "token": creds.get("token") or creds.get("access_token"),
        "refresh_token": creds.get("refresh_token"),
        "token_uri": creds.get("token_uri"),
        "client_id": creds.get("client_id"),
        "client_secret": creds.get("client_secret"),
        "scopes": creds.get("scopes")
    }

    return "ok"


# ---------------- RUN ----------------
if __name__ == "__main__":
    app.run(port=5000, debug=True)
