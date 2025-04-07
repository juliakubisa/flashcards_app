from fastapi import APIRouter
from src.application.commands import CreateAccountCommand, CreateTokenCommand, RefreshTokenCommand, CreateTokenWithGoogleCommand
from src.application.model.input import CreateTokenRequest, CreateAccountRequest, RefreshTokenRequest, CreateTokenWithGoogleRequest
from src.application.model.output import TokenResponse
from src.web_api.dependencies import AccountRepositoryDependency, GoogleAuthServiceDependency, JWTTokenServiceDependency


router = APIRouter(prefix="/accounts", tags=['Accounts'])

@router.post('', status_code=201)
async def create_acccount(account_repository: AccountRepositoryDependency, request: CreateAccountRequest):
    command = CreateAccountCommand(account_repository)
    command.handle(request)

@router.post('/token')
async def login(account_repository: AccountRepositoryDependency, token_service: JWTTokenServiceDependency, request: CreateTokenRequest) -> TokenResponse:
    command = CreateTokenCommand(account_repository, token_service)
    token_response = command.handle(request)
    return token_response

@router.post('/token/google')
async def login_with_google(account_repository: AccountRepositoryDependency, token_service: JWTTokenServiceDependency, google_auth_service: GoogleAuthServiceDependency, request: CreateTokenWithGoogleRequest) -> TokenResponse:
    command = CreateTokenWithGoogleCommand(account_repository, token_service, google_auth_service)
    token_response = command.handle(request)
    return token_response

@router.post('/token/refresh')
async def refresh_token(account_repository: AccountRepositoryDependency, token_service: JWTTokenServiceDependency, request: RefreshTokenRequest) -> TokenResponse:
    command = RefreshTokenCommand(account_repository, token_service)
    token_response = command.handle(request)
    return token_response
