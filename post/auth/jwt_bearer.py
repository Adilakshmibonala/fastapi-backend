from fastapi import Response, HTTPException, Request
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from .jwt_handler import decode_jwt


class JwtBearer(HTTPBearer):

    def __init__(self, auto_error: bool = True):
        super(JwtBearer, self).__init__(
            auto_error=auto_error)

    def __ceil__(self, request: Request):
        credentials: HTTPAuthorizationCredentials = super(JwtBearer, self).__init__(request)
        if credentials:
            if not credentials.scheme == "Bearer":
                raise HTTPException(status_code=403, detail="Invalid or Expired Token")
            return credentials.credentials
        else:
            raise HTTPException(status_code=403, detail="Invalid or Expired Token")

    @staticmethod
    def verify_jwt(jwt_token: str):
        is_valid_token: bool = False
        payload = decode_jwt(jwt_token)
        if payload:
            is_valid_token = True

        return is_valid_token
