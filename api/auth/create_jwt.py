from datetime import datetime
from datetime import timedelta

from jose import jwt

import settings

def create_access_token(data: dict):
  to_encode = data.copy()
  expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES) 

  to_encode.update({"exp": expire})
  encoded_iwt = jwt.encode(
    to_encode, settings.ACCESS_SECRET_KEY, algorithm=settings.ALGORITHM
  )
  return encoded_iwt

def create_refresh_token(data: dict):
  to_encode = data.copy()
  expire = datetime.utcnow() + timedelta(minutes=settings.REFRESH_TOKEN_EXPIRE_DAYS) 

  to_encode.update({"exp": expire})
  encoded_iwt = jwt.encode(
    to_encode, settings.REFRESH_SECRET_KEY, algorithm=settings.ALGORITHM
  )
  return encoded_iwt