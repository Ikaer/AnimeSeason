import os
import json
from typing import Any, Optional
from requests_oauthlib import OAuth2Session
import secrets
import base64

class MALAuth:
    def __init__(self, client_id, redirect_uri, auth_url, token_url):
        self.token_file = 'mal_token.json'
        self.client_id = client_id
        self.redirect_uri = redirect_uri
        self.auth_url = auth_url
        self.token_url = token_url

    def is_mal_token_valid(token: Optional[dict[str, Any]] = None) -> bool:
        import requests
        try:
            headers = {"Authorization": f"Bearer {token['access_token'] if isinstance(token, dict) else token}"}
            resp = requests.get("https://api.myanimelist.net/v2/users/@me", headers=headers)
            if resp.status_code == 401:
                return False
            resp.raise_for_status()
            return True
        except Exception:
            return False

    def generate_code_verifier(self):
        code_verifier = base64.urlsafe_b64encode(secrets.token_bytes(32)).rstrip(b'=').decode('utf-8')
        while len(code_verifier) < 43:
            code_verifier += "A"
        return code_verifier

    def authorize(self, code_verifier: str) -> tuple[str, str, str]:
        code_verifier = self.generate_code_verifier()
        oauth = OAuth2Session(self.client_id, redirect_uri=self.redirect_uri)
        auth_url, state = oauth.authorization_url(
            self.auth_url,
            code_challenge=code_verifier,
            code_challenge_method='plain'
        )
        return auth_url, state, code_verifier

    def get_token(self, code: str, returned_state: str,original_state: str, code_verifier: str) -> dict[str, Any]:

        if not code or not returned_state or not original_state or not code_verifier:
            raise ValueError("Code, state, or code_verifier is missing. Cannot proceed with token retrieval.")
        
        if returned_state != original_state:
            raise ValueError("State mismatch. Possible CSRF attack or session tampering.")
        
        oauth = OAuth2Session(self.client_id, redirect_uri=self.redirect_uri)
        token = oauth.fetch_token(
            self.token_url,
            code=code,
            include_client_id=True,
            code_verifier=code_verifier
        )
        return token

    def save_token(self, token: dict[str, Any]) -> None:
        with open(self.token_file, 'w', encoding='utf-8') as f:
            json.dump(token, f)
        
    def load_token(self) -> Optional[dict[str, Any]]:
        if os.path.exists(self.token_file):
            with open(self.token_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        return None




_mal_auth_instance: Optional['MALAuth'] = None


def init_mal_auth(client_id:str, redirect_uri:str, auth_url:str, token_url:str) -> None:
    global _mal_auth_instance
    _mal_auth_instance = MALAuth(client_id, redirect_uri, auth_url, token_url)

def get_mal_auth() -> 'MALAuth':
    if _mal_auth_instance is None:
        raise RuntimeError("MALAuth not initialized. Call init_mal_auth(config) first.")
    return _mal_auth_instance