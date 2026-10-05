import os

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile
from fastapi.responses import FileResponse

from app.core.config import settings
from app.db.models import User
from app.dependencies.auth import get_current_user
from app.services.file_service import save_file


router = APIRouter(
    prefix="/files",
    tags=["Files"]
)


@router.post("/upload")
async def upload_file(
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user)
):
    return await save_file(file)


@router.get("/")
def list_files(
    current_user: User = Depends(get_current_user)
):
    os.makedirs(
        settings.UPLOAD_DIR,
        exist_ok=True
    )

    files = os.listdir(settings.UPLOAD_DIR)

    return {
        "files": files
    }


@router.get("/{filename}")
def download_file(
    filename: str,
    current_user: User = Depends(get_current_user)
):
    filename = os.path.basename(filename)

    file_path = os.path.join(
        settings.UPLOAD_DIR,
        filename
    )

    if not os.path.exists(file_path):
        raise HTTPException(
            status_code=404,
            detail="File not found"
        )

    return FileResponse(file_path)


@router.delete("/{filename}")
def delete_file(
    filename: str,
    current_user: User = Depends(get_current_user)
):
    filename = os.path.basename(filename)

    file_path = os.path.join(
        settings.UPLOAD_DIR,
        filename
    )

    if not os.path.exists(file_path):
        raise HTTPException(
            status_code=404,
            detail="File not found"
        )

    os.remove(file_path)

    return {
        "message": "File deleted successfully"
    }