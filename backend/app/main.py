from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded

from app.core.config import settings
from app.api.v1.endpoints import auth, users, items, admin, analytics, claims
from app.middleware.rate_limiter import limiter
from app.middleware.error_handler import global_exception_handler, rate_limit_handler

app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json"
)

# Set all CORS enabled origins
origins = [
    "http://localhost:3000",
    "http://localhost:5173",
    "https://priyesh-lost-n-found.vercel.app",
    "https://lost-found-pri.vercel.app",
]

if settings.BACKEND_CORS_ORIGINS:
    settings_origins = (
        settings.BACKEND_CORS_ORIGINS 
        if isinstance(settings.BACKEND_CORS_ORIGINS, list) 
        else [settings.BACKEND_CORS_ORIGINS]
    )
    origins.extend(settings_origins)

from starlette.middleware.base import BaseHTTPMiddleware
from fastapi import Request, Response

# Custom Middleware to FORCE CORS headers
class ForceCORSMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        if request.method == "OPTIONS":
            response = Response()
        else:
            try:
                response = await call_next(request)
            except Exception as e:
                # Ensure headers are sent even on error
                response = Response(content=str(e), status_code=500)

        origin = request.headers.get("origin")
        if origin:
            response.headers["Access-Control-Allow-Origin"] = origin
            response.headers["Access-Control-Allow-Credentials"] = "true"
            response.headers["Access-Control-Allow-Methods"] = "GET, POST, PUT, DELETE, OPTIONS, PATCH"
            response.headers["Access-Control-Allow-Headers"] = "Content-Type, Authorization, X-Requested-With"
        
        return response

app.add_middleware(ForceCORSMiddleware)

# Keep standard middleware as backup (optional, but good for other features)
app.add_middleware(
    CORSMiddleware,
    allow_origins=[], 
    allow_origin_regex=".*",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Rate Limiting
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, rate_limit_handler)
app.add_exception_handler(Exception, global_exception_handler)

# Routers
app.include_router(auth.router, prefix=f"{settings.API_V1_STR}/auth", tags=["auth"])
app.include_router(users.router, prefix=f"{settings.API_V1_STR}/users", tags=["users"])
app.include_router(items.router, prefix=f"{settings.API_V1_STR}/items", tags=["items"])
app.include_router(admin.router, prefix=f"{settings.API_V1_STR}/admin", tags=["admin"])
app.include_router(analytics.router, prefix=f"{settings.API_V1_STR}/analytics", tags=["analytics"])
app.include_router(claims.router, prefix=f"{settings.API_V1_STR}/claims", tags=["claims"])

@app.get("/")
def root():
    return {"message": "Welcome to Lost & Found API"}
