from google.oauth2 import id_token as google_id_token
from google.auth.transport import requests as google_requests
from src.domain.exceptions import TokenInvalidException


class GoogleAuthService():
    def __init__(self, google_client_id: str):
        self.google_client_id = google_client_id

    def decode_token(self, token: str) -> None:
        try:
            payload = google_id_token.verify_oauth2_token(token, google_requests.Request(), self.google_client_id)
            return payload
        except ValueError:
            raise TokenInvalidException("Google token is invalid")