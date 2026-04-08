from starlette.middleware.base import BaseHTTPMiddleware
from fastapi.responses import JSONResponse

from core.security import verify_access_token

class AuthMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        public_prefixes = [
            "/auth",
            "/docs",
            "/openapi.json",
            "/redoc",
            "/favicon.ico",
        ]

        if request.url.path == "/" or any(
            request.url.path.startswith(path) for path in public_prefixes
        ):
            return await call_next(request)

        auth_header = request.headers.get("Authorization")

        if not auth_header:
            return JSONResponse(
                status_code=401,
                content={"detail": "Authorization header missing"}
            )

        # Remove "Bearer "
        token = auth_header.replace("Bearer ", "")

        if not verify_access_token(token):
            return JSONResponse(
                status_code=401,
                content={"detail": "Invalid token"}
            )

        return await call_next(request)
