from pydantic import BaseModel


class FileResponse(BaseModel):
    filename: str
    size: int