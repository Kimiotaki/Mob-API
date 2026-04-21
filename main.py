from fastapi import FastAPI
from middleware.auth_middleware import AuthMiddleware
from api.routes.auth_routes import router as auth_router
from api.routes.user_routes import router as user_router

app = FastAPI()
app.add_middleware(AuthMiddleware)
app.include_router(auth_router)
app.include_router(user_router)
