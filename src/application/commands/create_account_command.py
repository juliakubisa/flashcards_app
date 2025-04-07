import bcrypt
from src.application.model.input import CreateAccountRequest
from src.domain.entities import Account
from src.domain.exceptions import FieldEmptyException, DuplicateException
from src.infrastructure.database.repositories import AccountRepository

class CreateAccountCommand:
    def __init__(self, repository: AccountRepository):
        self.repository = repository

    def handle(self, request: CreateAccountRequest) -> None:
        if request.name is None:
            raise FieldEmptyException("Name is required")
        if request.email is None:
            raise FieldEmptyException("Email is required")
        if request.password is None:
            raise FieldEmptyException("Password is required")
        
        existing_account = self.repository.get_by_email(request.email)

        if existing_account is not None:
            raise DuplicateException("Account with such email already exists")
        
        hashed_password = bcrypt.hashpw(request.password.encode('utf-8'), bcrypt.gensalt()).decode()
        new_account = Account(request.name, request.email, hashed_password)

        self.repository.add(new_account)