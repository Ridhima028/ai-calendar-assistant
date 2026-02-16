import os
import json
# Force intent detection to a known value for testing (bypass Gemini)
os.environ['TEST_INTENT'] = 'create_event'
from router import route_message

try:
    with open('token.json','r') as f:
        creds = json.load(f)
except Exception as e:
    print('Could not load token.json:', e)
    raise SystemExit(1)

session = {
    'credentials': {
        'token': creds.get('token') or creds.get('access_token'),
        'refresh_token': creds.get('refresh_token'),
        'token_uri': creds.get('token_uri'),
        'client_id': creds.get('client_id'),
        'client_secret': creds.get('client_secret'),
        'scopes': creds.get('scopes')
    }
}

message = 'Create a meeting tomorrow at 3pm for 30 minutes'
print('Sending message:', message)
resp = route_message(user_message=message, session=session)
print('Response:', resp)
