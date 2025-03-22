from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from pydantic import BaseModel

from ..core.database import get_db
from ..services.user_service import UserService
from ..models.user import User
from .auth import get_current_user

router = APIRouter()

class UserCreate(BaseModel):
    email: str
    username: str
    password: str
    full_name: str

class UserUpdate(BaseModel):
    full_name: str = None
    wallet_address: str = None

@router.post("/users/", response_model=User)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user = UserService.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    return UserService.create_user(
        db=db,
        email=user.email,
        username=user.username,
        password=user.password,
        full_name=user.full_name
    )

@router.get("/users/", response_model=List[User])
def read_users(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    users = db.query(User).offset(skip).limit(limit).all()
    return users

@router.get("/users/{user_id}", response_model=User)
def read_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    db_user = UserService.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    return db_user

@router.put("/users/{user_id}", response_model=User)
def update_user(
    user_id: int,
    user_update: UserUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    db_user = UserService.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    if user_update.full_name is not None:
        db_user.full_name = user_update.full_name
    if user_update.wallet_address is not None:
        db_user.wallet_address = user_update.wallet_address
    
    db.commit()
    db.refresh(db_user)
    return db_user 