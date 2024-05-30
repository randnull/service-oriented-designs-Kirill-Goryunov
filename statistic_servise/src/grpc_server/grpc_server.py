import grpc

import statistic_pb2_grpc
import statistic_pb2

from controllers.statistic_grpc_controller import StatisticService

from config.settings import settings


async def start_grpc():
    server = grpc.aio.server()
    statistic_pb2_grpc.add_StatisticServiceServicer_to_server(StatisticService(), server)
    server.add_insecure_port(f'[::]:{settings.GRPC_SERVER_PORT}')
    await server.start()
    await server.wait_for_termination()
