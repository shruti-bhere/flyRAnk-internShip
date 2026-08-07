from fastapi import FastAPI, HTTPException, status, Depends, Response
from pydantic import BaseModel, EmailStr
from database import supabase
from auth import get_current_user

app = FastAPI(
    title="Auth Login & Protect API",
    description="Secure API with Supabase Auth, JWT verification, and FastAPI Dependency Injection.",
    version="1.0.0"
)

# Request Models
class UserAuthSchema(BaseModel):
    email: EmailStr
    password: str

# -------------------------------------------------------------
# STAGE 2: Public Route
# -------------------------------------------------------------
@app.get("/public/info", tags=["Public"])
def public_info():
    return {"message": "Welcome stranger! This info is public."}

# -------------------------------------------------------------
# STAGE 1: Signup Route
# -------------------------------------------------------------
@app.post("/auth/signup", status_code=status.HTTP_201_CREATED, tags=["Authentication"])
def signup(credentials: UserAuthSchema):
    try:
        res = supabase.auth.sign_up({
            "email": credentials.email,
            "password": credentials.password
        })
        return {
            "message": "User created successfully",
            "user": {
                "id": res.user.id,
                "email": res.user.email,
                "created_at": res.user.created_at
            }
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

# -------------------------------------------------------------
# STAGE 1: Login Route
# -------------------------------------------------------------
@app.post("/auth/login", status_code=status.HTTP_200_OK, tags=["Authentication"])
def login(credentials: UserAuthSchema):
    try:
        res = supabase.auth.sign_in_with_password({
            "email": credentials.email,
            "password": credentials.password
        })
        return {
            "access_token": res.session.access_token,
            "refresh_token": res.session.refresh_token,
            "token_type": "bearer",
            "user": {
                "id": res.user.id,
                "email": res.user.email
            }
        }
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid login credentials"
        )

# -------------------------------------------------------------
# STAGE 3 & 4: Protected Profile Route
# -------------------------------------------------------------
@app.get("/protected/profile", tags=["Protected"])
def get_profile(auth_data: dict = Depends(get_current_user)):
    user = auth_data["user"]
    return {
        "user_id": user.id,
        "email": user.email,
        "created_at": user.created_at,
        "last_sign_in_at": user.last_sign_in_at
    }

# -------------------------------------------------------------
# STAGE 4: Logout Route
# -------------------------------------------------------------
@app.post("/auth/logout", status_code=status.HTTP_204_NO_CONTENT, tags=["Authentication"])
def logout(auth_data: dict = Depends(get_current_user)):
    token = auth_data["token"]
    try:
        supabase.auth.sign_out(token)
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Logout failed"
        )