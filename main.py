from fastapi import FastAPI
import uvicorn

from app.Routers.apiv1.upload import router as upload_router

app = FastAPI()

app.include_router(upload_router)

if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)