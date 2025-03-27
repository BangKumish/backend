from fastapi import FastAPI
from app.routes import dosen, mahasiswa, waktu_bimbingan, antrian_bimbingan, admin, auth, news, file, layanan
from app.config import engine
from app.models import admin as admin_model, dosen as dosen_model, mahasiswa as mahasiswa_model, waktu_bimbingan as waktu_model, antrian_bimbingan as antrian_model, news as news_model, file as file_model, layanan as layanan_model

app = FastAPI(title="Dosen Queue System API", version="1.0.0")

# Register API Routes
app.include_router(dosen.router)
app.include_router(mahasiswa.router)
app.include_router(waktu_bimbingan.router)
app.include_router(antrian_bimbingan.router)
app.include_router(admin.router)
app.include_router(auth.router)
app.include_router(news.router)
app.include_router(file.router)
app.include_router(layanan.router)

@app.get("/")
def read_root():
    return {"message": "Welcome to Dosen Queue System"}

# Ensure tables are created
admin_model.Base.metadata.create_all(bind=engine)
dosen_model.Base.metadata.create_all(bind=engine)
mahasiswa_model.Base.metadata.create_all(bind=engine)
waktu_model.Base.metadata.create_all(bind=engine)
antrian_model.Base.metadata.create_all(bind=engine)
news_model.Base.metadata.create_all(bind=engine)
file_model.Base.metadata.create_all(bind=engine)
layanan_model.Base.metadata.create_all(bind=engine)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
