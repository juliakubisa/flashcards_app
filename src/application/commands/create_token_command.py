import bcrypt
from src.application.model.input import CreateTokenRequest
from src.application.model.output import TokenResponse
from src.domain.exceptions import FieldEmptyException, NotExistsException
from src.infrastructure.database.repositories import AccountRepository
from src.infrastructure.services import JWTTokenService, ImageStorageService

class CreateTokenCommand:
    def __init__(self, repository: AccountRepository, token_service: JWTTokenService, image_storage_service: ImageStorageService):
        self.repository = repository
        self.token_service = token_service
        self.image_storage_service = image_storage_service

    def handle(self, request: CreateTokenRequest) -> tuple[TokenResponse, str]:
        if request.email is None:
            raise FieldEmptyException("Email is required")
        if request.password is None:
            raise FieldEmptyException("Password is required")
        
        account = self.repository.get_by_email(request.email)

        if not account or not bcrypt.checkpw(request.password.encode('utf-8'), account.password.encode('utf-8')):
            raise NotExistsException("Account does not exist")
        
        access_token = self.token_service.generate_access_token(account.email)
        account.refresh_token = self.token_service.generate_refresh_token(account.email)
        self.repository.save_changes(account)

        image_url = self.image_storage_service.get_account_image_url(account.id)

        return (TokenResponse(access_token=access_token, email=account.email, name=account.name, image_url=image_url), account.refresh_token)