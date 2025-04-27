from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.docs import (
    get_redoc_html,
    get_swagger_ui_html,
    get_swagger_ui_oauth2_redirect_html
)
from fastapi.staticfiles import StaticFiles

from app.routes import dosen, mahasiswa, waktu_bimbingan, antrian_bimbingan, admin, auth, news, file, layanan, mahasiswa_dosen
# from app.routes import test_notify
from app.routes import websocket
# from app.routes import push_notif
from app.routes import file

from app.config import engine
from app.models import admin as admin_model, dosen as dosen_model, mahasiswa as mahasiswa_model, waktu_bimbingan as waktu_model, antrian_bimbingan as antrian_model, news as news_model, file as file_model, layanan as layanan_model, mahasiswa_dosen as relasi_model
from app.models import file as files_model

app = FastAPI(
    title="Dosen Queue System API",
    version="1.0.0",
    docs_url=None,
    redoc_url=None
    )

app.mount("/static", StaticFiles(directory="static"), name="static")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"], 
    allow_headers=["*"], 

)

# Register API Routes
app.include_router(auth.router)

app.include_router(admin.router)
app.include_router(dosen.router)
app.include_router(mahasiswa.router)
app.include_router(mahasiswa_dosen.router)

app.include_router(waktu_bimbingan.router)
app.include_router(antrian_bimbingan.router)

app.include_router(layanan.router)

# app.include_router(test_notify.router)
app.include_router(websocket.router)
# app.include_router(push_notif.router)
app.include_router(file.router)
# app.include_router(news.router)
# app.include_router(file.router)

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

# @app.middleware("http")
# async def csp_middleware(request, call_next):
#     response = await call_next(request)
#     response.headers["Content-Security-Policy"] = "default-src 'self'; connect-src 'self' ws://localhost:8000"
#     return response

# Ensure tables are created
admin_model.Base.metadata.create_all(bind=engine)
dosen_model.Base.metadata.create_all(bind=engine)
mahasiswa_model.Base.metadata.create_all(bind=engine)
waktu_model.Base.metadata.create_all(bind=engine)
antrian_model.Base.metadata.create_all(bind=engine)
news_model.Base.metadata.create_all(bind=engine)
file_model.Base.metadata.create_all(bind=engine)
layanan_model.Base.metadata.create_all(bind=engine)
# relasi_model.Base.metadata.create_all(bind=engine)
# subs_model.Base.metadata.create_all(bind=engine)
files_model.Base.metadata.create_all(bind=engine)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
