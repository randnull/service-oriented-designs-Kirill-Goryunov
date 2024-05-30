from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.responses import JSONResponse

from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from passlib.context import CryptContext

from common.database_connection.base import get_session

from dto_table.user_dto import UserModel
from dto_table.register_dto import RegisterModel

from repository.repo import user_repository

from auth.auth import create_jwt, decode_jwt


auth_router = APIRouter(prefix="", tags=["login&register"])


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


@auth_router.post("/register", tags=["login&register"])
async def registration(register_model: RegisterModel, s: AsyncSession = Depends(get_session)):
    is_username_exist = await user_repository.get(s, register_model.username)
    
    if not is_username_exist is None:
        return JSONResponse(content={"message": "Username already taken"}, status_code=409)

    password_hash = pwd_context.hash(register_model.password)
    register_model.password = password_hash
    x = await user_repository.add(s, register_model)
    return JSONResponse(content={"message": "Registration was succesfull!"}, status_code=200)


@auth_router.post("/login", tags=["login&register"])
async def auth_user(request_model: OAuth2PasswordRequestForm = Depends(), s: AsyncSession = Depends(get_session)):
    user = await user_repository.get(s, request_model.username)

    if not user:
        return JSONResponse(content={"message": "User or password not found"}, status_code=404)
    
    user_dto = UserModel.to_dto(user)

    if not pwd_context.verify(request_model.password, user_dto.password):
        return JSONResponse(content={"message": "User or password not found"}, status_code=404)

    token = create_jwt(request_model.username)

    return {"access_token": token, "token_type": "bearer"}


async def get_user(token: str = Depends(oauth2_scheme), s: AsyncSession = Depends(get_session)):
    decode = decode_jwt(token)

    user = await user_repository.get(s, decode['username'])

    if user is None:
        return JSONResponse(content={"message": "Invalid authentication"}, status_code=401)

    dto_user = UserModel.to_dto(user)

    return dto_user
