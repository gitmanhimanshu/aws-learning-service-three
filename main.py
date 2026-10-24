import time
import logging
import datetime
from fastapi import FastAPI, Request
from config import settings

logging.basicConfig(
    level=settings.LOG_LEVEL,
    format="%(asctime)s [%(levelname)s] service=%(name)s %(message)s",
    datefmt="%Y-%m-%dT%H:%M:%SZ"
)
logger = logging.getLogger(settings.SERVICE_NAME)

app = FastAPI(
    title="AWS Learning - Service Three (Analytics & Calculation Service)",
    version=settings.VERSION,
    description="Microservice 3: Demonstrates adding a new service to existing architecture."
)

@app.middleware("http")
async def structured_log_middleware(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    duration_ms = round((time.time() - start_time) * 1000, 2)
    logger.info(
        "environment=%s method=%s path=%s status=%d duration_ms=%.2f",
        settings.ENVIRONMENT,
        request.method,
        request.url.path,
        response.status_code,
        duration_ms
    )
    return response

def get_welcome_data():
    return {
        "service": settings.SERVICE_NAME,
        "message": "Welcome to Service Three (Analytics & Calculation)",
        "timestamp": datetime.datetime.utcnow().isoformat() + "Z"
    }

def get_health_data():
    return {
        "status": "healthy",
        "service": settings.SERVICE_NAME,
        "environment": settings.ENVIRONMENT,
        "timestamp": datetime.datetime.utcnow().isoformat() + "Z"
    }

def get_info_data():
    return {
        "service": settings.SERVICE_NAME,
        "version": settings.VERSION,
        "environment": settings.ENVIRONMENT,
        "status": "running",
        "purpose": "Demonstrates adding new microservice dynamically"
    }

def get_calculate_data(a: int = 10, b: int = 20):
    return {
        "service": settings.SERVICE_NAME,
        "operation": "multiplication",
        "input_a": a,
        "input_b": b,
        "result": a * b,
        "calculated_at": datetime.datetime.utcnow().isoformat() + "Z"
    }

# Standard root endpoints
@app.get("/")
def read_root():
    return get_welcome_data()

@app.get("/health")
def read_health():
    return get_health_data()

@app.get("/info")
def read_info():
    return get_info_data()

@app.get("/calculate")
def read_calculate(a: int = 10, b: int = 20):
    return get_calculate_data(a, b)

# ALB Path-based routing compatibility (/service3/*)
@app.get("/service3")
@app.get("/service3/")
def read_root_prefixed():
    return get_welcome_data()

@app.get("/service3/health")
def read_health_prefixed():
    return get_health_data()

@app.get("/service3/info")
def read_info_prefixed():
    return get_info_data()

@app.get("/service3/calculate")
def read_calculate_prefixed(a: int = 10, b: int = 20):
    return get_calculate_data(a, b)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=settings.PORT, reload=True)
