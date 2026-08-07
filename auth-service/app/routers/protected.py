from fastapi import APIRouter, Depends

from app.middleware.auth import verify_token

router = APIRouter()


@router.get("/profile")
def profile(user=Depends(verify_token)):

    return {

        "message": "Protected Route",

        "current_user": user

    }


@router.get("/admin")
def admin(user=Depends(verify_token)):

    # Example authorization check
    if user.get("role") != "admin":
        from fastapi import HTTPException

        raise HTTPException(
            status_code=403,
            detail="Forbidden"
        )

    return {"message": "Welcome Admin"}