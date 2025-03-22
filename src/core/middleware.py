from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import Response
import time
from .logging import logger
from .config import settings

class RequestLoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        start_time = time.time()
        
        # Log request
        logger.info(f"Request: {request.method} {request.url.path}")
        
        # Process request
        response = await call_next(request)
        
        # Calculate processing time
        process_time = time.time() - start_time
        
        # Log response
        logger.info(
            f"Response: {request.method} {request.url.path} "
            f"Status: {response.status_code} "
            f"Time: {process_time:.2f}s"
        )
        
        return response

class CORSMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        response = await call_next(request)
        
        # Add CORS headers
        response.headers["Access-Control-Allow-Origin"] = ",".join(settings.CORS_ORIGINS)
        response.headers["Access-Control-Allow-Credentials"] = "true"
        response.headers["Access-Control-Allow-Methods"] = "GET, POST, PUT, DELETE, OPTIONS"
        response.headers["Access-Control-Allow-Headers"] = "Content-Type, Authorization"
        
        return response

class RateLimitMiddleware(BaseHTTPMiddleware):
    def __init__(self, app, requests_per_minute: int = 100):
        super().__init__(app)
        self.requests_per_minute = requests_per_minute
        self.requests = {}

    async def dispatch(self, request: Request, call_next):
        client_ip = request.client.host
        current_time = time.time()

        # Clean up old requests
        self.requests = {
            ip: reqs for ip, reqs in self.requests.items()
            if current_time - reqs["timestamp"] < 60
        }

        # Check rate limit
        if client_ip in self.requests:
            if self.requests[client_ip]["count"] >= self.requests_per_minute:
                logger.warning(f"Rate limit exceeded for IP: {client_ip}")
                return Response(
                    content="Too many requests",
                    status_code=429,
                    media_type="text/plain"
                )
            self.requests[client_ip]["count"] += 1
        else:
            self.requests[client_ip] = {
                "count": 1,
                "timestamp": current_time
            }

        return await call_next(request) 