from fastapi import APIRouter, Response, Depends

from app.users.schemas import SUserAuth
from app.users.dao import UserDAO
from app.users.auth import get_password_hash, authenticate_user, create_access_token
from app.users.dependencies import get_current_user
from app.users.models import Users
from app.exceptions import UserAlreadyExistsException, IncorrectEmailOrPasswordException, CannotAddDataToDatabase

router = APIRouter(
    prefix="/auth",
    tags=["Аутентификация и Пользователи"]
)


@router.post("/register", status_code=201)
async def register_user(user_data: SUserAuth):
    existing_user = await UserDAO.find_one_or_none(email=user_data.email)
    if existing_user:
        raise UserAlreadyExistsException
    hashed_password = get_password_hash(user_data.password)
    new_user = await UserDAO.add(email=user_data.email, hashed_password=hashed_password)
    if not new_user:
        raise CannotAddDataToDatabase


@router.post("/login")
async def login_user(response: Response, user_data: SUserAuth):
    user = await authenticate_user(user_data.email, user_data.password)
    if not user:
        raise IncorrectEmailOrPasswordException
    access_token = create_access_token({"sub": str(user.id)})
    response.set_cookie("candle_access_token", access_token, httponly=True)
    return {"access_token": access_token}


@router.post("/logout")
async def logout_user(response: Response):
    response.delete_cookie("candle_access_token")


@router.get("/me")
async def read_users_me(current_user: Users = Depends(get_current_user)):
    return current_user


@router.get("/all")
async def read_all_users():
    return await UserDAO.find_all()





