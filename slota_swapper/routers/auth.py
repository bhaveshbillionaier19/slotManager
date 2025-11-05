from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from slota_swapper.database import get_db
from slota_swapper.models.user import User
from slota_swapper.schemas.user_schemas import UserCreate, UserLogin
from slota_swapper.schemas.auth_schemas import Token
from slota_swapper.auth import security
from slota_swapper.auth import jwt_handler


auth_router = APIRouter(prefix="/auth", tags=["Auth"])


@auth_router.post("/signup", response_model=Token, status_code=status.HTTP_201_CREATED)
def signup(payload: UserCreate, db: Session = Depends(get_db)):
    password_hash = security.get_password_hash(payload.password)
    user = User(email=payload.email, password_hash=password_hash, name=payload.name)

    try:
        db.add(user)
        db.commit()
        db.refresh(user)
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered",
        )

    token = jwt_handler.create_access_token({"user_id": str(user.id)})
    return Token(access_token=token)


@auth_router.post("/login", response_model=Token)
def login(payload: UserLogin, db: Session = Depends(get_db)):
    user: User | None = db.query(User).filter(User.email == payload.email).first()
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")

    if not security.verify_password(payload.password, user.password_hash):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")

    token = jwt_handler.create_access_token({"user_id": str(user.id)})
    return Token(access_token=token)


