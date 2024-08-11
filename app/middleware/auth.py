from typing import Optional
from fastapi import Request
from fastapi.middleware import Middleware
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import JSONResponse
from app.core.config import settings


class AuthMiddleware(BaseHTTPMiddleware):
    def __init__(self, app, protected_paths: list[str]):
        super().__init__(app)
        self.protected_paths = protected_paths

    async def dispatch(self, request: Request, call_next):
        # Example: Extract token from headers
        auth_header = request.headers.get("Authorization")
        if any(request.url.path.startswith(path) for path in self.protected_paths):
            auth_header = request.headers.get("Authorization")

            if not self.is_valid_token(auth_header):
                return JSONResponse(content={"error": "Unauthorized"}, status_code=401)

        # Continue processing the request if authenticated
        response = await call_next(request)
        return response

    def is_valid_token(self, token: Optional[str]) -> bool:
        return settings.api_secret is None or token == settings.api_secret


middleware = [Middleware(AuthMiddleware, protected_paths=["/api"])]
