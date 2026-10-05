import os

from fastapi import HTTPException, UploadFile

from app.core.config import settings


ALLOWED_EXTENSIONS = {
    ".jpg",
    ".jpeg",
    ".png",
    ".pdf",
    ".txt",
    ".docx"
}


async def save_file(file: UploadFile):

    filename = os.path.basename(file.filename)

    extension = os.path.splitext(filename)[1].lower()

    if extension not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=400,
            detail="File type not allowed"
        )

    content = await file.read()

    if len(content) > settings.MAX_FILE_SIZE:
        raise HTTPException(
            status_code=400,
            detail="File too large"
        )

    os.makedirs(
        settings.UPLOAD_DIR,
        exist_ok=True
    )

    file_path = os.path.join(
        settings.UPLOAD_DIR,
        filename
    )

    with open(file_path, "wb") as buffer:
        buffer.write(content)

    return {
        "filename": filename,
        "size": len(content)
    }