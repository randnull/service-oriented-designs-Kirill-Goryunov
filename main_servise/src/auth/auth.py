import jwt
import os
from dotenv import load_dotenv

load_dotenv('.env')

JWT_SECRET = os.environ['JWT_SECRET']
JWT_ALGO = os.environ['JWT_ALGO']


def create_jwt(username: str):
    payload = {'username': username}

    token = jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGO)

    return token


def decode_jwt(token: str):
    decoded_data = jwt.decode(token, JWT_SECRET, algorithms=JWT_ALGO)

    return decoded_data

