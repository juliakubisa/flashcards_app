from src.application.model.output import TokenResponse
from src.domain.exceptions import FieldEmptyException, TokenInvalidException
from src.infrastructure.database.repositories import AccountRepository
from src.infrastructure.services import JWTTokenService

class RefreshTokenCommand:
    def __init__(self, repository: AccountRepository, token_service: JWTTokenService):
        self.repository = repository
        self.token_service = token_service

    def handle(self, refresh_token: str) -> tuple[TokenResponse, str]:
        if refresh_token is None:
            raise FieldEmptyException("Refresh token is required")

        decoded_token = self.token_service.decode_token(refresh_token)

        account = self.repository.get_by_refresh_token_and_email(refresh_token, decoded_token['email'])

        if not account:
            raise TokenInvalidException("Invalid refresh token")
        
        access_token = self.token_service.generate_access_token(account.email)
        account.refresh_token = self.token_service.generate_refresh_token(account.email)

        self.repository.save_changes(account)

        return (TokenResponse(access_token=access_token, email=account.email, name=account.name), account.refresh_token)