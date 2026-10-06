import logging

from fastapi import FastAPI
from fastapi.responses import JSONResponse

from app.api.cds_hooks import router as cds_router
from app.config.settings import settings

logging.basicConfig(
    level=getattr(logging, settings.log_level.upper(), logging.INFO),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
)
logger = logging.getLogger("cds_hooks.main")

app = FastAPI(
    title="Clinical Decision Support Rules Engine",
    version="1.0.0",
    description="CDS Hooks compatible clinical decision support rules engine using dynamic synthetic patient context.",
    docs_url="/docs",
    redoc_url="/redoc",
)


@app.get("/")
def root() -> dict:
    return {
        "service": "Clinical Decision Support Rules Engine",
        "version": settings.app_version,
        "description": settings.app_description,
    }


@app.get("/health")
def health() -> dict:
    logger.info("Health check requested")
    return {"status": "ok", "service": settings.app_name, "version": settings.app_version}


@app.exception_handler(Exception)
async def unexpected_exception_handler(request, exc):
    logger.exception("Unexpected server error", extra={"path": str(request.url.path)})
    return JSONResponse(status_code=500, content={"detail": "Unexpected server error"})


app.include_router(cds_router)
