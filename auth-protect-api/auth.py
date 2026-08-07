from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from database import supabase

# FastAPI security scheme that enables the "Authorize" lock button in Swagger UI (/docs)
security_scheme = HTTPBearer()

def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security_scheme)):
    """
    Extracts the Bearer token from the Authorization header,
    verifies it with Supabase Auth, and returns the user payload.
    """
    token = credentials.credentials
    try:
        # Verify token with Supabase
        user_response = supabase.auth.get_user(token)
        if not user_response or not user_response.user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid or expired token"
            )
        return {"user": user_response.user, "token": token}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token"
        )