from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.docs import (
    get_redoc_html,
    get_swagger_ui_html,
    get_swagger_ui_oauth2_redirect_html
)
from fastapi.staticfiles import StaticFiles
from apscheduler.schedulers.background import BackgroundScheduler
from contextlib import asynccontextmanager

from app.config import get_db
from app.config import engine

from app.models import admin as admin_model
from app.models import antrian_bimbingan as antrian_model
from app.models import dosen as dosen_model
from app.models import file as files_model
from app.models import layanan as layanan_model
from app.models import mahasiswa as mahasiswa_model
from app.models import mahasiswa_dosen as relasi_model
from app.models import news as news_model
from app.models import subscription as subs_model
from app.models import waktu_bimbingan as waktu_model

from app.routes import admin
from app.routes import antrian_bimbingan
from app.routes import auth
from app.routes import dosen
from app.routes import file
from app.routes import layanan
from app.routes import mahasiswa
from app.routes import mahasiswa_dosen
from app.routes import news
from app.routes import push_router
from app.routes import waktu_bimbingan
from app.routes import websocket_router

from app.services.notification_service import send_upcoming_bimbingan_notifications

@asynccontextmanager
async def lifespan(app: FastAPI):
    scheduler = BackgroundScheduler()
    scheduler.add_job(
        func=lambda: send_upcoming_bimbingan_notifications(next(get_db())),
        trigger="interval",
        minutes=1  
    )
    scheduler.start()

    yield
    
    scheduler.shutdown()

app = FastAPI(
    title="Dosen Queue System API",
    version="1.0.0",
    docs_url=None,
    redoc_url=None,
    lifespan=lifespan
    )

app.mount("/static", StaticFiles(directory="static"), name="static")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"], 
    allow_headers=["*"], 

)

app.include_router(admin.router)
app.include_router(auth.router)
app.include_router(antrian_bimbingan.router)
app.include_router(dosen.router)
app.include_router(file.router)
app.include_router(layanan.router)
app.include_router(mahasiswa.router)
app.include_router(mahasiswa_dosen.router)
app.include_router(news.router)
app.include_router(push_router.router)
app.include_router(waktu_bimbingan.router)
app.include_router(websocket_router.router)


@app.get("/")
def read_root():
    return {"message": "Welcome to Dosen Queue System"}

@app.get("/docs", include_in_schema=False)
async def custom_swagger_ui_html():
    return get_swagger_ui_html(
        openapi_url=app.openapi_url,
        title=app.title + " - Swagger UI",
        oauth2_redirect_url=app.swagger_ui_oauth2_redirect_url,
        swagger_js_url="/static/swagger-ui-bundle.js",
        swagger_css_url="/static/swagger-ui.css",
    )


@app.get(app.swagger_ui_oauth2_redirect_url, include_in_schema=False)
async def swagger_ui_redirect():
    return get_swagger_ui_oauth2_redirect_html()


@app.get("/redoc", include_in_schema=False)
async def redoc_html():
    return get_redoc_html(
        openapi_url=app.openapi_url,
        title=app.title + " - ReDoc",
        redoc_js_url="/static/redoc.standalone.js",
    )

admin_model.Base.metadata.create_all(bind=engine)
antrian_model.Base.metadata.create_all(bind=engine)
dosen_model.Base.metadata.create_all(bind=engine)
files_model.Base.metadata.create_all(bind=engine)
mahasiswa_model.Base.metadata.create_all(bind=engine)
news_model.Base.metadata.create_all(bind=engine)
layanan_model.Base.metadata.create_all(bind=engine)
relasi_model.Base.metadata.create_all(bind=engine)
subs_model.Base.metadata.create_all(bind=engine)
waktu_model.Base.metadata.create_all(bind=engine)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
