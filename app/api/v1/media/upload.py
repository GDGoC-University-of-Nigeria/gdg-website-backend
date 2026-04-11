from fastapi import APIRouter, Depends, File, UploadFile, HTTPException, status
from app.dependencies.get_current_user import get_current_user
from app.models.user import User
from app.services.cloudinary import upload_image

router = APIRouter()

@router.post("/upload")
async def upload_media(
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user)
):
    """
    Authenticated endpoint to upload media to Cloudinary.
    """
    if not file.content_type.startswith("image/"):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Only image files are allowed"
        )
    
    try:
        # Read file contents
        contents = await file.read()
        # Upload to cloudinary
        url = upload_image(contents)
        if not url:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to upload image to Cloudinary"
            )
        return {"url": url}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Upload error: {str(e)}"
        )
