# This file is responsible for signing, encoding, decoding and returning JWTs.

import time
import jwt
from decouple import config


JWT_SECRET_KEY = config("JWT_SECRET_KEY")
ALGORITHM = config("ALGORITHM")


def token_response(token: str) -> dict:
    return {
        "access_token": token
    }


def get_jwt_token(email: str):
    payload = {
        "email": email,
        "expiry": time.time() + int(config("ACCESS_TOKEN_EXPIRE_MINUTES"))
    }
    token = jwt.encode(payload, JWT_SECRET_KEY, algorithm=ALGORITHM)
    return token_response(token=token)


def decode_jwt(token: str):
    decode_token = jwt.decode(token, JWT_SECRET_KEY, algorithms=ALGORITHM)
    return decode_token if decode_token["expiry"] >= time.time() else None
