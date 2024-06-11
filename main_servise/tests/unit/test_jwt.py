import pytest

from main_servise.src.auth.auth import create_jwt, decode_jwt
import os


class TestJWT:
    def test_jwt(self):
        jwt_token = create_jwt('test')

        decode_token = decode_jwt(jwt_token)

        assert decode_token['username'] == 'test'
