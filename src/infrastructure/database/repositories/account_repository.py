from sqlalchemy.orm import Session
from src.domain.entities.account import Account


class AccountRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_email(self, email: str) -> Account | None:
        return (self.db.query(Account)
                .filter(Account.email == email)
                .one_or_none())
    
    def get_by_refresh_token_and_email(self, refresh_token: str, email: str) -> Account | None:
        return (self.db.query(Account)
                .filter(Account.email == email and Account.refresh_token == refresh_token)
                .one_or_none())
    
    def get_by_google_id(self, google_id: str) -> Account | None:
        return (self.db.query(Account)
                .filter(Account.google_id == google_id)
                .one_or_none())
    
    def add(self, account: Account) -> None:
        self.db.add(account)
        self.db.commit()
        self.db.refresh(account)

    def save_changes(self, account: Account) -> None:
        self.db.commit()
        self.db.refresh(account)
