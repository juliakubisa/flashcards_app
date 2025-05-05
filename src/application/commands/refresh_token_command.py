from src.application.model.output import TokenResponse
from src.domain.exceptions import FieldEmptyException, TokenInvalidException
from src.infrastructure.database.repositories import AccountRepository
from src.infrastructure.services import JWTTokenService, ImageStorageService

class RefreshTokenCommand:
    def __init__(self, repository: AccountRepository, token_service: JWTTokenService, image_storage_service: ImageStorageService):
        self.repository = repository
        self.token_service = token_service
        self.image_storage_service = image_storage_service

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

        # Image URL also needs to be refreshed because of the non-infinite expiration time
        user_image_url = self.image_storage_service.get_account_image_url(account.id)

        return (TokenResponse(access_token=access_token, email=account.email, name=account.name, image_url=user_image_url), account.refresh_token)