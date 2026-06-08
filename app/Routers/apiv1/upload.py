from fastapi import UploadFile, File, HTTPException
from fastapi import APIRouter

from uuid import uuid4
from app.Redis.clien import r

router = APIRouter(prefix="/api/upload/v1", tags=["Upload routers"])

@router.post("/file")
async def upload_file(file: UploadFile = File(...)):
    
    if not file.filename.endswith((".xlsx", ".xls")):
        raise HTTPException(status_code=400, detail="Только Excel файлы")
    
    contents = await file.read()
    task_id = str(uuid4())  
    
    # Сохранение файла в Redis
    r.hset(task_id, mapping={
        'status': 'processing',
        'total': 0,
        'processed': 0,
    })

    return {
        "task_id": task_id,
        "filename": file.filename,
        "size": len(contents)
    }


@router.get("/status/{task_id}")
def get_status(task_id: str):
    data = r.hgetall(task_id)
    if not data:
        raise HTTPException(status_code=404, detail="Задача не найдена")
    
    total = int(data['total'] if ["data"] != 0 else 1)
    processed = int(data['processed'])

    progress = round(processed / total * 100, 1) if total > 0 else 0.0

    return {
        "task_id": task_id,
        "status": data['status'],
        "progress": progress
    }


@router.get("/update_status/{task_id}")
def update_status(task_id: str):
    data = r.hgetall(task_id)
    if not data:
        raise HTTPException(status_code=404, detail="Задача не найдена")
    
    if data['status'] != 'done':
        raise HTTPException(status_code=400, detail="Задача еще не завершена")
    
    return {
        "task_id": task_id,
        "status": data['status'],
        "result": data.get('result', "{}"),
    }

