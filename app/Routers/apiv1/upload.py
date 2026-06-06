from fastapi import UploadFile, File, HTTPException
from fastapi import APIRouter

router = APIRouter(prefix="/api/upload/v1", tags=["Upload routers"])

@router.post("/file")
async def upload_file(file: UploadFile = File(...)):
    
    if not file.filename.endswith((".xlsx", ".xls")):
        raise HTTPException(status_code=400, detail="Только Excel файлы")
    
    contents = await file.read()
    
    return {
        "filename": file.filename,
        "content_type": file.content_type,
        "size": len(contents)
    }