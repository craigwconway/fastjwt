from datetime import timedelta

from sqlalchemy.orm import Session

from fastapi.security import OAuth2PasswordRequestForm as OAuthForm
from fastapi import APIRouter, Depends, HTTPException, status

from config import JWT_EXPIRE_MINUTES_DEFAULT
from dependencies import authenticate_user, create_access_token, get_db, logger

from models.schema import Token

router = APIRouter(
    prefix="/auth",
    tags=["auth"]
)


@router.post("/token", response_model=Token)
def login_for_access_token(form_data: OAuthForm = Depends(), db: Session = Depends(get_db)):
    logger.debug('token request: %s' % form_data.username)
    user = authenticate_user(form_data.username, form_data.password, db)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=JWT_EXPIRE_MINUTES_DEFAULT)
    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    logger.info('token granted: %s', user.email)
    return {"access_token": access_token, "token_type": "bearer"}
