from fastapi import APIRouter, Depends, Response

from sqlalchemy.orm import Session

from dependencies import get_current_active_user, get_db, pwd_context
from models.schema import User, UserCreate
from dao.user import create_user

router = APIRouter(
    prefix="/users",
    tags=["users"],
    responses={
        201: {"description": "Created"},
        404: {"description": "Not found"}
    }
)


@router.post("/", tags=["users"])
def new_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user = create_user(db, pwd_context, user)
    return Response(status_code=201)


@router.get("/me/", response_model=User)
def read_users_me(current_user: User = Depends(get_current_active_user)):
    return current_user
