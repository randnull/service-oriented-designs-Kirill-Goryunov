from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.responses import JSONResponse

import grpc
import posts_pb2
import posts_pb2_grpc

from common.database_connection.base import get_session

from controllers.auth_controller import get_user

from dto_table.user_dto import UserModel
from dto_table.posts_dto import NewPostModel, PostModel, AllPosts

from repository.repo import user_repository

from config.settings import settings

import datetime


posts_router = APIRouter(prefix="/posts", tags=["posts"])

grpc_host = settings.GRPC_HOST
grpc_port = settings.GRPC_PORT

grpc_channel = grpc.insecure_channel(f'{grpc_host}:{grpc_port}')
grpc_stub = posts_pb2_grpc.PostsServiceStub(grpc_channel)


@posts_router.post("/new", tags=["posts"])
async def newpost(new_post: NewPostModel, s: AsyncSession = Depends(get_session), current_user: UserModel = Depends(get_user)):
    id = await user_repository.get_id_by_username(s, current_user.username)

    response = grpc_stub.CreatePost(posts_pb2.CreateRequest(user_id=id, title=new_post.title, body=new_post.body))
    
    return JSONResponse(content={"message": f"id = {response.id}"}, status_code=201)


@posts_router.delete("/{post_id}", tags=["posts"])
async def deletepost(post_id: str, s: AsyncSession = Depends(get_session), current_user: UserModel = Depends(get_user)):
    id = await user_repository.get_id_by_username(s, current_user.username)

    response = grpc_stub.DeletePost(posts_pb2.DeleteRequest(id=post_id, user_id=id))
    
    return JSONResponse(content={"message": "Deleted"}, status_code=204)


@posts_router.get("/{post_id}", tags=["posts"])
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


@posts_router.put("/{post_id}", tags=["posts"])
async def updatepost(post_id: str, update_post: NewPostModel, s: AsyncSession = Depends(get_session), current_user: UserModel = Depends(get_user)):
    id = await user_repository.get_id_by_username(s, current_user.username)

    response = grpc_stub.UpdatePost(posts_pb2.UpdateRequest(id=post_id, user_id=id, title=update_post.title, body=update_post.body))
    
    if int(response.status) != 0:
        return JSONResponse(content={"message": f"Not Found"}, status_code=404)

    return JSONResponse(content={"message": f"Updated"}, status_code=200)


@posts_router.post("/{user_login}", tags=["posts"])
async def getallposts(user_login: str, page_config: AllPosts, s: AsyncSession = Depends(get_session), current_user: UserModel = Depends(get_user)):
    if page_config.page_size <= 0:
        return JSONResponse(content={"message": f"Page size equal/less than zero!"}, status_code=400)
    if page_config.page_number <= 0:
        return JSONResponse(content={"message": f"Page number equal/less than zero!"}, status_code=400)

    user_id = await user_repository.get_id_by_username(s, username=user_login)

    response = grpc_stub.GetAllPost(posts_pb2.GetAllRequest(user_id=int(user_id), page_size=page_config.page_size, page_number=page_config.page_number))

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
