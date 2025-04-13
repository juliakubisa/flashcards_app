import datetime
import jwt
from src.domain.exceptions import TokenExpiredException, TokenInvalidException


class JWTTokenService():
    def __init__(self, jwt_secret: str, access_token_age_seconds: int, refresh_token_age_seconds: int):
        self.jwt_secret = jwt_secret
        self.access_token_age_seconds = access_token_age_seconds
        self.refresh_token_age_seconds = refresh_token_age_seconds

    def generate_access_token(self, email: str) -> str:
        token_payload = {
            'email': email,
            'exp': datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(seconds=self.access_token_age_seconds),
            'token_type': 'access'
        }
        
        token = jwt.encode(token_payload, self.jwt_secret, algorithm='HS256')

        return token

    def generate_refresh_token(self, email: str) -> str:
        token_payload = {
            'email': email,
            'exp': datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(seconds=self.refresh_token_age_seconds),
            'token_type': 'refresh'
        }
        
        token = jwt.encode(token_payload, self.jwt_secret, algorithm='HS256')

        return token
    
    def decode_token(self, token: str) -> dict:
        try:
            return jwt.decode(token, self.jwt_secret, algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise TokenExpiredException('Token has expired')
        except jwt.InvalidTokenError:
            raise TokenInvalidException('Token is invalid')