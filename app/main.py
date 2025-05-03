from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from app.core.config import settings
from app.core.scheduler import create_scheduler

from app.database.models import *
from app.routes import all_routers

@asynccontextmanager
async def lifespan(app: FastAPI):
    scheduler = create_scheduler()
    yield
    scheduler.shutdown(wait=True)

app = FastAPI(
    title=settings.app_name,
    description="API for Dosen Queue System",
    version="1.0.0",
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins="*", 
    allow_credentials=True,
    allow_methods=["*"], 
    allow_headers=["*"]
)

for router in all_routers:
    app.include_router(router)

@app.get("/")
def read_root():
    return {"message": f"Welcome to {settings.app_name}"}

# if __name__ == "__main__":
#     import uvicorn
#     uvicorn.run("app.main:app", host="127.0.0.1", port=8000, reload=True)