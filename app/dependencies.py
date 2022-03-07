from datetime import datetime, timedelta

from typing import Optional

import logging
from logging.config import dictConfig

from jose import JWTError, jwt

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

from passlib.context import CryptContext

from config import ALGORITHM, SQLALCHEMY_DATABASE_URL, SECRET_KEY
from dao.user import get_user_by_email
from models.orm import Base
from models.schema import User, TokenData

from config import LogConfig, APP_NAME, DB_ARGS, JWT_EXPIRE_MINUTES_DEFAULT


dictConfig(LogConfig().dict())
logger = logging.getLogger(APP_NAME)

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/token")

db_engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args=DB_ARGS
)

db_session = sessionmaker(autocommit=False, autoflush=False, bind=db_engine)

Base.metadata.create_all(bind=db_engine)


def get_db():
    db = db_session()
    try:
        yield db
    finally:
        db.close()


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=JWT_EXPIRE_MINUTES_DEFAULT)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def authenticate_user(username: str, password: str, db: Session):
    user = get_user_by_email(db, username)
    if not user:
        return False
    # pwd_context.hash(password) == user.hashed_password
    if pwd_context.verify(password, user.hashed_password):
        return user
    return False


def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    user = get_user_by_email(db, username)
    if user is None:
        logger.error('get_user_by_email(%s)' % username)
        raise credentials_exception
    return user


def get_current_active_user(current_user: User = Depends(get_current_user)):
    if not current_user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user
