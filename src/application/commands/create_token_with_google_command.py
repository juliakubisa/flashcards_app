import secrets
import string
import bcrypt
from src.application.model.input import CreateTokenWithGoogleRequest
from src.application.model.output import TokenResponse
from src.domain.entities import Account
from src.domain.exceptions import FieldEmptyException
from src.infrastructure.database.repositories import AccountRepository
from src.infrastructure.services import JWTTokenService, GoogleAuthService


class CreateTokenWithGoogleCommand:
    def __init__(self, repository: AccountRepository, token_service: JWTTokenService, google_auth_service: GoogleAuthService):
        self.repository = repository
        self.token_service = token_service
        self.google_auth_service = google_auth_service

    def handle(self, request: CreateTokenWithGoogleRequest) -> TokenResponse:
        if request.id_token is None:
            raise FieldEmptyException("Google idToken is required")
        
        decoded_token = self.google_auth_service.decode_token(request.id_token)

        user_google_id = decoded_token['sub']
        user_email = decoded_token['email']
        account = self.repository.get_by_google_id(user_google_id)

        if not account:
            account = Account(decoded_token['name'], user_email, self.__generate_random_password())
            account.google_id = user_google_id
            self.repository.add(account)

        access_token = self.token_service.generate_access_token(user_email)
        refresh_token = self.token_service.generate_refresh_token(user_email)

        account.refresh_token = refresh_token
        self.repository.save_changes(account)

        return TokenResponse(access_token=access_token, refresh_token=account.refresh_token, email=account.email, name=account.name)
    
    def __generate_random_password(self) -> str:
        alphabet = string.ascii_letters + string.digits
        password = ''.join(secrets.choice(alphabet) for i in range(20))
        return password