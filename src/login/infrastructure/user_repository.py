from sqlalchemy.orm import Session
from ..domain.user import User

class UserRepository:
    def __init__(self, session: Session):
        self.session = session

    def get_by_email(self, email: str) -> User:
        return self.session.query(User).filter(User.email == email).first()

    def add(self, user: User):
        self.session.add(user)
        self.session.commit()