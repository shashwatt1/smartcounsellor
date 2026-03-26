from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from mangum import Mangum
from app.routes import predict
from app.config import config

app = FastAPI(
    title="Smart Counsellor AI",
    description="Determiniscially predict colleges based on JEE rank thresholds",
    version="1.0.0",
)

# CORS — allow frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"] if config.CORS_ORIGINS == "*" else config.CORS_ORIGINS.split(","),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register routers
app.include_router(predict.router, prefix="/api", tags=["predict"])


@app.get("/", tags=["health"])
async def root():
    return {"status": "ok", "message": "Smart Counsellor API is running", "debug": config.DEBUG}

# AWS Lambda Serverless Entry Point
handler = Mangum(app)
