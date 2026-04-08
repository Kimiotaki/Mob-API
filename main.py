from fastapi import FastAPI
from middleware.auth_middleware import AuthMiddleware
from api.routes.auth_routes import router as auth_router

app = FastAPI()
app.add_middleware(AuthMiddleware)
app.include_router(auth_router)
