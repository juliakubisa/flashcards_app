import bcrypt
from src.application.model.input import CreateTokenRequest
from src.application.model.output import TokenResponse
from src.domain.exceptions import FieldEmptyException, NotExistsException
from src.infrastructure.database.repositories import AccountRepository
from src.infrastructure.services import JWTTokenService

class CreateTokenCommand:
    def __init__(self, repository: AccountRepository, token_service: JWTTokenService):
        self.repository = repository
        self.token_service = token_service

    def handle(self, request: CreateTokenRequest) -> TokenResponse:
        if request.email is None:
            raise FieldEmptyException("Email is required")
        if request.password is None:
            raise FieldEmptyException("Password is required")
        
        account = self.repository.get_by_email(request.email)

        if not account or not bcrypt.checkpw(request.password.encode('utf-8'), account.password.encode('utf-8')):
            raise NotExistsException("Account with such email or password does not exist")
        
        access_token = self.token_service.generate_access_token(account.email)
        account.refresh_token = self.token_service.generate_refresh_token(account.email)
        self.repository.save_changes(account)

        return TokenResponse(access_token=access_token, refresh_token=account.refresh_token, email=account.email, name=account.name)