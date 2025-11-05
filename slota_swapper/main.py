import os
from typing import Annotated

from dotenv import load_dotenv

# Load environment variables early
load_dotenv()

from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from fastapi.middleware.cors import CORSMiddleware

from slota_swapper.database import create_db_and_tables, get_db
from slota_swapper.routers.auth import auth_router
from slota_swapper.routers.events import events_router
from slota_swapper.routers.swaps import swaps_router
from slota_swapper.auth.jwt_handler import decode_access_token
from slota_swapper.models.user import User


app = FastAPI(title="SlotSwapper API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")


def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)],
    db: Session = Depends(get_db),
) -> User:
    token_data = decode_access_token(token)
    if token_data is None or token_data.user_id is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid or expired token")

    user: User | None = db.query(User).filter(User.id == token_data.user_id).first()
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")
    return user


@app.on_event("startup")
def on_startup() -> None:
    create_db_and_tables()


@app.on_event("shutdown")
def on_shutdown() -> None:
    # Add graceful shutdown logic if needed
    pass


app.include_router(auth_router)
app.include_router(events_router)
app.include_router(swaps_router)
