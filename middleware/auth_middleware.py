from starlette.middleware.base import BaseHTTPMiddleware
from fastapi.responses import JSONResponse

from core.security import verify_access_token

class AuthMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        # Here you would implement your authentication logic
        # For example, you could check for a valid JWT token in the Authorization header
        public_paths = [
            "/"
            "/auth",
            "/docs",
            "/openapi.json",
            "/redoc",
            "/favicon.ico"
        ]

        #Allow public endpoints
        if any(request.url.path.startswith(path) for path in public_paths):
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
