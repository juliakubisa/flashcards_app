from fastapi import APIRouter, Request, Response
from src.application.commands import CreateAccountCommand, CreateTokenCommand, RefreshTokenCommand, CreateTokenWithGoogleCommand
from src.application.model.input import CreateTokenRequest, CreateAccountRequest, CreateTokenWithGoogleRequest
from src.application.model.output import TokenResponse
from src.web_api.dependencies import AccountRepositoryDependency, GoogleAuthServiceDependency, JWTTokenServiceDependency, ImageStorageServiceDependency
from src.web_api.settings import Settings


router = APIRouter(prefix="/accounts", tags=['Accounts'])

@router.post('', status_code=201)
async def create_acccount(account_repository: AccountRepositoryDependency, request: CreateAccountRequest):
    command = CreateAccountCommand(account_repository)
    command.handle(request)

@router.post('/token')
async def login(account_repository: AccountRepositoryDependency, 
                token_service: JWTTokenServiceDependency, 
                image_storage_service: ImageStorageServiceDependency,
                request: CreateTokenRequest, 
                response: Response) -> TokenResponse:
    command = CreateTokenCommand(account_repository, token_service, image_storage_service)
    token_response, refresh_token = command.handle(request)

    set_refresh_token_cookie(refresh_token, response)

    return token_response

@router.post('/token/google')
async def login_with_google(account_repository: AccountRepositoryDependency, 
                            token_service: JWTTokenServiceDependency, 
                            google_auth_service: GoogleAuthServiceDependency, 
                            image_storage_service: ImageStorageServiceDependency,
                            request: CreateTokenWithGoogleRequest,
                            response: Response) -> TokenResponse:
    command = CreateTokenWithGoogleCommand(account_repository, token_service, google_auth_service, image_storage_service)
    token_response, refresh_token = command.handle(request)

    set_refresh_token_cookie(refresh_token, response)

    return token_response

@router.post('/token/refresh')
async def refresh_token(request: Request, 
                        account_repository: AccountRepositoryDependency, 
                        token_service: JWTTokenServiceDependency,
                        image_storage_service: ImageStorageServiceDependency,
                        response: Response) -> TokenResponse:
    command = RefreshTokenCommand(account_repository, token_service, image_storage_service)
    
    refresh_token = request.cookies.get('refresh_token')
    token_response, refresh_token = command.handle(refresh_token)

    set_refresh_token_cookie(refresh_token, response)

    return token_response

def set_refresh_token_cookie(refresh_token: str, response: Response):
    settings = Settings.load()
    response.set_cookie(key='refresh_token', 
                        value=refresh_token, 
                        httponly=True, 
                        secure=True, 
                        path='/accounts/token/refresh',
                        domain=settings.domain,
                        samesite='none',
                        max_age=settings.refresh_token_age_seconds)

