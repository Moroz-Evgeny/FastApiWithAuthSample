from datetime import datetime
from enum import Enum
from sqlalchemy import Boolean, Integer
from sqlalchemy import Column
from sqlalchemy import String, Text, DateTime
from sqlalchemy.dialects.postgresql import UUID, ARRAY, TIMESTAMP
from sqlalchemy.orm import declarative_base

import uuid

Base = declarative_base()


class PortalRole(str, Enum):
    ROLE_PORTAL_USER = "ROLE_PORTAL_USER"
    ROLE_PORTAL_MODERATOR = "ROLE_PORTAL_MODERATOR"
    ROLE_PORTAL_ADMIN = "ROLE_PORTAL_ADMIN"


class User(Base):
   __tablename__ = "users"
   
   id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
   login = Column(String, unique=True, nullable=False)
   first_name = Column(String, nullable=False)
   middle_name = Column(String, nullable=False)
   last_name = Column(String, nullable=False)
   hashed_password = Column(String, nullable=False)
   role = Column(String, default=PortalRole.ROLE_PORTAL_USER)
   is_active = Column(Boolean, default=True)






    