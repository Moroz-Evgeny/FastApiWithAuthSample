from api.auth.create_jwt import create_access_token, create_refresh_token

from db.session import get_db
from db.models import User
 
from api.auth.utils import _authenticate_user, _get_current_user_from_refresh_token
from api.schemas import Token

from fastapi import APIRouter, Request, Response, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from sqlalchemy.ext.asyncio import AsyncSession

from typing import Union

login_router = APIRouter()

@login_router.post('/', response_model=Token)
async def login_for_acess_token(
  response: Response,
  form_data: OAuth2PasswordRequestForm = Depends(),
  db: AsyncSession = Depends(get_db)) -> Token:
  user = await _authenticate_user(login=form_data.username, user_password=form_data.password, session=db)
  if user is None:
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=f"Incorrect username or password")
  
  access_token = create_access_token(
    data={"type": "access","sub": user.login , "id": str(user.id), "role": user.role}
  )
  refresh_token = create_refresh_token(
    data={"type": "refresh","sub": user.login, "id": str(user.id), "role": user.role}
  )

  response.set_cookie(
    key="refresh_token",
    value=refresh_token,
    httponly=True,  
    # secure=True,              # Только HTTPS
    samesite=None, 
    max_age=60 * 60 * 24 * 7
  )
  return Token(access_token=access_token, token_type='bearer')

@login_router.post("/refresh", response_model=Token)
async def refresh_token(request: Request, response: Response, session: AsyncSession = Depends(get_db)) -> Union[None, Token]:
  try:
    print('-'*100)
    token = request.cookies.get("refresh_token")
    print(token, request.cookies)
    user = await _get_current_user_from_refresh_token(token=token, session=session)
    print(user)
    access_token = create_access_token(
      data={"type": "access","sub": user.login , "id": str(user.id), "role": user.role}
    )
    refresh_token = create_refresh_token(
      data={"type": "refresh","sub": user.login, "id": str(user.id), "role": user.role}
    )
    
    response.set_cookie(
      key="refresh_token",
      value=refresh_token,
      httponly=True,  
      # secure=True,              # Только HTTPS
      samesite=None, 
      max_age=60 * 60 * 24 * 7
    )
  except:
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
    )
  return Token(access_token=access_token, token_type='bearer')



