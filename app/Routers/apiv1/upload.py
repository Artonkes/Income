from fastapi import UploadFile, File, HTTPException, APIRouter
from uuid import uuid4
import os

from app.models.dataset_llm import UploadResponse
from app.Redis.clien import r

router = APIRouter(prefix="/api/upload/v1", tags=["Upload routers"])

UPLOAD_DIR = "/tmp/uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)


# Функция для обработки файла в фоне 
def process_file(file_path: str, task_id: str):
    pass


@router.post("/file")
async def upload_file(file: UploadFile = File(...)):
    
    if not file.filename.endswith((".xlsx", ".xls")):
        raise HTTPException(status_code=400, detail="Только Excel файлы")
    
    contents = await file.read()
    task_id = str(uuid4())  

    file_patch = f"{UPLOAD_DIR}/{task_id}_{file.filename}"

    with open(file_patch, "wb") as f:
        f.write(contents)
    
    # Сохранение файла в Redis
    r.hset(task_id, mapping={
        'status': 'processing',
        'total': 0,
        'processed': 0,
        'file_path': file_patch,
    })

    return UploadResponse(
        task_id=task_id,
        filename=file.filename,
        size=len(contents),
        status="processing"
    )

# Получение статуса задачи
@router.get("/status/{task_id}")
def get_status(task_id: str):
    data = r.hgetall(task_id)
    
    if not data:
        raise HTTPException(status_code=404, detail="Задача не найдена")
    
    total = int(data['total'])
    processed = int(data['processed'])
    progress = round(processed / total * 100, 1) if total > 0 else 0.0
    
    return {
        "task_id": task_id,
        "status": data['status'],
        "progress": progress
    }

# Получение результата задачи
@router.get("/result/{task_id}")
def get_result(task_id: str):
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

