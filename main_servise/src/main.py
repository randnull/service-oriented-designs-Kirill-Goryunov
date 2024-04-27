from fastapi import FastAPI, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.responses import JSONResponse

from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from passlib.context import CryptContext
import os

import grpc
import posts_pb2
import posts_pb2_grpc

from database_connection.base import get_session

from dto_table.user_dto import UserModel
from dto_table.register_dto import RegisterModel
from dto_table.update_dto import UpdateModel
from dao_table.user_dao import User
from dto_table.posts_dto import NewPostModel, PostModel, AllPosts

from repository.repo import user_repository

from auth.auth import create_jwt
from auth.auth import decode_jwt

import datetime

tags = [
    {
        "name": "login&register",
        "description": "Operations with registration and authentication"
    },
    {
        "name": "user",
        "description": "Operations with user profile"
    },
    {
        "name": "posts",
        "description": "Operations with posts"
    }
]

grpc_host = os.environ['GRPC_HOST']
grpc_port = os.environ['GRPC_PORT']

grpc_channel = grpc.insecure_channel(f'{grpc_host}:{grpc_port}')
grpc_stub = posts_pb2_grpc.PostsServiceStub(grpc_channel)

app = FastAPI(openapi_tags=tags)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


@app.post("/register", tags=["login&register"])
async def registration(register_model: RegisterModel, s: AsyncSession = Depends(get_session)):
    is_username_exist = await user_repository.get(s, register_model.username)
    
    if not is_username_exist is None:
        return JSONResponse(content={"message": "Username already taken"}, status_code=409)

    password_hash = pwd_context.hash(register_model.password)
    register_model.password = password_hash
    x = await user_repository.add(s, register_model)
    return JSONResponse(content={"message": "Registration was succesfull!"}, status_code=200)


@app.post("/login", tags=["login&register"])
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


@app.get("/profile", tags=["user"])
async def get_current_user(current_user: UserModel = Depends(get_user)):
    return current_user.dict(exclude={"password"})


@app.put("/update", tags=["user"])
async def update(new_info: UpdateModel, s: AsyncSession = Depends(get_session), current_user: UserModel = Depends(get_user)):
    id = await user_repository.get_id_by_username(s, current_user.username)

    to_update = new_info.dict(exclude_none=True)

    await user_repository.update_info(s, id, to_update)

    return JSONResponse(content={"message": "Updated"}, status_code=200)


@app.post("/posts/new", tags=["posts"])
async def newpost(new_post: NewPostModel, s: AsyncSession = Depends(get_session), current_user: UserModel = Depends(get_user)):
    id = await user_repository.get_id_by_username(s, current_user.username)

    response = grpc_stub.CreatePost(posts_pb2.CreateRequest(user_id=id, title=new_post.title, body=new_post.body))
    
    return JSONResponse(content={"message": f"id = {response.id}"}, status_code=201)


@app.delete("/posts/{post_id}", tags=["posts"])
async def deletepost(post_id: str, s: AsyncSession = Depends(get_session), current_user: UserModel = Depends(get_user)):
    id = await user_repository.get_id_by_username(s, current_user.username)

    response = grpc_stub.DeletePost(posts_pb2.DeleteRequest(id=post_id, user_id=id))
    
    return JSONResponse(content={"message": "Deleted"}, status_code=204)


@app.get("/posts/{post_id}", tags=["posts"])
async def getpost(post_id: str, s: AsyncSession = Depends(get_session), current_user: UserModel = Depends(get_user)):
    id = await user_repository.get_id_by_username(s, current_user.username)

    response = grpc_stub.GetByIdPost(posts_pb2.GetById(id=post_id, user_id=id))

    if response.status != 0:
        return JSONResponse(content={"message": f"Not Found"}, status_code=404)

    time_seconds = response.created_at.seconds + response.created_at.nanos / 1e9
    
    response_dto = PostModel(
        id=response.id,
        user_id=response.user_id,
        title=response.title,
        body=response.body,
        created_at=datetime.datetime.fromtimestamp(time_seconds)
    )

    return response_dto


@app.put("/posts/{post_id}", tags=["posts"])
async def updatepost(post_id: str, update_post: NewPostModel, s: AsyncSession = Depends(get_session), current_user: UserModel = Depends(get_user)):
    id = await user_repository.get_id_by_username(s, current_user.username)

    response = grpc_stub.UpdatePost(posts_pb2.UpdateRequest(id=post_id, user_id=id, title=update_post.title, body=update_post.body))
    
    if int(response.status) != 0:
        return JSONResponse(content={"message": f"Not Found"}, status_code=404)

    return JSONResponse(content={"message": f"Updated"}, status_code=200)


@app.post("/posts/{user_id}", tags=["posts"])
async def getallposts(user_id: int, page_config: AllPosts, s: AsyncSession = Depends(get_session), current_user: UserModel = Depends(get_user)):
    if page_config.page_size <= 0:
        return JSONResponse(content={"message": f"Page size equal/less than zero!"}, status_code=400)
    if page_config.page_number <= 0:
        return JSONResponse(content={"message": f"Page number equal/less than zero!"}, status_code=400)

    response = grpc_stub.GetAllPost(posts_pb2.GetAllRequest(user_id=user_id, page_size=page_config.page_size, page_number=page_config.page_number))

    posts_from_grpc = response.posts

    posts_list = list()

    for post in posts_from_grpc:
        time_seconds = post.created_at.seconds + post.created_at.nanos / 1e9

        response_dto = PostModel(
            id=post.id,
            user_id=post.user_id,
            title=post.title,
            body=post.body,
            created_at=datetime.datetime.fromtimestamp(time_seconds)
        )
        posts_list.append(response_dto)
    
    return {"number_posts": f"{len(posts_list)}", "page": f"{page_config.page_number}"}, posts_list
