from fastapi import Request, status
from fastapi.responses import JSONResponse
from slowapi.errors import RateLimitExceeded

def cors_json(content: dict, status_code: int = 400, origin: str = None):
    """
    Always mirror the Origin header back to the client to satisfy CORS.
    """
    if origin is None:
        origin = "https://lost-found-pri.vercel.app"  # safe fallback
    
    return JSONResponse(
        content=content,
        status_code=status_code,
        headers={
            "Access-Control-Allow-Origin": origin,
            "Access-Control-Allow-Credentials": "true",
            "Access-Control-Allow-Methods": "*",
            "Access-Control-Allow-Headers": "*"
        }
    )

async def global_exception_handler(request: Request, exc: Exception):
    origin = request.headers.get("origin", "https://lost-found-pri.vercel.app")
    return cors_json(
        content={"detail": "Internal Server Error"},
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        origin=origin
    )

async def rate_limit_handler(request: Request, exc: RateLimitExceeded):
    origin = request.headers.get("origin", "https://lost-found-pri.vercel.app")
    return cors_json(
        content={"detail": "Rate limit exceeded"},
        status_code=status.HTTP_429_TOO_MANY_REQUESTS,
        origin=origin
    )
