from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from app.config import settings
from app.utils import ensure_directories
from app.routes import router

ensure_directories(settings.PANELS_DIR, settings.EXPORTS_DIR)

app = FastAPI(title="ComicCraft", version="1.0.0")
app.mount("/static", StaticFiles(directory=settings.STATIC_DIR), name="static")
app.include_router(router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="127.0.0.1", port=8000, reload=True)
