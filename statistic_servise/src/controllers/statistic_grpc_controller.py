import statistic_pb2
import statistic_pb2_grpc

from common.database_connection.base import async_session

from repository.repo import statistic_repository


class StatisticService(statistic_pb2_grpc.StatisticServiceServicer):
    async def GetStatisticByPost(self, request, context):
        async with async_session() as session:
           likes, views = await statistic_repository.get_statistic(session, request.id)

        return statistic_pb2.GetByPostResponse(likes=likes, views=views)

    async def GetPopularPost(self, request, context):
        sort_type = request.sort_type

        async with async_session() as session:
            popular_posts = await statistic_repository.get_popular_posts(session, sort_type)

        popular_posts_dto = list()

        for post in popular_posts:
            post_dto = statistic_pb2.PostAnswer(
                post_id=post.post_id,
                author=post.author,
                count=int(post.count_actions)
            )

            popular_posts_dto.append(post_dto)

        return statistic_pb2.GetPopularPostResponse(popular_posts=popular_posts_dto)

    async def GetPopularUser(self, request, context):
        async with async_session() as session:
            popular_users = await statistic_repository.get_popular_users(session)

        popular_users_dto = list()

        for post in popular_users:
            post_dto = statistic_pb2.UserAnswer(
                author=post.author,
                likes=int(post.likes)
            )

            popular_users_dto.append(post_dto)

        return statistic_pb2.GetPopularUserResponse(popular_users=popular_users_dto)
