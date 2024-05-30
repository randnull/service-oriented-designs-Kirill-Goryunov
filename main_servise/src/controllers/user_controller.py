from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.responses import JSONResponse

from common.database_connection.base import get_session

from dto_table.user_dto import UserModel
from dto_table.update_dto import UpdateModel
from controllers.auth_controller import get_user

from repository.repo import user_repository


user_router = APIRouter(prefix="", tags=["user"])


@user_router.get("/profile", tags=["user"])
async def get_current_user(current_user: UserModel = Depends(get_user)):
    return current_user.dict(exclude={"password"})


@user_router.put("/update", tags=["user"])
async def update(new_info: UpdateModel, s: AsyncSession = Depends(get_session), current_user: UserModel = Depends(get_user)):
    id = await user_repository.get_id_by_username(s, current_user.username)

    to_update = new_info.dict(exclude_none=True)

    await user_repository.update_info(s, id, to_update)

    return JSONResponse(content={"message": "Updated"}, status_code=200)
