from sqlalchemy.orm import Session
from typing import Optional
from ..models.user import User
from ..core.security import get_password_hash, verify_password
from fastapi import HTTPException, status

class UserService:
    @staticmethod
    def get_user(db: Session, user_id: int) -> Optional[User]:
        return db.query(User).filter(User.id == user_id).first()

    @staticmethod
    def get_user_by_email(db: Session, email: str) -> Optional[User]:
        return db.query(User).filter(User.email == email).first()

    @staticmethod
    def get_user_by_username(db: Session, username: str) -> Optional[User]:
        return db.query(User).filter(User.username == username).first()

    @staticmethod
    def create_user(db: Session, email: str, username: str, password: str, full_name: str) -> User:
        hashed_password = get_password_hash(password)
        db_user = User(
            email=email,
            username=username,
            hashed_password=hashed_password,
            full_name=full_name
        )
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user

    @staticmethod
    def authenticate_user(db: Session, email: str, password: str) -> Optional[User]:
        user = UserService.get_user_by_email(db, email)
        if not user:
            return None
        if not verify_password(password, user.hashed_password):
            return None
        return user

    @staticmethod
    def update_user_wallet(db: Session, user_id: int, wallet_address: str) -> User:
        user = UserService.get_user(db, user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        user.wallet_address = wallet_address
        db.commit()
        db.refresh(user)
        return user 