from fastapi import Depends, HTTPException, Request
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from src.web_api.dependencies import AccountRepositoryDependency, JWTTokenServiceDependency


def authenticate(request: Request, 
                 token_service: JWTTokenServiceDependency, 
                 account_repository: AccountRepositoryDependency, 
                 auth_header: HTTPAuthorizationCredentials = Depends(HTTPBearer(auto_error=False))):
    if auth_header is None:
        raise HTTPException(status_code=401, detail='Token is required')
    
    token = auth_header.credentials

    token_payload = token_service.decode_token(token)

    account = account_repository.get_by_email(token_payload['email'])

    if account is None:
        raise HTTPException(status_code=401, detail='No such account')
    
    request.state.account_id = account.id


