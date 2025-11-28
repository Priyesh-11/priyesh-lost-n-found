from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from slowapi.errors import RateLimitExceeded
import logging

from app.core.config import settings
from app.api.v1.endpoints import auth, users, items, admin, analytics, claims
from app.middleware.rate_limiter import limiter
from app.middleware.error_handler import global_exception_handler, rate_limit_handler

logger = logging.getLogger(__name__)

app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json"
)

# CRITICAL: CORS must be the FIRST middleware for proper header injection
# Use settings for CORS origins to allow environment configuration
cors_origins = settings.BACKEND_CORS_ORIGINS if settings.BACKEND_CORS_ORIGINS else []
# Always include production frontend and localhost for development
default_origins = [
    "https://lost-found-pri.vercel.app",
    "http://localhost:3000",
    "http://localhost:5173"
]
# Merge and deduplicate origins
all_origins = list(set(cors_origins + default_origins)) if isinstance(cors_origins, list) else default_origins

app.add_middleware(
    CORSMiddleware,
    allow_origins=all_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"]
)

# TRUSTED HOST - MUST USE WILDCARDS to prevent blocking Vercel/Render subdomains
# Without wildcards, requests are REJECTED BEFORE CORS runs = No CORS headers!
app.add_middleware(
    TrustedHostMiddleware,
    allowed_hosts=[
        "*.vercel.app",        # Allows all Vercel deployments (prod + preview)
        "*.onrender.com",      # Allows Render backend
        "localhost",
        "127.0.0.1"
    ]
)

# Rate limiting
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

@app.on_event("startup")
async def startup_event():
    """Validate SMTP configuration on startup"""
    logger.info("="*80)
    logger.info("🚀 Starting Lost & Found API")
    logger.info("="*80)
    
    # Check SMTP configuration
    if settings.SMTP_HOST and settings.SMTP_USER and settings.SMTP_PASSWORD:
        logger.info(f"✅ SMTP configured: {settings.SMTP_HOST}:{settings.SMTP_PORT or 587}")
        logger.info(f"   From: {settings.EMAILS_FROM_EMAIL or settings.SMTP_USER}")
        logger.info("   Email sending is ENABLED")
    else:
        logger.warning("⚠️  SMTP NOT FULLY CONFIGURED:")
        logger.warning(f"   SMTP_HOST: {'✅' if settings.SMTP_HOST else '❌'}")
        logger.warning(f"   SMTP_USER: {'✅' if settings.SMTP_USER else '❌'}")
        logger.warning(f"   SMTP_PASSWORD: {'✅' if settings.SMTP_PASSWORD else '❌'}")
        logger.warning("   ⚠️  Emails will be logged to console only!")
        logger.warning("   To enable email sending, set SMTP_HOST, SMTP_USER, and SMTP_PASSWORD environment variables")
    
    logger.info("="*80)

@app.get("/")
def root():
    return {"message": "Welcome to Lost & Found API"}
