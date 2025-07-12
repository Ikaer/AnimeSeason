import os
import json
import time
from typing import Any, Optional
import urllib.parse
from requests_oauthlib import OAuth2Session
import secrets
import base64



class PCKEMalAuth:
    def __init__(self, client_id: str, redirect_uri: str, auth_url: str, token_url: str):
        self.token_file = 'mal_token_pcke.json'
        self.client_id = client_id
        self.redirect_uri = redirect_uri
        self.auth_url = auth_url
        self.token_url = token_url
        self.token = None
        self.session = None
        self._load_token()

    def _load_token(self):
        if os.path.exists(self.token_file):
            with open(self.token_file, 'r', encoding='utf-8') as f:
                self.token = json.load(f)
        else:
            self.token = None

    def _save_token(self, token: dict[str, Any]) -> None:
        with open(self.token_file, 'w', encoding='utf-8') as f:
            json.dump(token, f)
        self.token = token

    def is_token_valid(self) -> bool:
        if not self.token:
            return False
        expires_at = self.token.get('expires_at')
        if not expires_at:
            return False
        return expires_at > time.time() + 60  # 60s buffer

    def pcke_is_token_valid(self):
        if not self.token:
            return False
        expires_at = self.token.get('expires_at')
        if not expires_at:
            return False
        return expires_at > time.time() + 60  # 60s buffer

    def pcke_refresh_token(self):
        refresh_token = self.token.get('refresh_token')
        if not refresh_token:
            return False
        print('Refreshing MAL access token...')
        oauth = OAuth2Session(self.client_id, redirect_uri=self.redirect_uri, token=self.token)
        try:
            new_token = oauth.refresh_token(
                self.token_url,
                refresh_token=refresh_token,
                client_id=self.client_id,
            )
            # Add expires_at if not present
            if 'expires_in' in new_token:
                new_token['expires_at'] = time.time() + int(new_token['expires_in'])
            self._save_token(new_token)
            print('Token refreshed.')
            return True
        except Exception as e:
            print('Failed to refresh token:', e)
            return False

    def pcke_authenticate(self):
        if self.pcke_is_token_valid():
            return self.token['access_token']
        if self.token and self.pcke_refresh_token() and self.pcke_is_token_valid():
            return self.token['access_token']
        # PKCE plain method
        code_verifier = base64.urlsafe_b64encode(secrets.token_bytes(32)).rstrip(b'=').decode('utf-8')
        code_challenge = code_verifier
        extra = {'code_challenge': code_challenge, 'code_challenge_method': 'plain'}
        oauth = OAuth2Session(self.client_id, redirect_uri=self.redirect_uri)
        print("""
==== MAL OAuth2 Authentication ====
1. Open the URL below in your browser and log in to MyAnimeList.
2. After authorizing, you will be redirected to your redirect_uri with ?code=... (the page will fail to load, that's OK).
3. Copy the full URL from the address bar and paste it below.
""")
        auth_url, state = oauth.authorization_url(self.auth_url, **extra)
        print(f"Go to the following URL and authorize access:\n{auth_url}\n")
        url = input("Paste the FULL redirect URL from your browser's address bar here: ")
        parsed = urllib.parse.urlparse(url.strip())
        params = urllib.parse.parse_qs(parsed.query)
        code = params.get('code', [None])[0]
        if not code:
            print("Could not find 'code' in the URL. Please try again.")
            exit(1)
        try:
            token = oauth.fetch_token(
                self.token_url,
                code=code,
                include_client_id=True,
                code_verifier=code_verifier,
                client_secret=None
            )
            # Add expires_at for easier checking
            if 'expires_in' in token:
                token['expires_at'] = time.time() + int(token['expires_in'])
            self._save_token(token)
            print('Authentication successful.')
            return token['access_token']
        except Exception as e:
            print('Authentication failed. Please check your redirect_uri and credentials.')
            print(e)
            exit(1)