import secrets
import base64
from requests_oauthlib import OAuth2Session

CLIENT_ID = "c142d107081a1ebf47f93cfd4d6acede"
REDIRECT_URI = "http://localhost:12345/mal/callback"
AUTH_URL = "https://myanimelist.net/v1/oauth2/authorize"
TOKEN_URL = "https://myanimelist.net/v1/oauth2/token"

# Generate a valid code_verifier (43+ chars)
code_verifier = base64.urlsafe_b64encode(secrets.token_bytes(32)).rstrip(b'=').decode('utf-8')
while len(code_verifier) < 43:
    code_verifier += "A"  # pad if needed

oauth = OAuth2Session(CLIENT_ID, redirect_uri=REDIRECT_URI)
auth_url, state = oauth.authorization_url(
    AUTH_URL,
    code_challenge_method='plain',
    code_challenge=code_verifier
)
print("Go to:", auth_url)
# After authorizing, paste the ?code=... value here:
code = input("Enter code: ")
token = oauth.fetch_token(
    TOKEN_URL,
    code=code,
    include_client_id=True,
    code_verifier=code_verifier
)
print(token)