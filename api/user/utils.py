from typing import Union
from uuid import UUID

from fastapi import HTTPException, status
from api.schemas import UserCreate, ShowUser, UpdateUserRequest

from db.dals import UserDAL
from db.models import PortalRole, User

from api.hasher import Hasher

async def _create_new_user(body: UserCreate, session) -> ShowUser:
    async with session.begin():
        user_dal = UserDAL(session)
        user = await user_dal.create_user(
            login=body.login,
            first_name=body.first_name,
            middle_name=body.middle_name,
            last_name=body.last_name,
            hashed_password=Hasher.get_password_hash(body.password),
        )
        return ShowUser(
            id=user.id,
            login=user.login,
            role=user.role,
            is_active=user.is_active,
        )

async def _delete_user(id: UUID, session) -> Union[UUID, None]:
    async with session.begin():
        user_dal = UserDAL(session)
        remote_user_id = await user_dal.delete_user(id=id)
        if remote_user_id is not None:
            return remote_user_id

async def _update_user(id: UUID, update_user_params: dict, session) -> Union[UUID, None]:
    async with session.begin():
        user_dal = UserDAL(session)
        update_user_id = await user_dal.update_user(id=id, update_user_params=update_user_params)
        if update_user_id is not None:
            return update_user_id

async def _get_user_by_id(id: UUID, session) -> Union[User, None]:
    async with session.begin():
        user_dal = UserDAL(session)
        user = await user_dal.get_user_by_id(id=id)
        if user is not None:
            return user

async def _get_user_by_login(login: str, session) -> Union[User, None]:
    async with session.begin():
        user_dal = UserDAL(session)
        user = await user_dal.get_user_by_login(login=login)
        if user is not None:
            return user

async def _check_user_permissions(target_user: User, current_user: User) -> bool:
    if PortalRole.ROLE_PORTAL_ADMIN == target_user.role and PortalRole.ROLE_PORTAL_USER == current_user.role:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Admin cannot be deleted by the user."
        )
    if target_user.id != current_user.id:
        if PortalRole.ROLE_PORTAL_ADMIN != current_user.role:
            return False
        if PortalRole.ROLE_PORTAL_ADMIN == target_user.role and PortalRole.ROLE_PORTAL_ADMIN == current_user.role:
            return False
    return True
