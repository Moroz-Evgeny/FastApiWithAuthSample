from uuid import UUID
import settings

from typing import Union

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

from api.hasher import Hasher

from db.dals import UserDAL
from db.models import User
from db.session import get_db

from sqlalchemy.ext.asyncio import AsyncSession

from jose import jwt


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")

async def _get_user_by_login_for_token(login: str, session) -> Union[None, User]:
    async with session.begin():
        user_dal = UserDAL(session)
        user = await user_dal.get_user_by_login(login=login)
        if user is not None:
            return user

async def _authenticate_user(login: str, user_password: str, session) -> Union[None, User]:
    async with session.begin():
      user_dal = UserDAL(session)
      user = await user_dal.get_user_by_login(login=login)
      if user is None:
          return None
      if Hasher.verify_password(user_password, user.hashed_password) == False:
          return None
      return user

async def _get_current_user_from_access_token(token: str = Depends(oauth2_scheme), session: AsyncSession = Depends(get_db)) -> Union[User, None]:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
    )
    try:
        payload = jwt.decode(
            token,
            settings.ACCESS_SECRET_KEY,
            algorithms=[settings.ALGORITHM]
        )
        id: str = payload.get("id")
        if id is None:
            raise credentials_exception
    except:
        raise credentials_exception
    async with session.begin():
        user_dal = UserDAL(session)
        user = await user_dal.get_user_by_id(id=id)
    if user is None:
        raise credentials_exception
    return user

async def _get_current_user_from_refresh_token(token: str, session) -> Union[User, None]:
    print('-'*100)  
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
    )
    try:
        payload = jwt.decode(
            token,
            settings.REFRESH_SECRET_KEY,
            algorithms=[settings.ALGORITHM]
        )
        print(payload)
        id: str = payload.get("id")
        if id is None:
            raise credentials_exception
    except:
        raise credentials_exception
    async with session.begin():
        user_dal = UserDAL(session)
        user = await user_dal.get_user_by_id(id=id)
        print(user)
    if user is None:
        raise credentials_exception
    return user