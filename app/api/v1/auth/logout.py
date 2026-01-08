from fastapi import APIRouter, Response

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/logout")
def logout(response: Response):
    
    response.delete_cookie(key="access_token")
    response.delete_cookie(key="refresh_token")
    return {"message": "Logged out successfully"}
