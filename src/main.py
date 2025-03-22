from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import uvicorn

from .core.config import settings
from .core.logging import logger
from .core.middleware import RequestLoggingMiddleware, RateLimitMiddleware
from .api import auth, users, blockchain

# Load environment variables
load_dotenv()

# Create FastAPI app
app = FastAPI(
    title=settings.APP_NAME,
    description="AI-powered decision support platform",
    version="1.0.0"
)

# Add middleware
app.add_middleware(RequestLoggingMiddleware)
app.add_middleware(RateLimitMiddleware, requests_per_minute=settings.RATE_LIMIT_REQUESTS)
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router, prefix="/api", tags=["auth"])
app.include_router(users.router, prefix="/api", tags=["users"])
app.include_router(blockchain.router, prefix="/api", tags=["blockchain"])

@app.on_event("startup")
async def startup_event():
    logger.info(f"Starting {settings.APP_NAME} in {settings.APP_ENV} mode")
    logger.info(f"API documentation available at /docs")

@app.on_event("shutdown")
async def shutdown_event():
    logger.info(f"Shutting down {settings.APP_NAME}")

@app.get("/")
async def root():
    return {
        "message": f"Welcome to {settings.APP_NAME}",
        "status": "online",
        "version": "1.0.0",
        "environment": settings.APP_ENV
    }

@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "services": {
            "api": "up",
            "database": "up",
            "blockchain": "up"
        },
        "version": "1.0.0",
        "environment": settings.APP_ENV
    }

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=settings.APP_PORT,
        reload=settings.APP_DEBUG,
        log_level="debug" if settings.APP_DEBUG else "info"
    ) 