from fastapi import Request, Depends, status
from jose import jwt, JWTError, ExpiredSignatureError

from app.config import settings
from app.users.dao import UserDAO
from app.exceptions import TokenAbsentException, IncorrectTokenFormatException, TokenExpiredException, \
    UserIsNotPresentException


def get_token(request: Request):
    token = request.cookies.get("candle_access_token")
    if not token:
        raise TokenAbsentException
    return token


async def get_current_user(token: str = Depends(get_token)):
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, settings.ALGORITHM
        )
    except ExpiredSignatureError:
        # Как позже выяснилось, ключ exp автоматически проверяется
        # командой jwt.decode, поэтому отдельно проверять это не нужно
        raise TokenExpiredException
    except JWTError:
        raise IncorrectTokenFormatException
    user_id: str = payload.get("sub")
    if not user_id:
        raise UserIsNotPresentException
    user = await UserDAO.find_one_or_none(id=int(user_id))
    if not user:
        raise UserIsNotPresentException

    return user
