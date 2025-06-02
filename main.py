from fastapi import FastAPI
from pydantic import BaseModel, EmailStr
from auth import *
from token_store import *

app = FastAPI()


class RegisterRequest(BaseModel):
    email: EmailStr
    password: str


@app.post("/register")
async def register(request: RegisterRequest):
    return await register_user(request.email, request.password)


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


@app.post("/login")
async def login(request: LoginRequest):
    return await login_user(request.email, request.password)


class EmailRequest(BaseModel):
    email: EmailStr


@app.get("/protected")
async def protected():
    email = get_last_logged_email()
    if not email:
        return {"message": "No logged in user"}
    return await get_protected_data(email)


@app.post("/refresh")
async def refresh(request: EmailRequest):
    return await refresh_access_token(request.email)


# @app.get("/debug_tokens")
# def debug_tokens():
#     return load_all_tokens()